
from simple_logs import read
from footprint import Alpha
from petri_net import PetriNet
import sys
import pprint


def main(argv):
    log = read(argv[1])
    lm = Alpha(log)
    print(lm)
    pn = PetriNet()
    pn.from_alpha(lm)

if __name__ == "__main__":
    main(sys.argv)
