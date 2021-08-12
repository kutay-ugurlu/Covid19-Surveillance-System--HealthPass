import dotenv as dv
import pymongo
from datetime import datetime
import random
import time
import os

DBError = pymongo.errors.PyMongoError

MongoDBaddress = dv.get_variable(".env","dbadress")

print(MongoDBaddress)

client = pymongo.MongoClient(MongoDBaddress, socketTimeoutMS=10000, connectTimeoutMS=10000, serverSelectionTimeoutMS=10000)

db = client['surveillances']

collection = db['surveillance']
collection_numberofpeople = db['surveillance_numberofpeople']

storeName = "AlgoDetectium5"

dbfourchoice = client[storeName]
collection_options = dbfourchoice['options']

prevLogs = []
exitedPeople = 0
enteredPeople = 0
cachePeopleInside = 0
cachedOptions = None

def sendLog(temp, expected_ans, ans, facemask, peopleInside, isAllowed):
    global prevLogs
    obj = {"date": datetime.now(),
        "temp": temp,
        "expected_ans": expected_ans,
        "ans": ans,
        "facemask": facemask,
        "peopleInside": peopleInside,
        "storeName": storeName,
        "isAllowed": isAllowed}
    try:
        if prevLogs != []:
            collection.insert_many(prevLogs)
            prevLogs = []
        collection.insert_one(obj)
    except DBError:
        print("Connection Lost! The logs will be sent later.")
        prevLogs.append(obj)

def sendLogOut():
    global exitedPeople
    try:
        collection_numberofpeople.update({'storeName': str(storeName), 'peopleInside': {"$gt": 0}}, {
                                        '$inc': {'peopleInside': -1 - exitedPeople}}, upsert=False)
        collection_numberofpeople.update({'storeName': str(storeName), 'peopleInside': {"$lt": 0}}, {
                                        '$set': {'peopleInside': 0}}, upsert=False)
        exitedPeople = 0
    except DBError:
        print("Connection Lost! Exitted person will be sent later.")
        exitedPeople += 1

def sendLogIn():
    global enteredPeople
    try:
        collection_numberofpeople.update({'storeName': str(storeName)}, {'$inc': {'peopleInside': 1 + enteredPeople},
                                                                        '$setOnInsert': {'storeName': str(storeName)}}, upsert=True)
        enteredPeople = 0
    except DBError:
        print("Connection Lost! Entered person will be sent later.")
        enteredPeople += 1

def number_of_people_inside():
    global cachePeopleInside
    try:
        peopleInside = 0
        log = collection_numberofpeople.find_one({"storeName": str(storeName)})
        if log:
            peopleInside = log["peopleInside"]
            cachePeopleInside = peopleInside
        return peopleInside + enteredPeople - exitedPeople
    except DBError:
        print("Connection Lost! Cached value is being returned.")
        return cachePeopleInside + enteredPeople - exitedPeople

def getOptions():
    global cachedOptions
    try:
        ret = collection_options.find_one()
        cachedOptions = ret
        return ret
    except DBError:
        print("Connection Lost! Cached value is being returned.")
        return cachedOptions

def setNumberofPeople(n):
    try:
        collection_numberofpeople.update({'storeName': str(storeName)}, {'$set': {'peopleInside': n},
                                                                        '$setOnInsert': {'storeName': str(storeName)}}, upsert=True)
    except DBError:
        print("Connection Lost! Could not set the number of poeple!")