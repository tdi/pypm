#!/usr/bin/python
class LogFootprint(object):
    pass

    def __str__(self):
        retlist = []
        retlist.append("Seen events: (%s)" % ",".join(map(str, self.seen)))
        retlist.append("Direct followers >: (%s)" % ",".join(map(str , self.direct_followers)))
        retlist.append("Causally dep. events ->: (%s)" % ",".join(map(str , self.causal)))
        retlist.append("Not Causally dep. events ->: (%s)" % ",".join(map(str , self.not_causal)))
        retlist.append("Parallel events ->: (%s)" % ",".join(map(str , self.parallel)))
        return "\n".join(retlist)

class Alpha(object):

    def __init__(self,log, cardinality = False):
        self.log = log
        self.footprint = self._build_footprint(self.log)
        self.xl = self._make_Xl_set()
        self.yl = self._make_Yl_set(self.xl)
        self.ti = self._make_Ti_set(self.log)
        self.to = self._make_To_set(self.log)

    def __str__(self):
        retlist = []
        retlist.append("Xl set: (%s)"% ",".join(map(str,self.xl)))
        retlist.append("Yl set: (%s)"% ",".join(map(str,self.yl)))
        retlist.append("Ti set: (%s)"% ",".join(map(str,self.ti)))
        retlist.append("To set: (%s)"% ",".join(map(str,self.to)))
        return "\n".join(retlist)

    def _direct_followers(self,log, sort=True):
        ds = []
        for trace in log:
            for index,event in enumerate(trace):
                if index != len(trace)-1:
                    if (event, trace[index+1]) not in ds:
                        ds.append((event, trace[index+1]))
        return ds

    def _causalities(self,seen, df):
        cs = []
        for event in seen:
            for event2 in seen:
                if (event, event2) not in cs:
                    if (event, event2) in df and (event2,event) not in df:
                        cs.append((event, event2))
        return cs

    def _no_causalities(self,seen, df):
        cs = []
        for event in seen:
            for event2 in seen:
                if (event, event2) not in cs:
                    if (event, event2) not in df and (event2,event) not in df:
                        cs.append((event, event2))
        return cs

    def _parallels(self,seen, df):
        par = []
        for event in seen:
            for event2 in seen:
                if (event, event2) not in par:
                    if (event, event2) in df and (event2,event) in df:
                        par.append((event, event2))
        return par

    def _build_footprint(self,log):
        """
        Build footprint, first list is all activities (Tl)
        second one is list of direct followers
        third is causalities
        forth is no causalities
        fifth is parallels
        """
        fp = LogFootprint()
        fp.seen = set([item for sub in log for item in sub])
        fp.direct_followers = self._direct_followers(log)
        fp.causal = self._causalities(fp.seen, fp.direct_followers)
        fp.not_causal = self._no_causalities(fp.seen, fp.direct_followers)
        fp.parallel = self._parallels(fp.seen, fp.direct_followers)
        return fp


    def _check_set(self,A,ncs):
        for event in A:
            for event2 in A:
                if (event, event2) not in ncs:
                    return False
        return True

    def _check_outsets(self,A,B, cs):
        for event in A:
            for event2 in B:
                if (event, event2) not in cs:
                    return False
        return True


    def _make_Xl_set(self):
        import itertools
        xl = set()
        subsets = set()
        for i in range(1,len(self.footprint.seen)):
            for s in itertools.combinations(self.footprint.seen, i):
                subsets.add(s)
        for a in subsets:
            reta = self._check_set(a, self.footprint.not_causal)
            for b in subsets:
                retb = self._check_set(b, self.footprint.not_causal)
                if reta and retb and self._check_outsets(a,b,self.footprint.causal):
                    xl.add((a,b))
        return xl

    def _make_Yl_set(self, xl):
        """ Generates Yl set """
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


    def _make_Ti_set(self,log):
        ti = set()
        [ti.add(event[0]) for event in log]
        return ti

    def _make_To_set(self,log):
        to = set()
        [to.add(event[-1]) for event in log]
        return to




