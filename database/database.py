from pymongo import MongoClient


# MongoDB connection

client = MongoClient(
    "mongodb://localhost:27017/"
)


# Database name

db = client["research_paper_analyzer"]



# Collections

users_collection = db["users"]

papers_collection = db["papers"]



# Function to save user details

def save_user(user):

    result = users_collection.insert_one(user)

    return str(result.inserted_id)



# Function to save paper analysis

def save_paper(paper):

    result = papers_collection.insert_one(paper)

    return str(result.inserted_id)



# Function to get all papers

def get_papers():

    papers = list(
        papers_collection.find(
            {},
            {"_id":0}
        )
    )

    return papers