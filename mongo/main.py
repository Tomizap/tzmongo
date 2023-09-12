from pymongo import MongoClient

# Définir l'URI de connexion
uri = "mongodb+srv://tom:jHq13Y2ru1y5Dijb@cluster0.crkabz3.mongodb.net/?retryWrites=true&w=majority"

# Créer un client MongoClient avec une configuration pour définir la version de l'API stable
client = MongoClient(uri, serverApi=ServerApiVersion.v1, serverApiStrict=True, serverApiDeprecationErrors=True)

async def mongo(config):
    print("mongo")
    response = None
    if not config:
        config = {}
    db = config.get("db", "tools")
    col = config.get("collection", "users")
    action = config.get("action", "get")
    selector = config.get("selector", {})
    selector["userAccess"] = { "$in": ["zaptom.pro@gmail.com"] }
    updator = config.get("updator")

    try:
        print(f"Se connecter à MongoDB")
        await client.start_session()
        print(f"Connecté à MongoDB {db} {col}")
        collection = client[db][col]
        if action == "get":
            response = await collection.find(selector).to_list(length=None)
        elif action in ("add", "create"):
            response = await collection.insert_one(selector)
        elif action == "edit":
            response = await collection.update_one(selector, updator)
        elif action == "delete":
            response = await collection.delete_one(selector)
    finally:
        await client.close()

    return response
