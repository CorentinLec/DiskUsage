from json import JSONEncoder
import os
import time
from os.path import join, getsize

class SizeElement():

    def __init__(self, directory='.', compute=True, verbose=False, json_input=""):
        #discover tree
        if compute:
            self.computeSize( directory, verbose)
        else:
            self.decode(json_input, verbose)

    def computeSize(self, directory, verbose):
        if verbose:
            print "processing {}".format(directory)
        for root, dirs, files in os.walk(directory):
            self.time=time.time()
            self.path=root
            self.abs_path=os.path.abspath(root)
            self.sizefiles=sum(getsize(join(root, name)) for name in files)
            self.countfiles=len(files)
            if verbose:
                print "{} files, {}o, {} sudirectories : {}".format(self.countfiles, self.sizefiles, len(dirs), dirs)
            self.sub_elements=[SizeElement(join(root,subdir), True, verbose) for subdir in dirs]
            break

    def decode(self, inputData, verbose):
        if verbose:
            print "decoding {}".format(inputData["abs_path"])
        self.time=inputData["time"]
        self.path=inputData["path"]
        self.abs_path=inputData["abs_path"]
        self.sizefiles=inputData["sizefiles"]
        self.countfiles=inputData["countfiles"]
        self.sub_elements=inputData["sub_elements"]


    def display(self, deep=False):
        print "{} :".format(self.abs_path)
        print "\tsize : {}o in {} file(s)".format(self.sizefiles,self.countfiles)
        print "\t{} directory(ies)".format(len(self.sub_elements))
        if deep:
            for x in self.sub_elements:
                x.display(deep)


class SizeElementEncoder(JSONEncoder):

    # def __init__(self):
    #     JSONEncoder.__init__(self)

    def default(self, o):
        print ".",
        if not isinstance(o,SizeElement):
            return JSONEncoder.default(self, o)
        return o.__dict__
