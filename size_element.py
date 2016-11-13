from json import JSONEncoder
import os
import time

class SizeElement():

    def __init__(self, directory):
        #discover tree
        from os.path import join, getsize
        for root, dirs, files in os.walk(directory):
            self.time=time.time()
            self.path=root
            self.abs_path=os.path.abspath(root)
            self.sizefiles=sum(getsize(join(root, name)) for name in files)
            self.countfiles=len(files)
            self.sub_elements=[SizeElement(subdir) for subdir in dirs]
            break

    def display(self):
        print "{} :".format(self.abs_path)
        print "\tsize : {}o in {} file(s)".format(self.sizefiles,self.countfiles)
        print "\t{} directory(ies)".format(len(self.sub_elements))


class SizeElementEncoder(JSONEncoder):

    # def __init__(self):
    #     JSONEncoder.__init__(self)

    def default(self, o):
        print ".",
        if not isinstance(o,SizeElement):
            return JSONEncoder.default(self, o)
        return o.__dict__
        # encoded = """
        #     \{"root":"{root}",
        #       "abs_path":"{abs_path}",
        #       "time":{time},
        #       "sizefiles":{sizefiles},
        #       "countfiles":{countfiles},
        #       "sub_elements":
        #       [
        # """
        # for el in o.sub_elements:
        #     encoded.append(self.default(el))
        #     encoded.append(',')
        # encoded.append("]\}")
        # return encoded
