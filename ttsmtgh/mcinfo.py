# Copyright (c) 2015 Richard Hawkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
import requests

from os.path import expanduser


CARD_LIST_URL = 'http://magiccards.info/{release}/en.html'
SCAN_URL = 'http://magiccards.info/scans/en/{release}/{index}.jpg'
BASE_CACHE_DIR = expanduser("~/.ttsmtgh")


def cached_catalog(release):
    cachefile = '{}/catalogs/{}.json'.format(BASE_CACHE_DIR, release)
    if not os.path.isfile(cachefile):
        return None
    f = open(cachefile, 'r')
    d = f.read()
    f.close()
    if not d:
        return None
    return json.loads(d)


def cache_catalog(release, catalog):
    cachefile = '{}/catalogs/{}.json'.format(BASE_CACHE_DIR, release)
    if not os.path.exists(os.path.dirname(cachefile)):
        os.makedirs(os.path.dirname(cachefile))
    f = open(cachefile, 'w')
    f.write(json.dumps(catalog))
    f.close()


def cached_scan(release, index):
    cachefile = '{}/scans/{}/{}.jpg'.format(BASE_CACHE_DIR, release, index)
    if not os.path.isfile(cachefile):
        return None
    f = open(cachefile, 'br+')
    d = f.read()
    f.close()
    return d


def cache_scan(release, index, data):
    cachefile = '{}/scans/{}/{}.jpg'.format(BASE_CACHE_DIR, release, index)
    if not os.path.exists(os.path.dirname(cachefile)):
        os.makedirs(os.path.dirname(cachefile))
    f = open(cachefile, 'bw+')
    f.write(data)
    f.close()


def get_catalog(release):
    cache = cached_catalog(release)
    if cache:
        return cache
    url = CARD_LIST_URL.format(release=release)
    r = requests.get(url)
    if not r.ok:
        raise Exception('could not get catalog from: {}'.format(url))

    regex = ('.*<td><a href="/{}/en/([0-9]+)\.html">(.+)</a></td>.*'.format(
             release))
    p = re.compile(regex)

    c = {}
    for l in r.content.decode("utf-8").split('\n'):
        m = p.match(l)
        if m:
            c[m.group(2).lower()] = int(m.group(1))
    cache_catalog(release, c)
    return c


def get_scan(release, index):
    if cached_scan(release, index):
        return None
    url = SCAN_URL.format(release=release, index=index)
    r = requests.get(url)
    if not r.ok:
        raise Exception('could not get scan from: {}'.format(url))
    cache_scan(release, index, r.content)
    return r.content


def get_scans(deck):
    catalog = {}
    for c in deck:
        r = c.get('release', '')
        if r not in catalog:
            catalog[r] = get_catalog(r)
        n = c.get('name')
        i = catalog[r].get(n)
        get_scan(r, i)
