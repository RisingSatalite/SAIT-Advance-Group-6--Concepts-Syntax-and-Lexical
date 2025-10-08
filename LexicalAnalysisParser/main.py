# Main
from lexical_parser import tokenize, Parser
from pprint import pprint


# Main function to take user input

def run_parser():
    print("Enter your code (end with a blank line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    code = "\n".join(lines)

    try:
        tokens = tokenize(code)
        print("\nTOKENS:")
        pprint(tokens)

        parser = Parser(tokens)
        tree = parser.parse_program()

        print("\nPARSE TREE:")
        pprint(tree)

    except (SyntaxError, RuntimeError) as e:
        print(f"\n Error: {e}")


if __name__ == "__main__":
    run_parser()
