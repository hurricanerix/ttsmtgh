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
import logging

from ttsmtgh.sheet import Swriter
from ttsmtgh.mwdeck import MWDeck
from ttsmtgh.mcinfo import MTGInfo

version = '0.0'


def run(args):
    logging.basicConfig()
    logger = logging.getLogger('ttsmtgh')

    appio = None
    if args.verbose:
        appio = sys.stdout
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("running app")

    mwd = MWDeck(args.deck, io=appio, logger=logger)
    mwd.load()
    mtgi = MTGInfo(mwd.releases, io=appio, logger=logger)
    mtgi.load()

    outfile = args.outfile or '{}.jpg'.format(args.deck)
    sw = Swriter(outfile)
    sw.open()
    for c in mwd.deck:
        name = c.get('name')
        release = c.get('release')
        path = mtgi.scan_location(release, name)
        sw.append(path)
    sw.close()
