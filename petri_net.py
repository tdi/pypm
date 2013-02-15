

class PetriNet(object):

    def __init__(self):
        self.places = []
        self.transtions = []
        self.inputs = []
        self.outputs = []
        self.connections = {}

    def from_alpha(self,alpha_model):
        self.transitions = alpha_model.footprint.seen
        self.inputs = alpha_model.ti
        self.outputs = alpha_model.to
        self._make_structure(alpha_model.yl)

    def _make_structure(self,yl):
        for elem in yl:
            pass



