from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json

def isNaN(num):
    return num != num

def readElements(filename):
    #Reads things you want form file 
  with open(filename) as json_file:
    data = json.load(json_file)[0]
    elements = data['elements']
    unit_cell_formula= data['unit_cell_formula']
    volume = data['volume']
  return elements, unit_cell_formula, volume

def download_ALLstructures(allIDs):
    #Gets structures from materialsproject API
    with MPRester("GKDHNwKre8uiowqhPh") as m:
        for id in allIDs:
            material_prop = m.query(criteria={"task_id": id}, properties = ["unit_cell_formula", 
 "pretty_formula","elements", "nelements","material_id"]) 
            print(material_prop)

########################################################
do_download = False # See fillproperties.py for this functionality
csvfile = 'manual.csv'
cif_info_dir = './cif_info_dir/'
data = pd.read_csv(csvfile, sep=',')
#print(list(data.head()))
#print(data['Charged_ID'])

#makes a list of all elements and makes a set
AllElements = []
for id in data['Charged_ID']:
    if isNaN(id)==False:
        fn = cif_info_dir + id + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn)
#            print('list0=', elements0)
            for iel, el in enumerate(elements0):
                AllElements.append(elements0[iel])
        except: 
            print("not working ID: ", id)
#            print('File not found', fn)
#print('All elements=',AllElements)
AllE = list(set(AllElements))
#delete(AllElements)


nfiles = len(data['Charged_ID'])
print("AllE   ",AllE)
for el in AllE:
#   data[el + '_vol'] = np.linspace(0, nfiles, nfiles-1)
  data[el + '_vol'] = [0.]*nfiles


#Finds the number of one type of atom *1000/volume
for iqid,qid in enumerate(data['Charged_ID']):
    mid = data['Battid'][iqid]
#    print('mid, qid=', mid, qid)
    if isNaN(qid) == False:
        fn = cif_info_dir + qid + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn)
            elems  = unit_cell_formula0
#            print('=====>', elements0, volume0, '  +    print("elems: ", elems)++  ', elems)
            for iel, el in enumerate(elements0):
                nel = elems[el]
#                print("el= ", el, "   nel=", nel)
                normVol = nel*1000. / volume0  
                data[el+'_vol'][iqid] = normVol

#             AllElements.append(elements0[iel])
#             AllFormula.append(unit_cell_formula0[iel])
#             AllVolume.append(volume0[iel])

        except: 
            print('File not found', fn)

df = pd.DataFrame(data)
df.to_csv("out_csv.csv")












