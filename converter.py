import json
import pprint
import sys

"""
$ python2.7 converter.py <file_with_permissions>

"""


def decode(raw_rule):
    res = {}
    while len(raw_rule) > 0:
        old_rule = raw_rule[:3]
        raw_rule = raw_rule[3:]
        operator = old_rule[1]

        if operator == 'eq':
            new_rule = {old_rule[0]: old_rule[2]}
            res.update(new_rule)
        elif operator == 'in':
            new_rule = {old_rule[0]: {"$in": old_rule[2]}}
            res.update(new_rule)
        else:
            print "ERROR: Unrecognized operator:", old_rule[1]

    return res


def convert(old_object):
    res = {}

    for obj_key, obj_val in old_object.iteritems():

        if obj_val and len(obj_val) > 1:
            or_obj = []

            for obj_rule in obj_val:
                rule = decode(obj_rule)
                or_obj.append(rule)
            res[obj_key] = {"$or": or_obj}

        elif obj_val and len(obj_val) == 1:
            single_rule = obj_val[0]
            rule = decode(single_rule)
            res[obj_key] = rule
        else:
            res[obj_key] = {}

    return res


def safe_repr(object, context, maxlevels, level):
    typ = pprint._type(object)
    if typ is unicode:
        object = str(object)
    return pprint._safe_repr(object, context, maxlevels, level)

printer = pprint.PrettyPrinter()
printer.format = safe_repr


def read(permission_list):
    with open(permission_list) as f:
        for line in f:
            json_obj = json.loads(line)
            printer.pprint(convert(json_obj))
    return "Finished"


read(sys.argv[1])
