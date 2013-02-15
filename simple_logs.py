#!/usr/bin/python


def readc(filename, sep=" "):
    """
    Read file with cardinality
    """
    sl = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line =  line.split()
            if tuple(line) not in sl:
                sl[tuple(line)] = 1
            else:
                sl[tuple(line)] += 1
    return sl



def read(filename, sep=" "):
    """
    No cardinality version

    """
    sl = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line =  line.split()
            if line not in sl: sl.append(line)
    return sl


