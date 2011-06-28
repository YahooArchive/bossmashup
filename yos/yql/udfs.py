#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


""" Some handy user defined functions to plug in db.select """

__author__ = "BOSS Team"

from util.typechecks import is_dict

def unnest_value(row):
  """
  For data collections which have nested value parameters (like RSS)
  this function will unnest the value to the higher level.
  For example, say the row is {"title":{"value":"yahoo wins search"}}
  This function will take that row and return the following row {"title": "yahoo wins search"}
  """
  nr = {}
  for k, v in row.iteritems():
    if is_dict(type(v)) and "value" in v:
      nr[k] = v["value"]
    else:
      nr[k] = v
  return nr
