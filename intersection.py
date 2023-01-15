from cfg.cfg import CFG
from cfg.rule import Rule, Term, Nterm, Epsilon
from dfa.dfa import DFA, Edge
from pprint import pprint


class ScalObj:
    def __init__(self, p, Nont, q):
        self.p = p
        self.Nont = Nont
        self.q = q

    def __str__(self):
        j = ", ".join([self.p, str(self.Nont), self.q])
        return "<" + j + ">"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.p) + hash(self.Nont) + hash(self.q)

    def __eq__(self, o):
        return isinstance(o, ScalObj) and self.p == o.p and self.Nont == o.Nont and self.q == o.q


class IntersectionRule:
    def __init__(self, left: ScalObj, right: list[ScalObj | str]):
        self.left = left
        self.right = right

    def __str__(self):
        r = "".join(map(str, self.right))
        return str(self.left) + " -> " + r

    def __repr__(self):
        return self.__str__()


def find_intersection(cfg: CFG, dfa: DFA):
    intersection: set[IntersectionRule] = set()

    first_set_nont = set()
    rules: set[Rule] = set()

    # Сначала породим терминальные правила
    for rule in cfg.rules:
        if len(rule.rights) == 1:
            first_set_nont.add(rule.left)
            for trans in dfa.edges:
                if trans.sym == rule.rights[0].symbol:
                    obj = ScalObj(trans.e_from, rule.left, trans.e_to)
                    new_rule = IntersectionRule(obj, [trans.sym])
                    intersection.add(new_rule)
        else:
            rules.add(rule)
    # вроде породили

    terminal_only_nonterms = set()
    for nont in first_set_nont:
        for r in rules:
            if r.left == nont:
                break
        else:
            terminal_only_nonterms.add(nont)
    term_rules = intersection.copy()

    # По каждому правилу A -> A1..An из cfg строим правила
    # <p,A,q> -> <p,A,q1><q1,A,q> для всех возможных p,q,q1
    for rule in rules:
        for p in dfa.states:
            for q in dfa.states:
                for q1 in dfa.states:
                    s1 = ScalObj(p, rule.left, q)
                    s2 = ScalObj(p, rule.rights[0], q1)
                    s3 = ScalObj(q1, rule.rights[1], q)
                    if not rule_legit([s1, s2, s3], terminal_only_nonterms, term_rules):
                        continue

                    int_rule = IntersectionRule(s1, [s2, s3])
                    intersection.add(int_rule)

    # тут почистим
    start = ScalObj(dfa.start_state, Nterm("[S]"), dfa.final_state)
    result = find_result(intersection, start)
    return result


def find_result(intersection, start):
    final_scals = {start}
    final_intersection = set()
    flag = True  # мы добавляли правило на прошлой итерации?
    while flag:
        flag = False
        r = None
        for rule in intersection:
            if rule.left in final_scals:
                flag = True
                if len(rule.right) == 2:
                    final_scals.add(rule.right[0])
                    final_scals.add(rule.right[1])
                r = rule
                break
        if r:
            final_intersection.add(r)
            intersection.remove(r)
    return final_intersection


def rule_legit(objs: list[ScalObj], terminal_only_nonterms, term_rules):
    for obj in objs:
        if obj.Nont not in terminal_only_nonterms:
            continue
        f = True
        for rule in term_rules:
            if obj == rule.left:
                f = False
                break
        if f:
            return False
    return True
