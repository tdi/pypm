
from simple_logs import read
from footprint import build_footprint, get_Ti, get_To, get_Xl,get_Yl
import sys


def main(argv):
    log = read(argv[1])
    print("LOG %s : %s" % (argv[1], log))
    print("Footprint:\nTl %s\n>  %s\n-> %s\n#  %s\n|| %s" % build_footprint(log))
    seen, df, cs, ncs, par = build_footprint(log)
    print("Ti %s" % get_Ti(log))
    print("To %s" % get_To(log))
    xl = get_Xl(log,seen, cs, ncs)
    print("Xl %s" % xl )
    print("Yl %s" % get_Yl(xl))



if __name__ == "__main__":
    main(sys.argv)
