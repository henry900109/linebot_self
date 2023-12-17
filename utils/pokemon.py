# %%time
from functools import lru_cache

import requests
from bs4 import BeautifulSoup
import json

def Attributes_Table(InuputAttributes,mothed = "suppress"):
# restraint 克制 ,suppress 被克制 ,Reduce damage 扛傷
    InuputAttributes = InuputAttributes.replace("系","")
    InuputAttributes = InuputAttributes.replace("屬","")
    InuputAttributes = InuputAttributes.replace("超能力","超能")
    if "妖精" not in InuputAttributes:
      InuputAttributes = InuputAttributes.replace("妖","妖精")
    elif " " == InuputAttributes[0]:
        InuputAttributes = InuputAttributes[1:]
    name = ["一般","格鬥","毒","地面","飛行","蟲","岩石","幽靈","鋼","火","水","電","草","冰","超能","龍","惡","妖精"]
    attributes = {
        "一般" :  {"restraint" : {1.6 : [], 0.6 : ["岩石","鋼"],0.3: ["幽靈"]},"suppress" : { 1.6 : ["格鬥"],0.6 : [], 0.3 : ["幽靈"]}},
        "格鬥" :  {"restraint" : {1.6 : ["一般","鋼","冰","惡","岩石"], 0.6 : ["毒","飛行","蟲","超能","妖精"],0.3:["幽靈"]},"suppress" : {1.6 : ["飛行","超能","妖精"], 0.6 : ["蟲","岩石","惡"], 0.3 : []}},
        "毒"   :  {"restraint" : {1.6 : ["草","妖精"], 0.6 : ["毒","地面","岩石","幽靈"], 0.3 :["鋼"] },"suppress" : {1.6 : ["地面","超能"], 0.6 : ["格鬥","毒","蟲","草","妖精"], 0.3 : []}},
        "地面" :  {"restraint" : {1.6 : ["鋼","火","電"], 0.6:["蟲","草"], 0.3:["飛行"]},"suppress" : {1.6 : ["水","草","冰"], 0.6 : ["毒","岩石"], 0.3 : ["電"]}},
        "飛行" :  {"restraint" : {1.6 : ["格鬥","蟲","草"], 0.6 : ["岩石","鋼","電"],0.3:[]},"suppress" : {1.6 : ["電","岩石","冰"], 0.6 : ["格鬥","蟲","草"], 0.3 : ["地面"]}},
        "蟲"   :  {"restraint" : {1.6 : ["草","超能","惡"], 0.6 : ["格鬥","毒","飛行","幽靈","鋼","火","妖精"], 0.3 : []},"suppress" : {1.6 : ["飛行","岩石","火"], 0.6 : ["格鬥","地面","草"], 0.3 : []}},
        "岩石" :  {"restraint" : {1.6 : ["飛行","蟲","火","冰"], 0.6 : ["格鬥","地面","鋼"], 0.3 : []},"suppress" : {1.6 : ["格鬥","地面","鋼","水","草"], 0.6 : ["一般","毒","飛行","火"], 0.3 : []}},
        "幽靈" :  {"restraint" : {1.6 : ["幽靈","超能"], 0.6 : ["惡"], 0.3 : ["一般"]},"suppress" : {1.6 : ["幽靈","惡"], 0.6 : ["毒","蟲"], 0.3 : ["一般","格鬥"]}},
        "鋼"   :  {"restraint" : {1.6 : ["岩石","冰","妖精"], 0.6 : ["鋼","火","水","電"], 0.3 : []},"suppress" : {1.6 : ["格鬥","地面","火"], 0.6 : ["一般","飛行","蟲","岩石","鋼","草","冰","超能","龍","妖精"], 0.3 : ["毒"]}},
        "火"   :  {"restraint" : {1.6 : ["蟲","鋼","草","冰"], 0.6 : ["岩石","火","水","龍"], 0.3 : []},"suppress" : {1.6 : ["地面","岩石","水"], 0.6 : ["蟲","鋼","火","草","冰","妖精"], 0.3 : []}},
        "水"   :  {"restraint" : {1.6 : ["地面","岩石","火"], 0.6 : ["水","草","龍"], 0.3 : []},"suppress" : {1.6 : ["電","草"], 0.6 : ["鋼","火","水","冰"], 0.3 : []}},
        "電"   :  {"restraint" : {1.6 : ["蟲","水"], 0.6 : ["電","草","龍"], 0.3 : ["地面"]},"suppress" : {1.6 : ["地面"], 0.6 : ["飛行","鋼","電"], 0.3 : []}},
        "草"   :  {"restraint" : {1.6 : ["地面","岩石","水"], 0.6 : ["毒","飛行","蟲","鋼","火","草","龍"], 0.3 : []},"suppress" : {1.6 : ["毒","飛行","蟲","火","冰"], 0.6 : ["地面","水","電","草"], 0.3 : []}},
        "冰"   :  {"restraint" : {1.6 : ["飛行","蟲","草","龍"], 0.6 : ["鋼","火","草","冰"], 0.3 : []},"suppress" : {1.6 : ["格鬥","岩石","鋼","火"], 0.6 : ["冰"], 0.3 : []}},
        "超能" :  {"restraint" : {1.6 : ["格鬥","毒"], 0.6 : ["鋼","超能"], 0.3 : ["惡"]},"suppress" : {1.6 : ["蟲","幽靈","惡"], 0.6 : ["格鬥","超能"], 0.3 : []}},
        "龍"   :  {"restraint" : {1.6 : ["龍"], 0.6 : ["鋼"], 0.3 : ["妖精"]},"suppress" : {1.6 : ["冰","龍","妖精"], 0.6 : ["火","水","電","草"], 0.3 : []}},
        "惡"   :  {"restraint" : {1.6 : ["幽靈","超能"], 0.6 : ["惡","妖精"], 0.3 : []},"suppress" : {1.6 : ["格鬥","蟲","妖精"], 0.6 : ["幽靈","惡"], 0.3 : ["超能"]}},
        "妖精" :  {"restraint" : {1.6 : ["格鬥","超能","惡"], 0.6 : ["地面","鋼","火"], 0.3 : []},"suppress" : {1.6 : ["毒","鋼"], 0.6 : ["格鬥","蟲","惡"], 0.3 : ["龍"]}},
    }
    if mothed == "suppress":
        try: 
            name_attr = []
            for item in name:
                if item in InuputAttributes:
                    name_attr.extend(InuputAttributes.split(item))
            name_attr = [x for x in name_attr if x in name]
            InuputAttributes1,InuputAttributes2 = name_attr[0],name_attr[1]     
            Inuput1 = attributes[InuputAttributes1][mothed]
            Inuput2 = attributes[InuputAttributes2][mothed]
            Max = (set(Inuput1[1.6]).intersection(set(Inuput2[1.6])))
            one = (set(Inuput1[1.6]).intersection(set(Inuput2[0.6])).union(set(Inuput1[0.6]).intersection(set(Inuput2[1.6])))) #2.56
            onesix = (set(Inuput1[1.6]).union(set(Inuput2[1.6]))).difference(Max).difference(one) #1.6
            sixsix = (set(Inuput1[0.6]).intersection(set(Inuput2[0.6]))).union(set(Inuput1[0.3]).union(set(Inuput2[0.3]))) #0.3
            six = set(Inuput1[0.6]).union(set(Inuput2[0.6])).difference(sixsix).difference(one) #0.6
            onesix_in_zerothree = onesix.intersection(sixsix)
            six = six.union(onesix_in_zerothree)
            onesix = onesix.difference(onesix_in_zerothree)
            sixsix = sixsix.difference(onesix_in_zerothree)
            if "" in sixsix:
                sixsix.remove("")
            if not Max:
                Max = None
            elif not onesix:
                onesix = None
            elif not six:
                six = None
            elif not sixsix:
                sixsix = None
            output = "2.56 : " + str(Max) + "\n 1.6 : " + str(onesix)  + " \n 0.6 : " + str(six) +  " \n 0.3 : " + str(sixsix)
        except:
            Inuput1 = attributes[InuputAttributes][mothed]
            sixsix = Inuput1[0.3]
            if not sixsix:
                sixsix = None
            output = " 1.6 : " + str(Inuput1[1.6])  + " \n 0.6 : " + str(Inuput1[0.6]) +  " \n 0.3 : " + str(sixsix)
    else:
        Inuput1 = attributes[InuputAttributes][mothed]
        sixsix = Inuput1[0.3]
        Max = Inuput1[1.6]
        if not sixsix:
            sixsix = None
        elif not Max:
            Max = None
        output = "克制: " + str(Max)  + "  \n0.6 倍: " + str(Inuput1[0.6]) +  "  \n0.3 倍: " + str(sixsix)
    
    output = output.replace("[","").replace("]","").replace("'","").replace("{","").replace("}","")

    return output

@lru_cache(maxsize=None)
def allattr(url = "https://twpkinfo.com/PokemonSkill.aspx"):
    html = requests.get(url)
    soup=BeautifulSoup(html.text,"html.parser")
    result = soup.find_all(class_= "name")
    result = result[3:]
    return result

def attr(name):
    if " " == name:
        name = name[1:]
    try:
        path = r'/var/task/data/attr.json'
        jsonFile = open(path,'r')
        data = jsonFile.read()
        data = json.JSONDecoder().decode(data)
    except:
        result = allattr(url = "https://twpkinfo.com/PokemonSkill.aspx")
        data = {}
        for i in range(0,len(result),3):
            data[str(result[i].getText())] = result[i+2].getText()
    # print(data)
    for item in data.keys():
        if name in item:
            d = data[item].replace("、","")
            attr = Attributes_Table(d,"suppress")
            return item + ": " + data[item] + "\n" + attr

        

@lru_cache(maxsize=None)
def get_chinese_name(url):
    html = requests.get(url)
    data = json.JSONDecoder().decode(html.text)
    return data

@lru_cache(maxsize=None)
def cp_rank(rank):
    # rank = ['1500','2500','10000']
    url = 'https://pvpoketw.com/data/rankings/all/overall/rankings-'+ rank +'.json?v=1.31.4'
    html = requests.get(url)
    data = json.JSONDecoder().decode(html.text)
    # print(data)
    return data





def attack(attack):
    try:
        with open(r'/var/task/data/pokename.json','r') as file:
            data = json.load(file)
    except:
        data = get_chinese_name(url = 'https://pvpoketw.com/data/gamemaster.min.json?v=1.31.4')
    for i in range(len(data['moves'])):
        if attack in data['moves'][i]['moveId']:
            return (data['moves'][i]['name'])

def name(name):
    try:
        with open(r'/var/task/data/pokename.json','r') as file:
            data = json.load(file)
    except:
        data = get_chinese_name(url = 'https://pvpoketw.com/data/gamemaster.min.json?v=1.31.4')
    # print(data['pokemon'])
    for i in range(len(data['pokemon'])):
        if abs(len(name) -len(data['pokemon'][i]['speciesName'])) <3 and name in data['pokemon'][i]['speciesName']:
            return (data['pokemon'][i]['speciesId'])

# abs(len(Ename) -len(reply[i]['speciesId'])) < 3 and
def Rank(Cname,rank = "2500"):
    temp = ['1500','2500','10000']
    cp = set(temp).difference([rank])
    # print(cp[0])
    reply = cp_rank(rank)
    Ename = name(Cname)
    # print(Ename)
    # print(reply)
    respone = []
    cprank = []
    for i in range(len(reply)):
        if  Ename in (reply[i]['speciesId']):
            cprank.append(i+1)
            for item in reply[i]['moveset']:
                respone.append(attack(item))
            break
        elif i == len(reply)-1:
            cprank.append("None")

    for item in (cp):
        reply = cp_rank(item)
        for i in range(len(reply)):
                if  Ename in (reply[i]['speciesId']):
                    cprank.append(i+1)
                    break
                elif i == len(reply)-1:
                    cprank.append("None")
    cp = list(cp)
    cp.append(rank)    
    if respone == []:
        print(respone)
        respone.extend(["None","None","None"])
    
    cp = ["大師聯盟" if value == '10000' else "高級聯盟" if value == '2500'else "超級聯盟" if value == '1500' else value for value in cp]
    respone = f"{attr(Cname)}\n\n{cp[0]} 排名: {cprank[1]} \n{cp[-1]} 排名: {cprank[0]} \n{cp[1]} 排名: {cprank[2]}\n大招: {respone[0]}\n小招: {respone[1]},{respone[2]}"
    # temp = ["大師聯盟" if value == '10000' else "高級聯盟" if value == '2500'else "超級聯盟" if value == '1500' else value for value in temp]
    # respone = f"{attr(Cname)}\n\n{temp[-1]} 排名: {cprank[0]} \n{temp[1]} 排名: {cprank[1]} \n{temp[2]} 排名: {cprank[2]}\n大招: {respone[0]}\n小招: {respone[1]},{respone[2]}"
    return respone

if __name__ == '__main__':
    print(Rank("哲爾尼亞斯","2500"))
  
