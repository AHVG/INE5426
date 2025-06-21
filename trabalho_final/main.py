import sys
import argparse

from src.compiler import Compiler


def main():
    parser = argparse.ArgumentParser(description="Compile source code using the Compiler.")
    parser.add_argument('--program', type=str, help='Source code passed as string')
    parser.add_argument('--file', type=str, help='Path to file containing source code')

    args = parser.parse_args()

    if args.program:
        program = args.program

    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                program = f.read()
        except Exception as e:
            print(f"Failed to read file '{args.file}': {e}")
            sys.exit(1)

    else:
        print("Error: You must provide either --program or --file")
        parser.print_help()
        sys.exit(1)

    compiler = Compiler()
    compiler.compile(program)

if __name__ == "__main__":
    main()