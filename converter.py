import json, pprint, sys


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


def read(permission_list):
    with open(permission_list) as file:
        for line in file:
            json_obj = json.loads(line)
            pprint.pprint(convert(json_obj))
    return "Finished"

if (sys.argv[1]):
    read(sys.argv[1])
else:
    print "No file passed in args"
