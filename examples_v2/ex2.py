#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


"""
Search yahoo news and twitter for facebook
Combine results with techmeme feeds based on titles having at least 2 term overlap
Print results to stdout
"""

__author__ = "BOSS Team"

from util import console, text
from yos.yql import db, udfs
from yos.boss import ysearch

gn = db.create(name="gn", data=ysearch.search("facebook", bucket="news", count=40))
gn.rename("headline", "title")

sm = db.create(name="sm", url="http://search.twitter.com/search.json?q=facebook&rpp=40")
sm.rename("text", "title")

tm = db.select(name="tm", udf=udfs.unnest_value, url="http://techmeme.com/firehose.xml")

def overlap(r1, r2):
  return text.overlap(r1["title"], r2["title"]) > 1

j = db.join(overlap, [gn, sm, tm])
j = db.sort(key="sm$id", table=j)

for r in j.rows:
  console.write( "\n%s\n[yahoo] %s\n[twitter] %s\n[techmeme] %s\n" % (r["sm$created_at"], r["gn$title"], r["sm$title"], r["tm$title"]) )
