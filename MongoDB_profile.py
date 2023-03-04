
import pymongo

client = pymongo.MongoClient("mongodb+srv://ze0966747312:a0966747312@cluster0.bf8bdil.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
mydb=client["Coody_line_bot"]
mycol=mydb["Profile"]


def store_profile(dict):
    mycol.insert_one(dict)

def  find_profile(user_id):
    return mycol.find_one({ "User_Id":user_id })


def delete_profile(user_id):
    mycol.delete_one({"User_Id":user_id})

def update_Status(user_id,status):
    mycol.update_one({"User_Id":user_id},{"$set":{"Status":status}})


def check_profil_exist(user_id):
    if find_profile(user_id) is None:
        return False
    else:
        return True
    