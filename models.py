from utils import mongo
from bson import ObjectId

# get a user by id
def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})


# Create a new user
def create_user(username, email, hashed_password):
    result = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return mongo.db.users.find_one({"_id": result.inserted_id})


# Create a new user
def create_businesses(name, owner, location, category, phone, description):
    result = mongo.db.businesses.insert_one({
        "name": name,
        "owner": owner,
        "location": location,
        "category": category,
        "phone": phone,
        "description": description
    })
    return mongo.db.businesses.find_one({"_id": result.inserted_id})


# get all business
def get_all_business():
    businesses = list(mongo.db.businesses.find({}))
    # loop to convert all id from individual business to a string from objectid
    for business in businesses:
        business["_id"] = str(business["_id"])
    return businesses


# get a business by id
def get_business_by_id(business_id):
    business = mongo.db.businesses.find_one({"_id": ObjectId(business_id)})
    if business:
        business["_id"] = str(business["_id"])
    return business


# using business id update business data
def update_a_business(business_id, updated_data):
    mongo.db.businesses.update_one(
        {"_id": ObjectId(business_id)},
        {"$set": updated_data}
    )
    return mongo.db.businesses.find_one({"_id": ObjectId(business_id)})


# delete a specifi business
def delete_a_business(business_id):
    return mongo.db.businesses.delete_one({"_id": ObjectId(business_id)})