import pymongo

client = pymongo.MongoClient('mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['todos']
