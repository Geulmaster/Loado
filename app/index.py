import argparse

class Parser:
    def run_arguments(self):
        global args, parser
        parser = argparse.ArgumentParser(description="Load test your app")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        group.add_argument("-q", "--quiet", action="store_true")
        parser.add_argument("run", nargs='?', help='Run command')
        parser.add_argument("type", nargs='?', help="The load tests web request type")
        args = parser.parse_args()
        return args

parser = Parser()
parser.run_arguments()

if args.quiet:
    print("Done") # Will be imported from core.flow
elif args.type:
    print(f"Type is {args.type}")
else:
    print(parser.print_help())