from copy import deepcopy

from cfg.rule import Rule, Term, Nterm, Epsilon
import uuid

class CFG():
    def __init__(self, rules_set):
        self.rules = rules_set
        self.terms = self.get_terms(rules_set)
        self.nterms = self.get_nterms(rules_set)

        self.start = Nterm('[S]')
        self.buid_dependency_graph()

    # извлекает список всех термов из множества правил КСГ
    # используется в конструкторе
    # не изменяет объект
    def get_terms(self, rules_set):
        terms_set = set()
        for rule in rules_set:
            rule_list = [rule.left] + rule.rights
            for tnt in rule_list:
                if isinstance(tnt, Term):
                    terms_set.add(tnt)
        return terms_set

    # извлекает список всех гетермов из множества правил КСГ
    # используется в конструкторе
    # не изменяет объект
    def get_nterms(self, rules_set):
        nterms_set = set()
        for rule in rules_set:
            rule_list = [rule.left] + rule.rights
            for tnt in rule_list:
                if isinstance(tnt, Nterm):
                    nterms_set.add(tnt)
        return nterms_set

    def __repr__(self):
        return '\n'.join(map(str, self.rules))

    # Строит граф зависимостей в КСГ
    # используется в конструкторе
    # не изменяет объект
    def buid_dependency_graph(self):
        child_relations = {}
        parent_relations = {}
        for rule in self.rules:
            left = rule.left
            rights = list(filter(lambda x: isinstance(x, Nterm), rule.rights))

            if left not in child_relations:
                child_relations[left] = set(rights)
            else:
                child_relations[left].update(rights)

            for right in rights:
                if right not in parent_relations:
                    parent_relations[right] = set([left])
                else:
                    parent_relations[right].add(left)

        self.child_relations = child_relations
        self.parent_relations = parent_relations

        return self

    # Удаляет из списка правил rules все нетерминалы,
    # которых нет ни в одной левой части
    # не меняет объект

    def remove_nterms_that_dont_present_at_left(self, rules):
        presenting_nterms = set()
        new_rules = set()
        for rule in rules:
            presenting_nterms.add(rule.left)
        for rule in rules:
            new_right = []
            for right in rule.rights:
                if (isinstance(right, Term) or isinstance(right, Nterm) and right in presenting_nterms):
                    new_right.append(right)
            if (len(new_right) == 0):
                new_right.append(Epsilon())
            new_rules.add(Rule(rule.left, new_right))
        return new_rules

    # Создает новый объект, в правилах которого удалены недостижимые нетермы

    def remove_unreachable_symbols(self):
        # скажем, что стартовый символ достижим
        self.reachable = set([self.start])
        # про остальные пока не понятно
        unallocated = self.nterms.difference(self.reachable)

        while True:
            upow = len(unallocated)

            unallocated_copy = deepcopy(unallocated)
            for nterm in unallocated_copy:
                # если у трема есть родитель и этот родитель достижим, значит терм достижим
                if nterm in self.parent_relations and set(self.parent_relations[nterm]) & self.reachable:
                    # то пересаживаем его к достижимым
                    self.reachable.add(nterm)
                    unallocated.remove(nterm)

            new_upow = len(unallocated)

            if new_upow == upow:
                break

        new_rules = set(filter(
            lambda x: x.left in self.reachable,
            self.rules
        ))

        return CFG(new_rules)

    # Удаление eps-правил из грамматики
    # Создает новый объект

    def remove_epsilon_rules(self):
        new_rules = deepcopy(self.rules)
        new_rules = self.remove_rules_with_only_eps_right(new_rules)
        self._find_collapsing()
        if (self.start in self.collapsing):
            new_rules.add(Rule(Nterm("[S]"), [Epsilon()]))

        new_rules = new_rules.union(
            self._gen_all_possible_combinations_of_rules(new_rules))
        new_rules = self.remove_rules_with_only_eps_right(
            self.remove_nterms_that_dont_present_at_left(new_rules))
        if (self.start in self.collapsing):
            new_rules.add(Rule(Nterm("[S]"), [Epsilon()]))
        return CFG(new_rules)

    # Удаляет из списка правил те, у которых в правой части только eps
    # Возвращает новый список, старый не меняет
    # Нужна для удаления eps-правил

    def remove_rules_with_only_eps_right(self, rules):
        new_rules = set()
        for rule in rules:
            if (all(map(lambda x: isinstance(x, Epsilon), rule.rights))):
                continue
            new_rules.add(deepcopy(rule))
        return new_rules

    # Генерирует новые правила
    # Нужная для удаления eps-правил
    # Не меняет объект
    def _gen_all_possible_combinations_of_rules(self, rules):
        combinations = set()
        for rule in rules:
            if any(map(lambda x: x in self.collapsing, rule.rights)):
                right_comb = self._gen_right_side_combinations(
                    rule.rights, [], 0)
                for comb in right_comb:
                    combinations.add(Rule(rule.left, comb))
        return combinations

    # Нужна для _gen_all_possible_combinations_of_rules
    # Не меняет объект
    def _gen_right_side_combinations(self, right, current_c, current_i):
        if (current_i == len(right)):
            if (all(map(lambda x: isinstance(x, Epsilon), current_c))):
                return []
            return [current_c]
        tmp = []
        if (right[current_i] in self.collapsing):
            tmp += self._gen_right_side_combinations(
                right, current_c + [Epsilon()], current_i + 1)
        tmp += self._gen_right_side_combinations(
            right, current_c + [right[current_i]], current_i + 1)
        return tmp

    # Ищет нетермы, которые МОГУТ раскрыться в eps
    # Сохраняет множество таких нетермов в поле объекта collapsing
    def _find_collapsing(self):
        self.collapsing = set()
        flag = True
        tmp = deepcopy(self.rules)
        while flag:
            flag = False
            for rule in tmp:
                if (len(rule.rights) == 1 and isinstance(rule.rights[0], Epsilon)):
                    flag = True
                    self.collapsing.add(rule.left)
                    tmp.remove(rule)
                    break
                if all(map(lambda x: isinstance(x, Nterm), rule.rights)) and all(
                        map(lambda x: x in self.collapsing, rule.rights)):
                    self.collapsing.add(rule.left)
                    flag = True
                    tmp.remove(rule)
                    break
        return self

    # Возвращает грамматику в нормальной форме Хомского
    # Возвращает новый объект, старый не меняет
    def toCNF(self):
        return self.remove_long_rules().remove_epsilon_rules().remove_chain_rules().remove_useless_rules().several_nonterm_removal()

    # Удаляет цепные правила из грамматики
    # Возвращает новый объект

    def remove_chain_rules(self):
        self._find_chain_rules()
        chainrules = self.ChR
        if len(self.nterms) == len(chainrules):
            return self
        rules = set()
        for rule in self.rules:
            left = rule.left
            rights = rule.rights
            if len(rights) == 1 and type(rights[0]) == Nterm and [left.name, rights[0].name] in chainrules:
                pass
            else:
                rules.add(rule)
        copy_rules = deepcopy(rules)
        for ch in chainrules:
            for rule in copy_rules:
                left = rule.left
                rights = rule.rights
                if ch[1] == left.name:
                    rules.add(Rule(Nterm(ch[0]), rights))
        return CFG(rules)

    # Возвращает множество цепных правил
    # Нужен remove_chain_rules
    # Сохраняет их в поле объекта ChR
    def _find_chain_rules(self):
        chainrules = []
        for nterm in self.nterms:
            chainrules.append([nterm.name, nterm.name])
        while True:
            upow = len(chainrules)
            for rule in self.rules:
                left = rule.left
                rights = rule.rights
                if len(rights) == 1 and type(rights[0]) == Nterm:
                    r = rights[0]
                    for ch in chainrules:
                        if ch[1] == left.name:
                            pair = [ch[0], r.name]
                            if not pair in chainrules:
                                chainrules.append(pair)
            new_upow = len(chainrules)
            if upow == new_upow:
                break
        self.ChR = chainrules

    # Возвращает новый объект без бесполезных правил
    def remove_useless_rules(self):
        return self.remove_nongenerating_rules().remove_unreachable_symbols()

    def several_nonterm_removal(self):
        def create_unique_str():
            return f"[U{uuid.uuid4().hex[:2].upper()}]"

        rules = set()
        new_rules = []
        to_symbol = {}
        for rule in self.rules:
            left = rule.left
            rights = rule.rights
            if len(rights) == 1 or all(map(lambda x: isinstance(x, Nterm), rights)):
                new_rules.append(rule)
                continue
            rights_new = []
            for r in deepcopy(rights):
                if isinstance(r, Term):
                    if not r.symbol in to_symbol.keys():
                        new_nterm = create_unique_str()
                        to_symbol[r.symbol] = new_nterm
                        new_rules.append(
                            Rule(Nterm(new_nterm), [Term(r.symbol)]))
                        rights_new.append(Nterm(new_nterm))
                    else:
                        rights_new.append(Nterm(to_symbol[r.symbol]))
                else:
                    rights_new.append(r)
            new_rules.append(Rule(left, rights_new))
        return CFG(new_rules)

    # Возвращает новый объект, в котором удалены "длинные правила"
    def remove_long_rules(self):
        new_rules = set()
        for rule in self.rules:
            if len(rule.rights) > 2:
                new_rules = new_rules.union(self._split_long_rule(rule))
            else:
                new_rules.add(deepcopy(rule))
        return CFG(new_rules)

    # Возвращает множество правил, в котором "длинные правила" разделены на несколько
    # Нужна для remove_long_rules
    def _split_long_rule(self, rule):
        new_rules = set()
        current_nterm = deepcopy(rule.left)
        new_nterm = Nterm("[U" + uuid.uuid4().hex[:3].upper() + "]")
        for i in range(len(rule.rights) - 2):
            new_rules.add(Rule(current_nterm, [rule.rights[i], new_nterm]))
            current_nterm = new_nterm
            new_nterm = Nterm("[U" + uuid.uuid4().hex[:3].upper() + "]")
        new_rules.add(Rule(current_nterm, [rule.rights[-2], rule.rights[-1]]))
        return new_rules

    # Возвращает новый объект, в котором удалены nonegenerating правила
    # (nongenerating - непораждающие. Для них в правой части всегда стоит хотя бы один нетерминал)
    def remove_nongenerating_rules(self):
        genetaring_nterm = set()
        for rule in self.rules:
            left = rule.left
            rights = rule.rights
            if all(map(lambda x: isinstance(x, Term), rights)):
                genetaring_nterm.add(left.name)
        while True:
            upow = len(genetaring_nterm)
            for rule in self.rules:
                left = rule.left
                rights = rule.rights
                flag = True
                for r in rights:
                    if isinstance(r, Nterm) and not r.name in genetaring_nterm:
                        flag = False
                        break
                if flag:
                    genetaring_nterm.add(left.name)

            new_upow = len(genetaring_nterm)
            if upow == new_upow:
                break
        new_rules = []
        for rule in self.rules:
            rights = rule.rights
            if any(map(lambda x: isinstance(x, Nterm) and not x.name in genetaring_nterm, rights)):
                continue
            new_rules.append(rule)
        return CFG(new_rules)
