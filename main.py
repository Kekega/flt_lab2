from parser import read_input
from intersection import find_intersection
import argparse


def _create_pipeline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="script information")
    parser.add_argument(
        "-i", "--input_path", type=str, default="input.txt", help="path to input file"
    )
    parser.add_argument("-c", "--cfg", action=argparse.BooleanOptionalAction, help="show normalized cfg")
    parser.add_argument("-d", "--dfa", action=argparse.BooleanOptionalAction, help="show dfa")
    return parser


if __name__ == "__main__":
    parser = _create_pipeline_parser()
    args = parser.parse_args()

    c, d = read_input(args.input_path)

    if args.cfg:
        print("CFG:\n", c, sep='', end='\n\n')

    if args.dfa:
        print("DFA:\n", d, sep='', end='\n\n')

    print("INTERSECTION:", *find_intersection(c, d), sep='\n')
