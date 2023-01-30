from cfg.parser import CFG_Parser
from cfg.cfg import CFG

from dfa.dfa import DFA, Edge


def read_input(input_filename):
    with open(input_filename, "r", encoding="utf-8") as inp:
        rules = inp.readlines()

    rules = list(filter(lambda item: item.strip(), rules))

    it = rules_iterator(rules)

    s = ""
    for rule in it:
        if rule == 0:
            break
        nonterm, r = rule.split("->")
        nonterm = nonterm.strip()

        se = r.split("|")

        for r in se:
            s += nonterm + "->" + r.strip() + "\n"

    a = CFG_Parser(s)
    cfff = a.parse_rules().toCNF()
    # получили cfg в нормальной форме Хомского

    # считаем терминальные состояния
    ttt = []
    for rule in it:
        if rule == 0:
            break
        nonterm, r = rule.split("->")

        se = r.split("|")

        for k in se:
            ttt.append(f"{nonterm} -> {k.strip()}")

    c = 0
    for rule in ttt:
        nonterm, r = rule.split("->")
        if len(r.strip()) == 1:
            c += 1
            fin = nonterm.strip()

    # если их нет
    if c == 0:
        raise ValueError("неверный формат праволинейной грамматики")
    # если терминальное состояние единственное
    if c == 1:
        final_state = f"{fin}"
        states = {f"{fin}"}
        edges = set()
        for rule in ttt:
            nonterm, r = rule.split("->")
            st_from = nonterm.strip()
            states.add(st_from)

            r = r.strip()
            sym = r[0]
            r = r[1:]
            st_to = r if r else f"{fin}"
            states.add(st_to)
            e = Edge(st_from, st_to, sym)
            edges.add(e)
    # если их несколько добавляем новое F0, которое будет единственным финальным в итоговом DFA
    else:
        final_state = "[F0]"
        states = {"[F0]"}
        edges = set()

        for rule in ttt:
            if rule == 0:
                break
            nonterm, r = rule.split("->")
            st_from = nonterm.strip()
            states.add(st_from)

            se = r.split("|")

            for r in se:
                r = r.strip()
                sym = r[0]
                r = r[1:]
                st_to = r if r else "[F0]"
                states.add(st_to)
                e = Edge(st_from, st_to, sym)
                edges.add(e)

    dfa = DFA(states, edges, final_state)

    return cfff, dfa


def rules_iterator(rules: list[str]):
    rules = rules[1:]
    for row in rules:
        ret = row.strip()
        if ret[0] != "[":
            yield 0
        else:
            yield ret
