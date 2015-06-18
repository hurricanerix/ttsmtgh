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


def file_exists(filepath):
    if not os.path.isfile(filepath):
        return False
    d, f = os.path.split(filepath)
    return f in os.listdir(d)


def parse_card(l):
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
    c['release'] = parts[1 + offset].strip('[]')
    c['name'] = parts[2 + offset]
    return c


def get_deck(filepath):
    if not filepath.lower().endswith('.mwdeck'):
        raise Exception('file does not have a .mwDeck extension')
    if not file_exists(filepath):
        raise Exception('file does not exist: {}'.format(filepath))

    f = open(filepath, 'r')

    if '// Bestiaire Magic Draft' not in f.readline():
        raise Exception('invalid BMD file')

    while f.readline().startswith('//'):
        pass

    deck = []
    eof = False
    while not eof:
        l = f.readline().rstrip('\n')
        if l == '':
            eof = True
            continue
        deck.append(parse_card(l))

    return deck
