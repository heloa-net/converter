import pprint

def convert_fn(old_object):
  res = {}

  for obj_key, obj_val in old_object.iteritems():
    print obj_key, obj_val
    
    if obj_val and len(obj_val) > 1:
      or_obj = []
      for obj_rule in obj_val:
        new_rule = {}
        new_rule[obj_key] = {}

        or_obj.append(new_rule)
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
pprint.pprint (convert_fn(val))