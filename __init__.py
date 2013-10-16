from __future__ import print_function
import sys
import re
from css_sort.__version__ import __version__

#
# The MIT License (MIT)

# Copyright (c) 2013 Einar Lielmanis and contributors.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def usage(stream=sys.stdout):

    print("css_sort.py@" + __version__ + """

CSS Sort (https://github.com/bthorben/css_sort)

""", file=stream)
    if stream == sys.stderr:
        return 1
    else:
        return 0

WHITE_RE = re.compile("^\s+$")
WORD_RE = re.compile("[\w$\-_]")


def sort(source):
    s = Sorter(source)
    return s.sort()


def sort_file(file_name):
    if file_name == '-':  # stdin
        stream = sys.stdin
    else:
        stream = open(file_name)
    content = ''.join(stream.readlines())
    s = Sorter(content)
    return s.sort()


class Sorter:

    def __init__(self, source):
        self.source = source

    def sort(self):
        result = self.source
        regions = self.getRules()
        for r in regions:
            rule = self.source[r[0]+1:r[1]]
            sortedRule = self.sortRule(rule)
            result = result[:r[0]+1] + sortedRule + result[r[1]:]

        return result

    def sortRule(self, rule):

        def getName(s):
            ss = s.split(":")
            name = ss[0].strip()
            name = re.sub("-o-|-moz-|-webkit-|-ms-", "", name)
            name = re.sub("/\*(?s).*\*/", "", name)
            return name.strip()

        properties = {}
        props = rule.split(";")

        last = props[-1]
        if getName(last) is "":
            props[-2] = props[-2] + ";" + last
            properties[getName(props[-2])] = props[-2]

        for prop in props[:-2]:
            properties[getName(prop)] = prop + ";"

        pieces = [properties[n] for n in sorted(properties)]
        return "".join(pieces)

    def getRules(self):

        def skipTo(pos, string):
            while pos <= len(self.source) - len(string):
                pos = pos + 1
                if self.source[pos:pos + len(string)] == string:
                    return pos + 1
            return pos

        regions = []
        pos = 0
        rstart = -1

        while pos < len(self.source):
            ch = self.source[pos]
            peek = self.source[min(pos + 1, len(self.source) - 1)]

            if ch == "{":
                rstart = pos
                pos = pos + 1
            elif ch == "}":
                if rstart >= 0:
                    regions.append((rstart, pos))
                    rstart = -1
                pos = pos + 1
            elif ch == "/" and peek == "*":
                pos = skipTo(pos, "*/")
            elif ch == "\"":
                # TODO: this doesn't take escaped quotes into account
                pos = skipTo(pos, "\"")
            elif ch == "'":
                pos = skipTo(pos, "'")
            else:
                pos = pos + 1

        return regions
