#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


""" Functions for downloading REST API's and converting their responses into dictionaries """

__author__ = "BOSS Team"

import urllib2
import urllib

import simplejson
import xml2dict

HEADERS = {"User-Agent": simplejson.load(open("config.json", "r"))["agent"]}

def download(url):
  try:
    r = urllib.urlopen(url).read()
    if all(map(lambda t: r.find(t) > 1, ["</head>", "</body>", "</html>"])):
      raise Error, "Why is this an html response?"
    return r
  except:
    req = urllib2.Request(url, None, HEADERS)
    return urllib2.urlopen(req).read()

def load_json(url):
  return simplejson.loads(download(url))

def load_xml(url):
  return xml2dict.fromstring(download(url))

def load(url):
  dl = download(url)
  try:
    return simplejson.loads(dl)
  except:
    return xml2dict.fromstring(dl)
