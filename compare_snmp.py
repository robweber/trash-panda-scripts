""""
Compares one SNMP OID value to another. Values must both be integers.

Examples:

# perform (XXX - YYYY), if result between 1 and 10 = warning, if betwen 10 and 20 = critical
--oid XXX YYY --action subtract -w 1:10 -c 10:20

# perform (XXX / YYYY), if result > .8 = warning, if > .9 = critical
--oid XXX YYY --action ratio -w .80 -c .90

# same as above but threshold is < .9 and < .8
--oid XXX YYY --action ratio -w .90: -c .80:

Requires hnmp
"""
import argparse
import sys
from hnmp import SNMP, SNMPError

OK = 0
WARNING = 1
CRITICAL = 2


def get_oid(oid):
    result = None

    try:
        result = int(snmp.get(oid))
    except SNMPError:
        print(f"Could not reach server {args.host} or find given oid")
        sys.exit(WARNING)
    except TypeError:
        print(f"OID {oid} return type is not an integer")
        sys.exit(CRITICAL)

    return result


# perform the numerical action
def do_action(val1, val2, action):
    if(action == "ratio"):
        return val1/val2
    elif(action == "add"):
        return val1 + val2
    elif(action == "substract"):
        return val1 - val2

    return 0


# https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT
def do_comparison(value, threshold):
    result = False
    # can start with @ to be inclusive range
    inclusive = False
    if(threshold[0] == "@"):
        threshold = threshold[1]
        inclusive = True

    if(":" in threshold):
        split = threshold.split(":")
        if(split[0] and split[1]):
            # use this as a range
            if(inclusive):
                result = value >= float(split[0]) and value <= float(split[1])
            else:
                result = value < float(split[0]) or value > float(split[1])
        elif(split[0]):
            # less than value given
            result = value < float(split[0])
        else:
            # greater than value given
            result = value > float(split[1])
    else:
        # it's a straight comparison
        result = value < 0 or value > float(threshold)

    return result


# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', required=True, help='The host address')
parser.add_argument('-C', '--community', required=True, help='The community string')
parser.add_argument('-o', '--oid', nargs=2, required=True,
                    help='The 2 OIDs to compare')
parser.add_argument("-a", "--action", type=str, choices=("ratio", "add", "subtract"), required=False, default="ratio",
                    help="The comparison action to use, ratio by default")
parser.add_argument("-w", "--warning", type=str, required=False,
                    help="The warning range or threshold (start <= end or start:end or ~:end")
parser.add_argument("-c", "--critical", type=str, required=False,
                    help="The critical range or threshold (start <= end or start:end or ~:end")

args = parser.parse_args()

# setup the snmp object
snmp = SNMP(args.host, community=args.community)

# run the action
result = do_action(get_oid(args.oid[0]), get_oid(args.oid[1]), args.action)
print(f"{result}")

# do the comparison
return_code = OK
if(args.warning and do_comparison(result, args.critical)):
    return_code = CRITICAL
elif(args.critical and do_comparison(result, args.warning)):
    return_code = WARNING

sys.exit(return_code)
