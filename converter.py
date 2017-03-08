import json
import sys

"""
$ python2.7 converter.py <file_with_permissions>
"""

def convert_rules(old_object):
    def decode_rule(raw_rule):
        res = {}
        for rule_index in xrange(0, len(raw_rule), 3 ):
            operator = raw_rule[rule_index+1]
            if operator == 'eq':
                new_rule = {raw_rule[rule_index+0]: raw_rule[rule_index+2]}
                res.update(new_rule)
            elif operator == 'in':
                new_rule = {raw_rule[rule_index+0]: {"$in": raw_rule[rule_index+2]}}
                res.update(new_rule)
            elif operator == 'has':
                first_part = raw_rule[rule_index+0]
                attributes = raw_rule[rule_index+2]

                if isinstance(raw_rule[rule_index+2], list):
                    while len(attributes) > 0:
                        aux_attrib = attributes.pop(0)
                        new_rule = {first_part + "." + aux_attrib: {"$exists": True}}
                        res.update(new_rule)
                elif isinstance(raw_rule[rule_index+2], unicode):
                    if len(raw_rule) == 6:
                        identifier = first_part + "." + attributes
                        
                        if identifier == raw_rule[rule_index+3]:
                            second_operator = raw_rule[rule_index+4]
                            
                            if raw_rule[rule_index+4] == 'eq' and isinstance(raw_rule[rule_index+5], bool):
                                single_rule = {identifier: raw_rule[rule_index+5]}
                            else:
                                raise RuntimeError("ERROR: Unrecognized has rule:" + str(raw_rule))
                        else:
                            raise RuntimeError("ERROR: Unrecognized compound has rule:" + str(raw_rule))
                        
                        res.update(single_rule)
                    elif len(raw_rule) == 3:
                        print "short unicode", str(raw_rule)
                        # check if conversion is correct
                        new_rule = {first_part + "." + raw_rule[rule_index+2]: {"$exists": True}}
                        res.update(new_rule)
                    else:
                        raise RuntimeError("ERROR: Unrecognized has rule pattern:" + str(raw_rule))
                    return res
            else:
                raise RuntimeError("ERROR: Unrecognized operator:" + str(operator))
        return res
    
    def optimize_rule(rule_obj):
        res = []
        aux = []
        for index, item in enumerate(rule_obj):
            val = item.values()
            if isinstance(val[0], bool):
                aux.insert(index, item)
            else:
                res.append(item)
        while len(aux) > 0:
            for index, item in enumerate(aux):
                key = item.keys()
                try:
                    first = aux.index({key[0]: False})
                    second = aux.index({key[0]: True})
                    res.append({key[0]: {"$type": "bool"}})
                    aux.__delitem__(first)
                    aux.__delitem__(second)
                except ValueError:
                    res.append(item)
                    aux.remove(item)
        return res

    res = {}
    for obj_key, obj_val in old_object.iteritems():

        if obj_val and len(obj_val) > 1:
            or_obj = []
            for obj_rule in obj_val:
                rule = decode_rule(obj_rule)
                or_obj.append(rule)
            optimized_obj = optimize_rule(or_obj)
            res[obj_key] = {"$or": optimized_obj}
        elif obj_val and len(obj_val) == 1:
            single_rule = obj_val[0]
            rule = decode_rule(single_rule)
            # should be optimized?
            res[obj_key] = rule
        else:
            res[obj_key] = {}

    return res

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for line in f:
            json_obj = json.loads(line)
            print(json.dumps(convert_rules(json_obj)))