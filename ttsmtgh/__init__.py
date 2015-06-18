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

import sys

from ttsmtgh.mwdeck import get_deck

version = '0.0'


CARD_LIST_URL = 'http://magiccards.info/{release}/en.html'
SCAN_URL = 'http://magiccards.info/scans/en/{release}/{card_index}.jpg'


def run(args):
    try:
        d = get_deck(args.deck)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)
    print(d)
