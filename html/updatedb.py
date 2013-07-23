import os
import StringIO
from lxml import etree
import csv

def getIDforDesign(type):
    file = 'db/Type'+type+'.csv'
    id=0
    # does file exist? if not n will be 0. if it does we need to get the last id
    if os.path.exists(file):
        with open(file, 'rU') as csvfile:
            typereader = csv.reader(csvfile)
            for row in typereader:
                if (len(row)>0 and not str(row[0])=='id'):
                    id=int(row[0])
        csvfile.close()
    return id

tdir = "../templates/"
items = os.listdir(tdir)

types = []
alloptionals = []
# get types and update those 
for file in items:
    if file.startswith("Type_") and file.endswith(".xml"):
        tree = etree.parse(tdir+file)
        name= tree.findtext("name")
        shortname = os.path.splitext(file)[0][5:]
        types.append(shortname)
        optionals= tree.findtext("optionals").split(',')
        if len(optionals)>0:
            with open('db/'+shortname+'Options.csv', 'wb') as csvfile:
                optwriter = csv.writer(csvfile)
                optwriter.writerow(['id', 'desc', 'xml'])
                n=1
                for option in optionals:
                    if (len(option)>1):
                        # we'll use this later..
                        alloptionals.append(option)
                        #get the desc for the optional
                        otree = etree.parse(tdir+option+'.xml')
                        optwriter.writerow([n, otree.findtext("name"), option])
                        n=n+1

# now update the Type csvs - with each design
designs = []
for file in items:
    if file.endswith(".xml") and not file.startswith("Type_") and not file.startswith('.'):
        designs.append(file)
        tree = etree.parse(tdir+file)
        name= tree.findtext("name")
        type= tree.findtext("type")
        #case= tree.findtext("case")
        shortname = os.path.splitext(file)[0]
        if shortname not in alloptionals:
            #print name, type, case, shortname
            id=getIDforDesign(type)
            with open('db/Type'+type+'.csv', 'a') as csvfile:
                optwriter = csv.writer(csvfile)
                if (id==0):
                    optwriter.writerow(['id', 'desc', 'xml'])
                optwriter.writerow([id+1, name, shortname])
                csvfile.close()

        