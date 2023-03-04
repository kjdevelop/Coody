
import pymongo
import random

client = pymongo.MongoClient("mongodb+srv://ze0966747312:a0966747312@cluster0.bf8bdil.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
mydb=client["Coody_line_bot"]
mycol=mydb["Coody_String"]

def Coody_message():
    max=mycol.find_one({},sort=[("Choice",-1)])#最大值
    min=mycol.find_one({},sort=[("Choice",1)]) #最大值
    print(min)
    number=random.randint(min["Choice"],max["Choice"])
    final_choice=mycol.find_one({"Choice":number})
    return final_choice["String"]

def learning_Greet(msg):
    max=mycol.find_one({},sort=[("Choice",-1)])
    num=max["Choice"]+1
    dict={"Choice":num,"String":msg}
    mycol.insert_one(dict)
    return "寶寶學習到新知識啦"
