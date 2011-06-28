#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


__author__ = "BOSS Team"

from yos.crawl import object_dict
from types import DictType, ListType, TupleType

OBJ_DICT_TYPE = type(object_dict.object_dict())

def is_dict(td):
  return td is DictType or td is OBJ_DICT_TYPE
                
def is_ordered(to):
  return to is ListType or to is TupleType

def is_list(o):
  return o is ListType    
