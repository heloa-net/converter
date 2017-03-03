import pprint

def decode(raw_rule):
  res = {}
  while len(raw_rule) > 0:
    old_rule = raw_rule[:3]
    raw_rule = raw_rule[3:]

    if old_rule[1] == 'eq':
      new_rule = {old_rule[0]: old_rule[2]}
      res.update(new_rule)
    else:
      print "ERROR: Unrecognized operator:",  old_rule[1]

  return res

def convert(old_object):
  res = {}

  for obj_key, obj_val in old_object.iteritems():
    
    if obj_val and len(obj_val) > 1:
      or_obj = []

      for obj_rule in obj_val:
        rule = decode(obj_rule)
        or_obj.append(rule)
      res[obj_key] = { '$or': or_obj }
    else:
      res[obj_key] = {}

  return res 

val = {
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
  "8": []
}

pprint.pprint(convert(val))