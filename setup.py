#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.

__author__ = "BOSS Team"

from distutils.core import setup
from os import path
from shutil import copy

if not path.exists("deps"):
  raise Error, "Could not locate deps folder. Please see README on how to create one."

copy("deps/dict2xml/_dict2xml.py", "yos/crawl/dict2xml.py")
copy("deps/xml2dict/xml2dict.py", "yos/crawl/xml2dict.py")
copy("deps/xml2dict/object_dict.py", "yos/crawl/object_dict.py")

files = ["*.*"]

setup(name = "boss_mashup_framework",
      version = "0.1",
      description = "A library for joining external web services with Yahoo's Boss API to produce unique search results pages",
      author = "Vik Singh",
      author_email = "viksi@yahoo-inc.com",
      url = "http://developer.yahoo.com",
      data_files= [("", ["config.json"])],
      package_dir={"templates/california": "templates/california"},
      packages = ['examples_v1', 'examples_v2', 'templates', 'util', 'yos', 'yos.boss', 'yos.crawl', 'yos.yql'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Web Services :: Search',
        'Environment :: Web Environment',
        'License :: Free To Use But Restricted',
        'License :: Other/Proprietary License'
      ]
) 
