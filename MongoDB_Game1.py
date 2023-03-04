import pymongo
import random
import MongoDB_profile

client = pymongo.MongoClient("mongodb+srv://ze0966747312:a0966747312@cluster0.bf8bdil.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
mydb=client["Coody_line_bot"]
mycol=mydb["Game_1"]

def Initial_Game1(user_id,range_lar):
    secret_num=random.randint(2,int(range_lar)-1)
    list={"User_Id":user_id,"guess":-1,"range_sm":0,"range_lar":int(range_lar),"secret_num":secret_num}
    mycol.insert_one(list)

def play_game(user_id,guess):
    guess=int(guess)
    IP=mycol.find_one({ "User_Id":user_id })
    mycol.update_one({"User_Id":user_id},{"$set":{"guess":guess}})
    range_sm=int(IP["range_sm"])
    range_lar=int(IP["range_lar"])
    secret_num=int(IP["secret_num"]) 

    if guess > secret_num and  guess<range_lar:
        mycol.update_one({"User_Id":user_id},{"$set":{"range_lar":guess}})
        (sm,lar)=range(user_id)
        return ("太高了\n"+"範圍:"+str(sm)+"~"+str(lar))
    elif guess<secret_num and guess>range_sm:
        mycol.update_one({"User_Id":user_id},{"$set":{"range_sm":guess}})
        (sm,lar)=range(user_id)
        return ("太低了\n"+"範圍:"+str(sm)+"~"+str(lar))
    elif guess==secret_num:
        MongoDB_profile.update_Status(user_id,"Standard")
        mycol.delete_one({"User_Id":user_id})
        return ("答對啦\n答案:"+str(IP["secret_num"]))
    else:
        return "唉呦！是不是沒有認真看範圍呀"        


def range(user_id):
        IP=mycol.find_one({"User_Id":user_id})
        a=IP["range_sm"]
        b=IP["range_lar"]
        return (a,b)
    