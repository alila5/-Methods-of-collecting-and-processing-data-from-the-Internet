# -*- coding: utf-8 -*-
import vk
from vk.exceptions import VkAuthError, VkAPIError
from collections import Counter
import time
from pymongo import MongoClient

def  Connect_collectionsDB(col_name):
    res = None
    client = MongoClient('localhost',27017)
    db = client['VK_info']
    try:
       res = db.create_collection(col_name)
    except:
       print(f'Connect with {col_name}!!! OK!')
       res= db.get_collection(col_name)
    return res

def Write_to_collections(col_con, info):
    col_con.insert_one(info)

class Take_hands():
    def __init__(self, login, password, id_start, id_end,**kw):
        self.login = login
        self.password = password
        self.start = id_start
        self.node = {}
        self.ftime = time.time()
        self.nodes = []
        self.victory = []
        self.know = []
        self.fiends_end = []
        self.lh= [None, None, None, None, None, None]#,None, None, None, None,None, None, None, None]
        self.vk_session = self.VKSession(self.login, self.password)
        self.vkAPI = self.getAPI()




    def VKSession (self,login, password):
        vk_session = vk.Session(access_token ='58f167fd58f167fd58f167fd96589eedf5558f158f167fd06cadb41750a527964dabcad')#vk_api.VkApi(login, password)
        #try:
        #    vk_session.auth(token_only=True)
        #except vk_api.AuthError as error_msg:
        #    print(error_msg)
        #    vk_session = None
        return vk_session

    def getAPI(self):
        try:
            #vkAPI = self.vk_session.get_api()
            vkAPI= vk.API(self.vk_session)
        except Exception as e:
            print(e)
        return  vkAPI

    def GetFriendsById(self, account_id=None):
        if account_id != None:
            response = self.vkAPI.friends.get(user_id=account_id, v='5.103')
            #api.users.get(user_ids=1)
        else:
            response = self.vkAPI.friends.get()
        if response['items']:
            pass
            #print(response)['items']
        return response



    def Find_handshake_from_start_to_end(self, prev_call, hop):
        hop = hop
        next_call = []
        n = 0
        for from_id, nodes in prev_call:
            loop = 0
            for id in nodes:
                #print(id)
                temp = list(from_id)
                #print(temp)
                try:
                    ffvk.know.append(id)
                    node_fids = ffvk.GetFriendsById(account_id=id)['items']
                    user = {'id': id, 'link':'https://vk.com/id'+str(id),'info': node_fids}
                    loop = loop +1
                    match = [id for id in node_fids if id in ffvk.friends_end]#id == ffvk.end]
                    if id != ffvk.end:
                        temp.append(id)
                    print(temp, 'Working time', time.time() - ffvk.ftime, 'hop=', hop, 'nodes left=', len(prev_call)-n, 'loop=', loop, 'left loop= ', len(nodes) - loop)
                    ffvk.nodes.append((temp, node_fids))
                    Write_to_collections(user_col, user)
                    if len(match) != 0:
                        print('---Victory !!!---' * 2)
                        print('Finish time', time.time() - ffvk.ftime)
                        for id in match:
                            smsg = ''
                            for inid in temp:
                                smsg = smsg + str(inid) + '<->'
                            smsg = smsg + '!'+str(id) +'<->'+str(ffvk.end)
                            result =  {'result': smsg, 'know persons': len(ffvk.know), 'time': time.time() - ffvk.ftime}
                            Write_to_collections(col, result)
                            print(smsg)
                            print('Lenght of know', len(ffvk.know))
                        ffvk.victory.append(temp)
                        ffvk.victory.append(ffvk.end)
                    l = len(node_fids)
                    _ids = [id for id in node_fids if id not in ffvk.know]
                    next_call.append((temp, _ids))
                    l = len(_ids)
                except vk.exceptions.VkAPIError as error_msg:
                    print(error_msg)
            n = n+1
        hop = hop+1
        print('-'*40)
        print('Lenght of know', len(ffvk.know))
        print('-' * 40)
        time.sleep(3)
        self.Find_handshake_from_start_to_end(next_call, hop)



if __name__ == '__main__':

    col = Connect_collectionsDB('FHH')
    user_col = Connect_collectionsDB('USER')

    start = 1072139 #944611#4412343 #58482966#19104#19104# 223298321#395634522 #395634522
    end = 236849421 #514413543#1155344#162425 #223298321  #id1155344

    ffvk = Take_hands('email', 'pwd', start, end )

    try:
        id1_friends = ffvk.GetFriendsById(account_id=start)['items']
        len1= len(id1_friends)
    except vk.exceptions.VkAPIError as error_msg:
        len1=[]
        print(error_msg)
        print('Аккаунт', start, ' не может быть использован как стартовый')
        #exit(0)

    try:
        id2_friends = ffvk.GetFriendsById(account_id=end)['items']
        len2= len(id2_friends)
    except vk.exceptions.VkAPIError as error_msg:
        len2=[]
        print(error_msg)
        print('Аккаунт', end, ' не может быть использован для расчета с конца цепочки')
        #exit(0)

    if len1 == [] and len2 ==[] :
        print('Запуск не возможен')
        exit(0)
    elif len1==[] and len2 != [] :
        ids = [([], [end])]
        ffvk.start = end
        ffvk.end = start
        ffvk.friends_end = []
    elif len2==[] and len1 != [] :
        ids = [([], [start])]
        ffvk.start = start
        ffvk.end = end
        ffvk.friends_end = []
    elif len1>len2 :
        ids = [([],[end])]
        ffvk.start = end
        ffvk.end = start
        ffvk.friends_end =  id1_friends
    else:
        ids = [([],[start])]
        ffvk.start = start
        ffvk.end = end
        ffvk.friends_end =  id2_friends


    ffvk.know.append(ffvk.end)
    ffvk.know.extend(ffvk.friends_end)
    hop =0

    ffvk.Find_handshake_from_start_to_end(ids,  hop)