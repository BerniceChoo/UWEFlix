import pymongo
connect_string = 'mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority' 

from django.conf import settings
my_client = pymongo.MongoClient(connect_string)

#Define the database name
dbname = my_client['sample_medicines']

#Get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["medicinedetails"]

#Create two documents
medicine_1 = {
    "medicine_id": "RR000123456",
    "common_name" : "Paracetamol",
    "scientific_name" : "",
    "available" : "Y",
    "category": "fever"
}
medicine_2 = {
    "medicine_id": "RR000342522",
    "common_name" : "Metformin",
    "scientific_name" : "",
    "available" : "Y",
    "category" : "type 2 diabetes"
}

#Insert the documents
collection_name.insert_many([medicine_1,medicine_2])



#Read the documents
med_details = collection_name.find({})

#Print on the terminal
for r in med_details:
    print(r["common_name"])

#Update one document
update_data = collection_name.update_one({'medicine_id':'RR000123456'}, {'$set':{'common_name':'Paracetamol 500'}})

#Delete one document
delete_data = collection_name.delete_one({'medicine_id':'RR000123456'})