#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


"""
Search 'iphone' on yahoo news and sort by date
Get the wikipedia edits for the iphone page
Rank the news results based on their title/text overlap with the wikipedia entries
Sort by the overlap sizes
This could potentially be a new freshness model, based on the idea that wikipedia is updated for recent significance
"""

__author__ = "BOSS Team"

from util import console, text
from yos.boss import ysearch
from yos.yql import db

yn = db.create(name="yn", data=ysearch.search_v1("iphone sdk", vertical="news", count=50, more={"news.ranking": "date"}))
wiki = db.create(name="wiki", url="http://en.wikipedia.org/w/index.php?title=IPhone_OS&feed=atom&action=history")

tb = db.cross([yn, wiki])

def rankf(row):
  row.update( {"rank": text.overlap(row["yn$abstract"], row["wiki$summary"]["value"])} ) ; return row

tb = db.select(udf=rankf, table=tb)
tb = db.group(by=["yn$title"], key="rank", reducer=lambda d1,d2: d1+d2, as="total", table=tb, norm=text.norm)
tb = db.sort(key="total", table=tb)

print "Before\n"
for r in yn.rows:
  console.write( "[news] %s\n" % r["yn$title"] )

print "After\n"
for r in tb.rows:
  console.write( "[news] %s\n[source] %s\t[rank] %d\n" % (r["yn$title"], r["yn$source"], r["total"]) )

