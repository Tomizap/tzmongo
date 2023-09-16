from bson import ObjectId
from pymongo import MongoClient

# Définir l'URI de connexion
uri = "mongodb+srv://tom:jHq13Y2ru1y5Dijb@cluster0.crkabz3.mongodb.net/?retryWrites=true&w=majority"

# Créer un client MongoClient avec une configuration pour définir la version de l'API stable
client = MongoClient(uri)

def mongo(config={}):
    print("mongo")
    response = None
    if not config:
        config = {}

    db = config.get("db", "tools")

    col = config.get("collection", "users")

    action = config.get("action", "get")

    selector = config.get("selector", {})
    if selector.get('_id', config.get("_id")) is not None:
        selector['_id'] = ObjectId(selector.get('_id', config.get("_id")))
    selector["userAccess"] = { "$in": ["zaptom.pro@gmail.com"] }

    updator = config.get("updator")

    try:
        print(f"Se connecter à MongoDB")
        client.start_session()
        print(f"Connecté à MongoDB {db} {col}")
        collection = client[db][col]
        if action == "get":
            response = list(collection.find(selector))
        elif action in ("add", "create"):
            response = collection.insert_one(selector).inserted_id
        elif action == "edit":
            response = collection.update_one(selector, updator).acknowledged
        elif action == "delete":
            response = collection.delete_one(selector).acknowledged

    except Exception as e:
        print("Error: " + str(e))

    finally:
        client.close()

    return response


# m = mongo({
#     "action": 'add',
#     "selector": {
#         "email": "test"
#     }
# })
# print(m)