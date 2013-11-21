
from simple_logs import read
from footprint import Alpha
from petri_net import PetriNet
import os
import sys


def main(argv):
    log = read(argv[1])
    lm = Alpha(log)
    pn = PetriNet()
    pn.from_alpha(lm, dotfile="{}.dot".format(os.path.basename(argv[1])))

if __name__ == "__main__":
    main(sys.argv)
