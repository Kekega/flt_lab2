# # import re
# #
# # def is_cf_rule(rule):
# #     # Check if a rule is in the form A -> BC or A -> a
# #     m = re.match(r'([A-Z]+) -> ([A-Z] [A-Z])|([a-z])', rule)
# #     return bool(m)
# #
# # def is_rl_rule(rule):
# #     # Check if a rule is in the form A -> aB or A -> a
# #     m = re.match(r'([A-Z]+) -> ([a-z] [A-Z])|([a-z])', rule)
# #     return bool(m)
# #
# # # Read the input file
# # with open('input.txt', 'r') as f:
# #     lines = f.readlines()
# #
# # # Separate the context-free and right-linear rules
# # cf_rules = []
# # rl_rules = []
# # for line in lines:
# #     if line.startswith('<rule>'):
# #         cf_rules.append(line.strip())
# #     elif line.startswith('<PR-rule>'):
# #         rl_rules.append(line.strip())
# #
# # # Find the intersection of the two grammars
# # intersection = []
# # for rule in cf_rules:
# #     if is_rl_rule(rule):
# #         intersection.append(rule)
# #
# # for rule in rl_rules:
# #     if is_cf_rule(rule):
# #         intersection.append(rule)
# #
# # # Remove non-generative and unattainable nonterminals
# # terminals = set()  # Set of terminal symbols
# # generative = set()  # Set of generative nonterminal symbols
# # for rule in intersection:
# #     m = re.match(r'([A-Z]+) -> ([A-Z] [A-Z])|([a-z])', rule)
# #     if m.group(3):  # Rule is of the form A -> a
# #         terminals.add(m.group(3))
# #         generative.add(m.group(1))
# #     else:  # Rule is of the form A -> BC
# #         generative.add(m.group(1))
# #         generative.add(m.group(2))
# #         generative.add(m.group(3))
# #
# # # Remove non-generative and unattainable nonterminals from the intersection
# # filtered_intersection = []
# # for rule in intersection:
# #     m = re.match(r'([A-Z]+) -> ([A-Z] [A-Z])|([a-z])', rule)
# #     if m.group(3) or m.group(1) in generative:
# #         filtered_intersection.append(rule)
# #
# # # Print the filtered intersection
# # print(filtered_intersection)
#
# # Build the Non-Contiguous Context-Free Automaton (NCA) for the filtered intersection grammar using the standard algorithm
#
# from collections import defaultdict
#
# def cfg_to_nca(cfg):
#     # Create an empty NCA
#     nca = defaultdict(list)
#     nca['start'] = ['start']
#     nca['final'] = []
#
#     # Create a start state and mark it as the current state
#     current_state = 'start'
#
#     # Process each rule in the CFG
#     for rule in cfg:
#         # Split the rule into a left-hand side and a right-hand side
#         lhs, rhs = rule.split(' -> ')
#
#         # If the right-hand side is the empty string, add an epsilon transition
#         # from the current state to a new final state
#         if not rhs:
#             final_state = f'final_{len(nca["final"])}'
#             nca[current_state].append((final_state, 'epsilon'))
#             nca['final'].append(final_state)
#         else:
#             # Split the right-hand side into a list of symbols
#             symbols = list(rhs)
#
#             # Process each symbol in the right-hand side
#             for symbol in symbols:
#                 # If the current state is a final state, create a new non-final state
#                 if current_state in nca['final']:
#                     new_state = f'nonfinal_{len(nca)}'
#                 else:
#                     new_state = current_state
#
#                 # Add a transition from the current state to the new state with the symbol as the label
#                 nca[current_state].append((new_state, symbol))
#                 current_state = new_state
#
#                 # If the current state is not a final state and the right-hand side is not the empty string,
#                 # mark the current state as a final state
#                 if current_state not in nca['final']:
#                     nca['final'].append(current_state)
#
#     return nca
#
# # Example CFG
# cfg = [
#     'S -> aSb',
#     'S -> bSa',
#     'S -> a',
#     'S -> b'
# ]
# # Convert the CFG to an NCA
# nca = cfg_to_nca(cfg)
# # Print the NCA
# print(nca)

from parser import read_input

# rules = ["g", "[S]", "[A]", "c", "[y]"]
# for r in rules_iterator(rules):
#     print(r)

read_input("input.txt")

