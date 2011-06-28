#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.

"""
Inner join popular delicious results and yahoo news results for the query 'iphone'
Combine results which have at least 2 terms in common in their titles
Then publish as a search results html page using the provided california template
"""

__author__ = "BOSS Team"

from templates import publisher
from util import text, console
from yos.boss.ysearch import search_v2
from yos.yql import db, udfs

dl = db.select(name="dl", udf=udfs.unnest_value, url="http://feeds.delicious.com/rss/popular/iphone")
dl.describe()
yn = db.create(name="yn", data=search_v2("iphone", bucket="news", count=50))

def overlap_predicate(r1, r2):
  return text.overlap(r1["title"], r2["title"]) > 1

serp = publisher.Serp(template_dir="templates/california", title="boss 'iphone'", endpoint="http://yahoo/search")

tb = db.join(overlap_predicate, [dl, yn])
tb = db.group(by=["yn$title"], key=None, reducer=lambda x,y: None, as=None, table=tb, norm=text.norm)

for row in tb.rows:
  serp.add(url=row["dl$link"], title=row["yn$title"], abstract=row["yn$abstract"], dispurl=row["yn$sourceurl"], source=row["dl$creator"])

serp.dump("iphone.html")
