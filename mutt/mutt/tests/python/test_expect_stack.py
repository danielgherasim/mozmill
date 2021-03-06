#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import json
import unittest
import subprocess


class ModuleTest(unittest.TestCase):
    def test_expectstack(self):
        # This is going to simply call mozmill and get the output.  In the
        # old method of running, we wouldn't even see the name of our
        # test in the output (the test in this case is testExpectStack.js)
        # and so we can verify this bug is fixed by ensuring that exists
        # and that the stack is valid JSON.  Here goes...
        relpath = os.path.join("js-modules", "testExpectStack.js")
        testpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                relpath)
        p = subprocess.Popen(["mozmill", "-t", testpath],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        errline = re.compile('ERROR \| Test Failure\: (.*)')
        lines = output.split("\n")
        for line in lines:
            m = errline.match(line)
            if m:
                j = json.loads(m.group(1))
                found = False
                node = j["fail"]["stack"]
                while not found:
                    if (("filename" in node) and
                        (node["filename"] is not None) and
                        ("testExpectStack.js" in node["filename"])):
                        self.assertTrue(True, msg="Found expected stackframe")
                        found = True
                    else:
                        if "caller" in node:
                            node = node["caller"]
                            self.assertTrue(node is not None,
                                            msg="No stack frame available.")
                        else:
                            self.assertTrue(False, msg="Invalid stack.")


if __name__ == '__main__':
    unittest.main()
