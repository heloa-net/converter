import pprint

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

json_obj = {
    "BF": [],
    "D": [
        ["Side", "eq", "1", "OrdType", "eq", "2"],
        ["Side", "eq", "2", "OrdType", "eq", "2"]
    ],
    "F": [],
    "U4": [],
    "U6": [
        ["Method", "eq", "bb"],
        ["Method", "eq", "bradesco"],
        ["Method", "eq", "ted"],
        ["Method", "eq", "doc"],
        ["Method", "eq", "Caixa"]
    ],
    "U2": [],
    "U18": [
        ["Currency", "eq", "BTC"]
    ],
    "U26": [],
    "U34": [],
    "U30": [],
    "U23": [],
    "U9": [],
    "U3": [],
    "U40": [],
    "8": [],
    "B2": [],
    "B8": [
        ["Verify", "in", [2, 3, 4]]
    ]
}

pprint.pprint(convert(json_obj))