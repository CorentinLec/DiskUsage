from argparse import ArgumentParser

#help(ArgumentParser.add_argument)

class DiskUsage(object):

    def __init__(self):
        parser = ArgumentParser()

        # parser.add_argument("-h", "--help", default=False,
        #                      action='help',
        #                      help="Display help")
        parser.add_argument("-f", "--file", default="$HOME/du.data",
                            dest="file", action="store",
                            help="file to store data", metavar="filename")

        parser.add_argument("-d", "--display", default=True,
                            action="store_true", dest="display",
                            help="display computed data")

        self.args = parser.parse_args()

if __name__=='__main__':
    du = DiskUsage()
