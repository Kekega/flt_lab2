from parser import read_input
from intersection import find_intersection
from pprint import pprint

if __name__ == "__main__":
    c, d = read_input("input.txt")

    print(c, d, sep="\n")

    pprint(find_intersection(c, d))
