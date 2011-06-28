#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


"""
Four way of join of 'google android' on yahoo news, summize, youtube, and digg
Combine results based on titles having an overlap of 3 terms or more
Group results based on yahoo news title (remove duplicates)
Redefined the group by equality operator to use text.norm to do near duplicate text removal
In the group sum the digg and youtube favorite counts as the rank for each joined result
Sort by rank, print to stdout
"""

__author__ = "BOSS Team"

from util import console, text
from yos.yql import db
from yos.boss import ysearch

ynews_data = ysearch.search_v1("google android", vertical="news", count=100, more={"news.ranking": "date"})
ynews = db.create(name="ynews", data=ynews_data)
ynews.rename(before="headline", after="title")

sm = db.create(name="sm", url="http://summize.com/search.json?q=google+android&rpp=60&lang=en")
sm.rename(before="text", after="title")

ytf = lambda r: {"title": r["title"]["value"], "favorites": int(r["statistics"]["favoriteCount"])}
yt = db.select(name="yt", udf=ytf, url="http://gdata.youtube.com/feeds/api/videos?vq=google+android&lr=en&orderby=published")

diggf = lambda r: {"title": r["title"]["value"], "diggs": int(r["diggCount"]["value"])}
digg = db.select(name="dg", udf=diggf, url="http://digg.com/rss_search?search=google+android&area=dig&type=both&section=news")

def overlap_predicate(r1, r2):
  return text.overlap(r1["title"], r2["title"]) > 2

tb = db.join(overlap_predicate, [ynews, sm, digg, yt])

def socialf(row):
  row.update({"social": row["dg$diggs"] + row["yt$favorites"]}) ; return row

tb = db.select(udf=socialf, table=tb)
tb = db.group(by=["ynews$title"], key="social", reducer=lambda d1,d2: d1+d2, as="rank", table=tb, norm=text.norm)
tb = db.sort(key="rank", table=tb)

for r in tb.rows:
  console.write( "\n%s\n[y] %s\n[t] %s\n[sr] %d\n" % (r["sm$created_at"], r["ynews$title"], r["sm$title"], r["rank"]) )
