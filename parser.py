from cfg.parser import CFG_Parser
from cfg.cfg import CFG

from dfa.dfa import DFA, Edge


def read_input(input_filename):
    with open(input_filename, "r", encoding="utf-8") as inp:
        rules = inp.readlines()

    it = rules_iterator(rules)

    s = ""
    for rule in it:
        if rule == 0:
            break
        nonterm, r = rule.split("->")
        nonterm = nonterm.strip()

        se = r.split("|")

        for t in se:
            s += nonterm + "->" + t.strip() + "\n"

    a = CFG_Parser(s)
    c = a.parse_rules().toCNF()
    # получили cfg в нормальной форме Хомского

    states = set()
    edges = set()

    for rule in it:
        if rule == 0:
            break
        nonterm, r = rule.split("->")
        st_from = nonterm.strip()
        states.add(st_from)

        se = r.split("|")

        for t in se:
            t = t.strip()
            sym = t[0]
            t = t[1:]
            st_to = t if t else st_from
            states.add(st_to)
            e = Edge(st_from, st_to, sym)
            edges.add(e)

    dfa = DFA(states, edges)

    return c, dfa



def parse_cf_rule():
    ...


def parse_right_rule():
    ...


def rules_iterator(rules: list[str]):
    rules = rules[1:]
    for row in rules:
        ret = row.strip()
        if ret[0] != "[":
            yield 0
        else:
            yield ret
