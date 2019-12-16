import json
import re
import pandas as pd

#Category Transforms
#Goal: Fix or Drop Categories that have been categorized wrong without changeing the orignal data
#save Transform into an excel doc with a seprate page for each kind of transform.
#Each sheet need 2 cols, Name and Action

#Transforms Type
#Fix or Drop Categories based on the current Category
print("Progress: Transforms Type")
def Translate(x):
    CurrentType = x['TYPE']
    if CurrentType in list(TranslationLookUp.keys()):
        x['TYPE'] = TranslationLookUp[CurrentType]
    if x['TYPE'] != 'Drop' and type(x['TASK']) == type(""):
        return x
		
TypeTranslation = pd.read_excel('Transforms.xlsx',sheet_name="Types",index_col="Name")
TranslationLookUp = TypeTranslation['Action'].to_dict()
df = df.apply(Translate,axis=1).dropna(how='all')
print(len(df))

#Transforms WOs
#Fix or Drop Categories based on the Indvle ID of the row. 
print("Progress: Transforms WOs")
def Translate(x):
    CurrentWO = x.WO_NUM
    if CurrentWO in list(TranslationLookUp.keys()):
        x['TYPE'] = TranslationLookUp[CurrentWO]
    if x['TYPE'] != 'Drop' and type(x['TYPE']) == type(""):
        return x
		
WOTranslation = pd.read_excel('Transforms.xlsx',sheet_name="WOs",index_col="Name")
TranslationLookUp = WOTranslation['Action'].to_dict()
df = df.apply(Translate,axis=1).dropna(how='all')
print(len(df))

#Word Level Clean UP
#Remove Names
with open("namelists.json", "r") as read_file:
    NameTranslation = json.load(read_file)
   
def removenames(x)
    #Remove the First Names
    namelist = NameTranslation['first']
    for name in namelist:
        if type(name) is str:
            if name.lower()+" " in x:
                x = x.replace(name.lower(),'RFirstName')
    #Remove the Last Names
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

print("Progress: CleanUp")
df['TASKClean'] = df.TASK.apply(cleanup)

#Export Cleaned Data to review the transformed data results
df.to_csv("CleanedData.csv")
