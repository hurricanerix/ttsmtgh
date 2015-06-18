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

# import os, sys

from PIL import Image


class Swriter(object):

    def __init__(self, filename, w=10, h=7):
        self.filename = filename
        self.w = w
        self.h = h
        self._curr_w = 0
        self._curr_h = 0
        self._im = None

    def _next(self):
        self._curr_w += 1
        if self._curr_w >= self.w:
            self._curr_h += 1
            self._curr_w = 0
        if self._curr_h >= self.h:
            raise Exception('out of room')

    def open(self):
        self._im = Image.new('RGB', (312 * self.w, 445 * self.h), 'white')

    def close(self):
        self._im.save(self.filename, 'JPEG')

    def append(self, path):
        scan = Image.open(path)
        offset = (312 * self._curr_w, 445 * self._curr_h)
        self._im.paste(scan, offset)
        self._next()
