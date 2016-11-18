#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os

import json

#app imports
from size_element import SizeElement
from size_element import SizeElementEncoder
#help(ArgumentParser.add_argument)

class Display(object):
    def __init__(self, size_data):
        index=1
        keys={}

        for sizeel in size_data.size_elements:
            keys[index]=sizeel

        self.display(keys)

    def display(self, keys):
        for (index, sizeel) in keys.iteritems():
            print index, sizeel

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
        if self.args.verbose:
            print self.args.__dict__


        #start by computing data
        if self.args.compute:
            sizeElts = [SizeElement(directory=directory, compute=self.args.compute, verbose=self.args.verbose) for directory in self.args.directories]
            sd = SizeData(sizeElts, self.args.file).write()
        #Display data
        if self.args.display:
            # First read data
            sd = SizeData(None, self.args.file, verbose=self.args.verbose).read()

            if self.args.verbose:
                print "sd : {}".format(sd)
            #Data should be ready, start intercative display
            Display(sd)

class SizeData(object):
    """ Data processed."""

    def __init__(self, sizeElts, datafile, verbose=False):

        self.datafile=os.path.expanduser(datafile)
        self.size_elements=sizeElts
        self.verbose=verbose

    def write(self):
        print "Writing in {}".format(self.datafile)
        with open(self.datafile, 'w') as f:
            f.write(json.dumps(self.size_elements, cls=SizeElementEncoder, indent=4, separators=(',', ': ')))
        print "done"
        return self

    def decode(self, x):
        return SizeElement(compute=False, json_input=x, verbose=self.verbose)

    def read(self):
        with open(self.datafile) as f:
            jsonData = json.load(f, object_hook=self.decode)
            self.size_elements=jsonData
        print [x.display(deep=True) for x in jsonData]
        return self

if __name__=='__main__':
    du = DiskUsage()
    du.run()
