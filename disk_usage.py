#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os

import json

#app imports
from size_element import SizeElement
from size_element import SizeElementEncoder
#help(ArgumentParser.add_argument)

class DiskUsage(object):

    def __init__(self):
        parser = ArgumentParser()

        # parser.add_argument("-h", "--help", default=False,
        #                      action='help',
        #                      help="Display help")
        parser.add_argument("-f", "--file", default="~/du.data",
                            dest="file", action="store",
                            help="File to store data, default:%(default)s",
                            metavar="filename")

        parser.add_argument("-p", "--print", default=False,
                            action="store_true", dest="display",
                            help="Display computed data, default:%(default)s")
        parser.add_argument("-d", "--dir", default=["./"], dest="directories",
                            nargs="+", metavar="directory",
                            help="Directories to process, recursively,"+
                            " default:%(default)s")
        parser.add_argument("-c", "--compute", default=False,
                            action="store_true", dest="compute", help=
                            "Compute data, default:%(default)s")

        parser.add_argument("-v", "--verbose", default=False,
                            action="store_true", dest="verbose",
                            help="Be verbose")
        self.args = parser.parse_args()

    def run(self):
        #main entry point

        #start by computing data
        if self.args.compute:
            sizeElts = [SizeElement(directory) for directory in self.args.directories]
            SizeData(sizeElts, self.args.file).write()
        #...

        for e in sizeElts:
            e.display()



class SizeData(dict):
    """ Data processed."""

    def __init__(self, sizeElts, datafile):
        dict.__init__(self)
        self.datafile=os.path.expanduser(datafile)
        self.size_elements=sizeElts

    def write(self):
        print "Writing in {}".format(self.datafile)
        with open(self.datafile, 'w') as f:
            f.write(json.dumps(self.size_elements, cls=SizeElementEncoder))
        print "done"



if __name__=='__main__':
    du = DiskUsage()
    du.run()
