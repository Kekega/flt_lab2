from cfg.parser import CFG_Parser
from cfg.cfg import CFG

# class element:
#     def __init__(self, sym: str, isTerm: bool):
#         self.sym = sym
#         self.isTerm = isTerm

def read_input(input_filename):
    with open(input_filename, "r", encoding="utf-8") as inp:
        rules = inp.readlines()

    CFG_rules = []
    Rigth_rules = []

    it = rules_iterator(rules)

    s = ""
    for rule in it:
        if rule == 0:
            break
        nonterm, r = rule.split("->")
        nonterm = nonterm.strip()

        # print(nonterm)

        se = r.split("|")

        for t in se:
            s += nonterm + "->" + t.strip() + "\n"
            # rul = []
            # t1 = t.strip()
            # while t1:
            #     ppp = t1[0]
            #     if ppp == "[":
            #         nont, t1 = add_nont_to_cfg(t1)
            #         rul.append(element(nont, False))
            #     else:
            #         rul.append(element(ppp, True))
            #         t1 = t1[1:]

    a = CFG_Parser(s)
    c = a.parse_rules().toCNF()
    # получили cfg в нормальной форме Хомского

    for rule in it:
        print(rule)

# def add_nont_to_cfg(t1: str):
#     ind = t1.find("]")
#     nont = t1[1:ind]
#     t1 = t1[ind+1:]
#     return nont, t1



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
