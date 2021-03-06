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
        parser.add_argument("-t", "--time", help="Set run's duration")
        parser.add_argument("-u", "--users", help="Set amount of users to simulate")
        parser.add_argument("-sp", "--spawn_rate", help="Set spawn rate of workers")
        parser.add_argument("run", nargs='?', help='Run command, should get type after it')
        parser.add_argument("type", nargs='?', help="The load tests web request type")
        args = parser.parse_args()
        return args


def runner():
    if len(sys.argv) < 2:
        print(parser.print_help())
    args_list = ["args.host", "args.port", "args.route", "args.time", "args.users", "args.spawn_rate"]
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

if __name__ == '__main__':
    parser = Parser()
    parser.run_arguments()
    runner()
    