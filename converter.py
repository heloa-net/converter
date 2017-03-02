import json

#val is imported json
val = '''
{
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
'''

val2 = '''
{

}
'''

old = json.loads(val)
new = dict();
if len(old) == 0:
  print(new)
else:
  for key in old:
    if old[key] == []:
      new[key] = {}
  print(new)