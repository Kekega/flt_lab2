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
    start_state = "[S]"
    final_state = "[F0]"

    def __init__(self, states: set[str], edges: set[Edge], final_state="[F0]"):
        self.states = states
        self.edges = edges
        self.final_state = final_state

    def add_state(self, state: str):
        self.states.add(state)

    def add_edge(self, e: Edge):
        self.edges.add(e)

    def __repr__(self):
        return "States:\n" + str(self.states) + "\n" + "Edges:\n" + str(self.edges)




