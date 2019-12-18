import json
import re
import pandas as pd

# Category Transforms
# Goal: Fix or Drop Categories that have been categorized wrong without changeing the orignal data
# save Transform into an excel doc with a seprate page for each kind of transform.
# Each sheet need 2 cols, Name and Action
TranslationLookUp = pd.read_excel('Transforms.xlsx',sheet_name="Types",index_col="Name")['Action'].to_dict()
WOTranslationLookUp = pd.read_excel('Transforms.xlsx',sheet_name="WOs",index_col="Name")['Action'].to_dict()

# Transforms Type
# Fix or Drop Categories based on the current Category
def TranslateType(x):
    CurrentType = x['TYPE']
    if CurrentType in list(TranslationLookUp.keys()):
        x['TYPE'] = TranslationLookUp[CurrentType]
    if x['TYPE'] != 'Drop' and type(x['TASK']) == type(""):
        return x

# Transforms WOs
# Fix or Drop Categories based on the Indvle ID of the row. 
def TranslateWO(x):
    CurrentWO = x.WO_NUM
    if CurrentWO in list(WOTranslationLookUp.keys()):
        x['TYPE'] = WOTranslationLookUp[CurrentWO]
    if x['TYPE'] != 'Drop' and type(x['TYPE']) == type(""):
        return x

# Word Level Clean UP
# Remove Names
def removenames(x):
    with open("namelists.json", "r") as read_file:
        NameTranslation = json.load(read_file)
    namelist = NameTranslation['first']
    for name in namelist:
        if type(name) is str:
            if name.lower()+" " in x:
                x = x.replace(name.lower(),'RFirstName')
    namelist = NameTranslation['last']
    for name in namelist:
        if type(name) is str:
            if " "+name.lower() in x:
                x = x.replace(name.lower(),'RLastName')
    if '[FName] [LName]' in x:
        x = x.replace('RFirstName RLastName','RFullName')
    return x
    namelist = NameTranslation['last']
    for name in namelist:
        if type(name) is str:
            if " "+name.lower() in x:
                x = x.replace(name.lower(),'RLastName')
    #Combine First and LastNames
    if '[FName] [LName]' in x:
        x = x.replace('RFirstName RLastName','RFullName')
    return x
    
def cleanup(x):
    x = x.lower()
    x = removenames(x)
    #Transform or Remove Stop words
    x = x.replace('can\'t','cant')
    x = x.replace('can not','cant')
    x = x.replace('account#','acct#')
    x = x.replace('&','and')
    x = x.replace('please ','')
    x = x.replace('can you ','')
    x = x.replace('re:','')
    x = x.replace('fw:','')
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/20[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]\/[0-9]?[0-9]\/[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-20[1-2][0-9]', 'RDate', x)
    x = re.sub(r'[0-9]?[0-9]-[0-9]?[0-9]-[1-2][0-9]', 'RDate', x)
    x = re.sub(r'\b\d{5}?\b', 'FiveDig', x)
    x = re.sub(r'\b\d{10}?\b', 'TenDig', x)
    x = x.replace(' - ',' ')
    return x
