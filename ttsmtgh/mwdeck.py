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

import os


conv_table = {
    'a': 'al',
}


class MWDeck(object):

    def __init__(self, filename, io=None, logger=None):
        self.logger = logger
        self._debug('MWDeck.__init__(\'{}\', io={}, logger={})'.format(filename, io, logger))
        self.filename = filename
        self.io = io
        self.deck = []
        self.releases = set()

    def _print(self, msg):
        if self.io:
            print(msg, file=self.io)

    def _debug(self, msg):
        if self.logger:
            self.logger.debug(msg)

    def _mw2info(self, release):
        self._debug('MWDeck._mw2info(\'{}\')'.format(release))
        r = conv_table.get(release, release)
        self._debug('MWDeck._mw2info <- \'{}\''.format(r))
        return r

    def _parse_card(self, l):
        self._debug('MWDeck._parse_card(\'{}\')'.format(l))
        c = {'sb': False}
        offset = 0
        l = l.lower()
        if l.startswith('sb:'):
            parts = l.split(' ', 3)
            c['sb'] = True
            offset = 1
        else:
            parts = l.split(' ', 2)
        c['count'] = int(parts[0 + offset])
        c['release'] = self._mw2info(parts[1 + offset].strip('[]'))
        c['name'] = parts[2 + offset]
        self._debug('MWDeck._parse_card <- {}'.format(c))
        return c

    def load(self):
        self._debug('MWDeck.load()')
        name = self.filename
        if not name.lower().endswith('.mwdeck'):
            raise Exception('file does not have a .mwDeck extension')
        if not os.path.isfile(name):
            raise Exception('file does not exist: {}'.format(name))
        self._print('Reading deck "{}"'.format(name))
        f = open(name, 'r')
        if '// Bestiaire Magic Draft' not in f.readline():
            raise Exception('invalid BMD file')
        while f.readline().startswith('//'):
            pass
        eof = False
        while not eof:
            l = f.readline().rstrip('\n')
            if l == '':
                eof = True
                continue
            self._print(l)
            c = self._parse_card(l)
            self.deck.append(c)
            self.releases.add(str(c['release']))
        self._debug('MWDeck.load <- None')
