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
            output = " 1.6 : " + str(Inuput1[1.6])  + " , 0.6 : " + str(Inuput1[0.6]) +  " , 0.3 : " + str(sixsix)
    else:
        Inuput1 = attributes[InuputAttributes][mothed]
        output = "克制: " + str(Inuput1[1.6])  + "  \n0.6 倍: " + str(Inuput1[0.6]) +  "  \n0.3 倍: " + str(Inuput1[0.3])
    
    output = output.replace("[","").replace("]","").replace("'","").replace("{","").replace("}","")

    return output
