#!/usr/bin/python

def _direct_followers(log, sort=True):
    ds = []
    for trace in log:
        for index,event in enumerate(trace):
            if index != len(trace)-1:
                if (event, trace[index+1]) not in ds:
                    ds.append((event, trace[index+1]))
    return ds

def _causalities(seen, df):
    cs = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in cs:
                if (event, event2) in df and (event2,event) not in df:
                    cs.append((event, event2))
    return cs

def _no_causalities(seen, df):
    cs = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in cs:
                if (event, event2) not in df and (event2,event) not in df:
                    cs.append((event, event2))
    return cs

def _parallels(seen, df):
    par = []
    for event in seen:
        for event2 in seen:
            if (event, event2) not in par:
                if (event, event2) in df and (event2,event) in df:
                    par.append((event, event2))
    return par

def build_footprint(log):
    """
    Build footprint, first list is all activities (Tl)
    second one is list of direct followers
    third is causalities
    forth is no causalities
    fifth is parallels
    """
    seen = [item for sub in log for item in sub]
    df = _direct_followers(log)
    cs = _causalities(seen, df)
    ncs = _no_causalities(seen, df)
    par = _parallels(seen, df)
    return set(seen), df, cs, ncs, par


def _check_set(A,ncs):
    for event in A:
        for event2 in A:
            if (event, event2) not in ncs:
                return False
    return True

def _check_outsets(A,B, cs):
    for event in A:
        for event2 in B:
            if (event, event2) not in cs:
                return False
    return True


def get_Xl(log, seen, cs, ncs):
    import itertools
    xl = set()
    subsets = set()
    for i in range(1,len(seen)):
        for s in itertools.combinations(seen, i):
            subsets.add(s)
    for a in subsets:
        reta = _check_set(a, ncs)
        for b in subsets:
            retb = _check_set(b, ncs)
            if reta and retb and _check_outsets(a,b,cs):
                print((a,b))
                xl.add((a,b))
    return xl

def get_Yl(xl):
    import copy
    yl = copy.deepcopy(xl)
    for a in xl:
        A = a[0]
        B = a[1]
        for b in xl:
            if set(A).issubset(b[0]) and set(B).issubset(b[1]):
                if a!=b:
                    yl.discard(a)
    return yl


def get_Ti(log):
    ti = set()
    [ti.add(event[0]) for event in log]
    return ti

def get_To(log):
    to = set()
    [to.add(event[-1]) for event in log]
    return to




