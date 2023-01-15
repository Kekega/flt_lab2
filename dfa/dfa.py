class Edge:
    e_from: str
    e_to: str
    sym: str

    def __init__(self, e_from: str, e_to: str, sym: str):
        self.e_from = e_from
        self.e_to = e_to
        self.sym = sym

    def __repr__(self):
        l = [self.e_from, self.e_to, self.sym]
        # print(l)
        return "[" + ", ".join(l) + "]"

class DFA:
    def __init__(self, states: set[str], edges: set[Edge]):
        self.states = states
        self.edges = edges

    def add_state(self, state: str):
        self.states.add(state)

    def add_edge(self, e: Edge):
        self.edges.add(e)

    def __repr__(self):
        return str(self.states) + "\n" + str(self.edges)




