#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


"""
Calculate the size of an object in python
This code used to be very complicated, and then realized in certain cases it failed
Given the structures handled in this framework, string'ing it and computing the length works fine
Especially since the # of bytes is not important - just need the relative sizes between objects
relsize is used to rank candidate collections of objects inferred from a REST response
The largest sized one wins
"""

__author__ = "BOSS Team"

def relsize(o):
  return len(str(o))
