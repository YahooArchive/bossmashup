#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.

"""
This answers questions that ask when something happened
It searches the question, and counts the month and year tokens in the titles and abstracts of the results
Then does a group by, summing up the frequencies, and prints the top month and year combination
This technique actually works sometimes ...
"""

__author__ = "BOSS Team"

from util import console, text
from yos.yql import db
from yos.boss import ysearch

def month_lookup(s):
  for m in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sept", "oct", "nov", "dec"]:
    if s.startswith(m):
      return m

def parse_month(s):
  months = filter(lambda m: m is not None, map(month_lookup, text.uniques(s)))
  if len(months) > 0:
    return text.norm(months[0])

def parse_year(s):
  years = filter(lambda t: len(t) == 4 and t.startswith("19") or t.startswith("200"), text.uniques(s))
  if len(years) > 0:
    return text.norm(years[0])

def date_udf(r):
  return {"year": parse_year(r["abstract"]), "month": parse_month(r["abstract"]), "count": 1}

# since max fetch size in v1 is 50, let's do two calls and increment start to get the first 100 results
i1 = db.select(name="i1", udf=date_udf, data=ysearch.search_v1("when was jfk assasinated", count=50))
i2 = db.select(name="i2", udf=date_udf, data=ysearch.search_v1("when was jfk assasinated", start=50, count=50))

iraq = db.union(name="iraq", tables=[i1, i2])
dates = db.group(by=["iraq$year", "iraq$month"], key="iraq$count", reducer=lambda d1,d2: d1+d2, as="total", table=iraq)
dates = db.sort(key="total", table=dates)

for row in dates.rows:
  month = row["iraq$month"]
  year = row["iraq$year"]
  if month is not None and year is not None:
    console.write( "Month: %s\tYear: %s\tTotal: %d\n" % (month, year, row["total"]) )
