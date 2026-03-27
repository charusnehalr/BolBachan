# src/main.py
import sys
from parser import parser
from interpreter import Interpreter

def print_parse_tree(data):
    def traverse_tree(node, level=0):
        if isinstance(node, list):
            for child in node:
                traverse_tree(child, level + 1)
        elif node is not None:
            print("  " * level + str(node))

    result = parser.parse(data)
    traverse_tree(result)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.bb>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        data = f.read()
        print("Parse Tree:")
        print_parse_tree(data)

        print("\nExecution Result:")
        result = parser.parse(data)
        interpreter = Interpreter()
        interpreter.eval(result)
