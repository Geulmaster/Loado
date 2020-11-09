import argparse
import sys
from Loado.app import change_config_file
from Loado.app.core import flow

class Parser:
    def run_arguments(self):
        global args, parser
        parser = argparse.ArgumentParser(description="Load test your app")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        group.add_argument("-q", "--quiet", action="store_true")
        parser.add_argument("-hn", "--host", help="Set host target")
        parser.add_argument("-p", "--port", help="Set target's port")
        parser.add_argument("-r", "--route", help="Set target's route")
        parser.add_argument("run", nargs='?', help='Run command')
        parser.add_argument("type", nargs='?', help="The load tests web request type")
        args = parser.parse_args()
        return args

def runner():
    if len(sys.argv) < 2:
        print(parser.print_help())
    args_list = ["args.host", "args.port", "args.route"]
    for arg in args_list:
        if eval(arg):
            change_config_file(arg[5:], eval(arg)) # Change the configuration file value
            print(f"{arg[5:]} is set to {eval(arg)}")
    if args.run == "run":
        if args.type:
            try:
                print(f"Requests type is {args.type}")
                method = getattr(flow, args.type)
                method()
            except AttributeError:
                print(f"{args.type} requests are not supported")
    sys.exit()

if __name__ == '__main__':
    parser = Parser()
    parser.run_arguments()
    runner()