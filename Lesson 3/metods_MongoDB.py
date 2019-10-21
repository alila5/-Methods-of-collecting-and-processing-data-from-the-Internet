from pymongo import MongoClient
from pprint import pprint
import  FindVacHH as fvHH
import  FindVacSJ as fvSJ
import transliterate

def Connect_collectionsDB(col_name):
    client = MongoClient('localhost',27017)
    db = client['vacancy_new']
    #print(db.collection_names())
    #if col_name in db.collection_names():
    #    res = db.col
    #    else:
    #        print('new')
    try:
       res = db.create_collection(col_name)
       #res = db.col_name
    except:
        res = db.vac
    return res

def Write_to_collections(col_con, list_of_vac):
    old = col_con.count()
    for vac in list_of_vac:
        find_obj_in_DB = col_con.find(vac).count()
        if find_obj_in_DB != 0:
            print(f'The vacancy {vac["vname"]} is already in the  DB')
        else:
            col_con.insert_one(vac)
    new = col_con.count()
    print(f'Add {new-old} documents')
    print('*'*100,'\n')

vac ='повар'#input('Какую вакансию ищем? ')
vac_tr = transliterate.translit(vac, reversed=True)
max_page =2# int(input('Сколько страниц анализировать? '))

all_page_hh = fvHH.PageWorker(max_page, vac)
col_con_hh = Connect_collectionsDB('vac_hh')
Write_to_collections(col_con_hh, all_page_hh)

all_page_sj = fvSJ.PageWorker(max_page, vac_tr)
col_con_sj = Connect_collectionsDB('vac_sj')
Write_to_collections(col_con_sj, all_page_sj)

ob = col_con_sj.find({'salary_min':{'$gte':40000}})
for o in ob:
    pprint(o)

# objects = users.find({'author':'John'},{'author','date','age'})
# objects = users.find({'age':{'$gte':10}}).sort('author').limit(3)
#users.delete_one({'name':'Георгий'})

#objects = users.find().sort('author')
# for obj in objects:
#     pprint(obj)

#print(users.count_documents({'author':'Eliot'}))
#\