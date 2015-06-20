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


class MTGInfo(object):

    def __init__(self, releases, io=None, logger=None):
        self.logger = logger
        self._debug('MTGInfo.__init__(\'{}\', io={}, logger={})'.format(releases, io, logger))
        self.releases = releases or set()
        self.io = io
        self.catalogs = {}

    def load(self):
        self._debug('MTGInfo.load()')
        for r in self.releases:
            self.catalogs[r] = self._get_catalog(r)
            self._get_scans(r)
        self._debug('MTGInfo.load <- None')

    def scan_location(self, release, name):
        self._debug('MTGInfo.scan_location(\'{}\', \'{}\')'.format(release, name))
        index = self.catalogs[release].get(name)
        if index is None:
            raise Exception('Could not get index for "{}/{}"'.format(release, name))
        location = '{}/scans/{}/{}.jpg'.format(BASE_CACHE_DIR, release, index)
        self._debug('MTGInfo.scan_location <- {}'.format(location))
        return location

    def _get_catalog(self, release):
        self._debug('MTGInfo._get_catalog(\'{}\')'.format(release))
        cache = self._cached_catalog(release)
        if cache:
            self._debug('MTGInfo._get_catalog <- (cached)')
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
        self._debug('MTGInfo._get_catalog <- {}'.format(c))
        return c

    def _cache_catalog(self, release, catalog):
        self._debug('MTGInfo._cache_catalog(\'{}\', \'{}\')'.format(release, catalog))
        cachefile = '{}/catalogs/{}.json'.format(BASE_CACHE_DIR, release)
        if not os.path.exists(os.path.dirname(cachefile)):
            os.makedirs(os.path.dirname(cachefile))
        f = open(cachefile, 'w')
        f.write(json.dumps(catalog))
        f.close()
        self._debug('MTGInfo._cache_catalog <- None')

    def _cached_catalog(self, release):
        self._debug('MTGInfo._cached_catalog(\'{}\')'.format(release))
        cachefile = '{}/catalogs/{}.json'.format(BASE_CACHE_DIR, release)
        if not os.path.isfile(cachefile):
            self._debug('MTGInfo._cached_catalog <- None')
            return None
        f = open(cachefile, 'r')
        json_data = f.read()
        f.close()
        if not json_data:
            self._debug('MTGInfo._cached_catalog <- None')
            return None
        data = json.loads(json_data)
        self._debug('MTGInfo._cached_catalog <- {}'.format(data))
        return data

    def _get_scans(self, release):
        self._debug('MTGInfo._get_scans(\'{}\')'.format(release))
        for n, i in self.catalogs[release].items():
            self._get_scan(release, i)
        self._debug('MTGInfo._get_scans <- None')

    def _get_scan(self, release, index):
        self._debug('MTGInfo._get_scan(\'{}\', \'{}\')'.format(release, index))
        if self._cached_scan(release, index):
            self._debug('MTGInfo._get_scan <- None (cached)')
            return None
        url = SCAN_URL.format(release=release, index=index)
        r = requests.get(url)
        if not r.ok:
            raise Exception('could not get scan from: {}'.format(url))
        self._cache_scan(release, index, r.content)
        self._debug('MTGInfo._get_scan <- (image data)')
        return r.content

    def _cached_scan(self, release, index):
        self._debug('MTGInfo._cached_scan(\'{}\', \'{}\')'.format(release, index))
        cachefile = '{}/scans/{}/{}.jpg'.format(BASE_CACHE_DIR, release, index)
        if not os.path.isfile(cachefile):
            self._debug('MTGInfo._cache_catalog <- None')
            return None
        f = open(cachefile, 'br+')
        d = f.read()
        f.close()
        self._debug('MTGInfo._cache_catalog <- (image data)')
        return d

    def _cache_scan(self, release, index, data):
        self._debug('MTGInfo._cache_scan(\'{}\', {}, (image data)'.format(release, index))
        cachefile = '{}/scans/{}/{}.jpg'.format(BASE_CACHE_DIR, release, index)
        if not os.path.exists(os.path.dirname(cachefile)):
            os.makedirs(os.path.dirname(cachefile))
        f = open(cachefile, 'bw+')
        f.write(data)
        f.close()
        self._debug('MTGInfo._cache_scan <- None')

    def _print(self, msg):
        if self.io:
            print(msg, file=self.io)

    def _debug(self, msg):
        if self.logger:
            self.logger.debug(msg)
