from pymongo import MongoClient
import pymongo
import datetime
client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
db = client.test

todo1 = {"name": "Patrick", "text": "My first todo!","status": "open",
        "tags": ["python", "coding"], "date": datetime.datetime.utcnow()}

todos = db.todos

result = todos.insert_one(todo1)