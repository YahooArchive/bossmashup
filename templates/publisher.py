#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


"""
Main class here is Serp (Search Engine Results Page)
This is a simple templating library for binding search results with html templates
Check out the california dir to see how templates are formatted and feel free to model to create your own
Look at examples/ex1 in the root directory to see how to use Serp
If you're looking for a more power templating library, try clearsilver
"""

__author__ = "BOSS Team"

from collections import defaultdict
from os.path import abspath

from util import console
from yos.yql.db import strip_prep

def serp(tr, title, endpoint, results):
  html = open(tr + "/page/page.html", "r").read()
  ht = tr + "/page/page.css"
  at = tr + "/result/result.css"
  html = html.replace("<?header_background_img_dir?>", tr + "/page/", 1)
  html = html.replace("<?header_css?>", ht, 1)
  html = html.replace("<?header_abstract_css?>", at, 1)
  html = html.replace("<?header_title?>", title, 1)
  html = html.replace("<?header_endpoint?>", endpoint, 1)
  return html.replace("<?header_results?>", "".join(results), 1)

def set_result(html, url, title, abstract, dispurl, source, imageurl):
  html = html.replace("<?result_imageurl?>", imageurl, 1)
  html = html.replace("<?result_source?>", source, 1)
  html = html.replace("<?result_clickurl?>", url, 1)
  html = html.replace("<?result_title?>", title, 1)
  html = html.replace("<?result_abstract?>", abstract, 1)
  return html.replace("<?result_dispurl?>", dispurl, 1)

def scratch_result(template, url, title, abstract="", dispurl="", source="", imageurl=""):
  html = open(template, "r").read()
  return set_result(html, url, title, abstract, dispurl, source, imageurl)

def prepare_row(row):
  """ Just removes namespacing in the field names """
  nr = defaultdict(lambda: "")
  existing = map(lambda item: (strip_prep(item[0]), item[1]), row.iteritems())
  nr.update(existing)
  return nr

class Serp:
  def __init__(self, template_dir, title, endpoint, result_template="result_default.html", maker=set_result):
    """
    template_dir specifies which template directory to use e.g. 'templates/california' that is provided
    title is the title of the search results html webpage
    result_template is an optional parameter to specifying another search result template
    maker is a function that follows the result template design to bind html e.g. set_result sets <?result_title?>
    """
    self._tr = abspath(template_dir.rstrip("/"))
    self._title = title
    self._endpoint = endpoint
    self._html = open(self._tr + "/result/" + result_template, "r").read()
    self.results = []
    self._maker = maker

  def add(self, url, title, abstract="", dispurl="", source="", imageurl=""):
    self.results.append( self._maker(self._html, url, title, abstract, dispurl, source, imageurl) )

  def _bind_row(self, row):
    nr = prepare_row(row)
    return self.add(nr["clickurl"], nr["title"], nr["abstract"], nr["dispurl"], nr["source"], nr["imageurl"])

  def bind_table(self, table):
    """
    If the table contains rows (dictionaries) which have the fields referenced in _bind_row,
    then just pass the table here and forget doing a loop around the add call
    """
    for row in table.rows:
      self._bind_row(row)

  def dumps(self):
    """ Return resulting html as a string """
    return console.strfix(serp(self._tr, self._title, self._endpoint, results=self.results))

  def dump(self, f):
    """ Save resulting html as a file named f """
    o = open(f, "w")
    o.write(self.dumps())
    o.close()
