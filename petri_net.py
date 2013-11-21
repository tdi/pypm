

class PetriNet(object):

    def __init__(self):
        self.places = []
        self.transtions = []
        self.inputs = []
        self.outputs = []
        self.connections = {}

    def from_alpha(self,alpha_model, dotfile="dot.dot"):
        self.transitions = alpha_model.footprint.seen
        self.inputs = alpha_model.ti
        self.outputs = alpha_model.to
        dot = self._make_structure(alpha_model.yl, alpha_model.ti, alpha_model.to)
        with open(dotfile, "w") as f:
            f.write(dot)


    def _make_structure(self,yl,ti,to):
        dot = []
        dot.append("digraph pn {")
        dot.append("rankdir=LR;")
        for elem in yl:
            for i in elem[0]:
                dot.append('"%s" -> "P(%s)";' % (i, elem))
                dot.append('"%s" [shape=box];' % i)
                dot.append('"P(%s)" [shape=circle];' % str(elem))
            for i in elem[1]:
                dot.append('"P(%s)" -> "%s";' % (elem, i))
                dot.append('"%s" [shape=box];' % i)
        for i in ti:
            dot.append('in -> "%s";' % i)
        for o in to:
            dot.append('"%s" -> out ;' % o)


        dot.append("}")
        dot = "\n".join(dot)
        return dot






