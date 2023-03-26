import pymongo

client = pymongo.MongoClient('mongodb+srv://choo2foonyee:FpaMQ6825hCyJw6x@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['Showings']
