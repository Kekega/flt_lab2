from cfg.cfg import CFG
from cfg.rule import Rule, Term, Nterm, Epsilon
from dfa.dfa import DFA, Edge

class ScalObj:
    def __init__(self, p, Nont, q):
        self.p = p
        self.Nont = Nont
        self.q = q

    def __str__(self):
        j = ", ".join([self.p, self.Nont, self.q])
        return "<" + j + ">"

    def __repr__(self):
        return self.__str__()
        # j = ", ".join([self.p, self.Nont, self.q])
        # return "<" + j + ">"

    def __hash__(self):
        return hash(self.p) + hash(self.Nont) + hash(self.q)

    def __eq__(self, o):
        return isinstance(o, ScalObj) and self.p == o.p and self.Nont == o.Nont and self.q == o.q

class IntersectionRule:
    def __init__(self, left: ScalObj, right: list[ScalObj | str]):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " -> " + str(self.right)

    def __repr__(self):
        return self.__str__()



def find_intersection(cfg: CFG, dfa: DFA):
    intersection: set[IntersectionRule] = set()
    # Сначала породим терминальные правила
    for rule in cfg.rules:
        print(rule, rule.rights, sep='\n', end='\n\n')
        if len(rule.rights) == 1:
            print(rule.rights[0], end='\n\n')
            for trans in dfa.edges:
                if trans.sym == rule.rights[0].symbol:
                    obj = ScalObj(trans.e_from, rule.left.name, trans.e_to)
                    new_rule = IntersectionRule(obj, [trans.sym])
                    intersection.add(new_rule)
    # вроде породили



    return intersection
