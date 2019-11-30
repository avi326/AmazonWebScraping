import sys
import os

REQUIRED_NUM_OF_ARGS = 3
ARG_OPTION = 1
ARG_FILE_NAME = 2
PRINT = -1

"""
////////////  USING ARGV

if len(sys.argv) != REQUIRED_NUM_OF_ARGS:
    print("usage: ./FILE.py {-quary |-a} file")
    sys.exit(1)

option = sys.argv[ARG_OPTION]
try:
    filename = sys.argv[ARG_FILE_NAME]
except:
    print("Input file doesn't exist, please check and run again...")
if option == "-all":
    print(...)

elif option == "-player":
    print(...)
elif option == "-team":
    print(...)
elif option == "-league":
    print(...)
elif option == "-country":
    print(...)

else:
    print("unknown option: " + option)
    sys.exit(1)
    
    
"""
"""
////////////  USING ARGPARSE


def SB_summary(name, query):

    func_dict = {'country': country,
                 'league': league,
                 'team': team,
                 'player': player,


    return func_dict[query](name)[PRINT]


    # Parse arguments
    
    parser = argparse.ArgumentParser(description="Print SB stats from command")
    parser.add_argument('query", help="choose which question you like to check", choices=
                        {'country', 'league', 'team', 'player'}
    parser.add_argument("name", help="Print Summary File for arg", action="store_true")
    parser.add_argument("-a", help="Print Summary File", action="store_true")
    args = parser.parse_args()

    if args.a or not args.query:
        qs = ['country', 'league', 'team', 'player']
        for q in qs:
            print(SB_summary(args, q))
    else:
        try:
            result = SB_summary(args.query)
            print(result)
        except:
            print("usage: ./FILE.py {query] | -a}")

"""

