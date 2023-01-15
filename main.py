from parser import read_input
from intersection import find_intersection

if __name__ == "__main__":
    c, d = read_input("input.txt")

    print(c, d, sep="\n")

    print(find_intersection(c, d))
    # for rule in c.rules:
        # print(type(rule))


