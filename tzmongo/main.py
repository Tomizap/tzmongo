import pprint
from bson import ObjectId
from colorama import Fore, Style
from pymongo import MongoClient

# Définir l'URI de connexion
uri = "mongodb+srv://tom:jHq13Y2ru1y5Dijb@cluster0.crkabz3.mongodb.net/?retryWrites=true&w=majority"

# Créer un client MongoClient avec une configuration pour définir la version de l'API stable
client = MongoClient(uri)

def mongo(config={}) -> dict:
    # print("mongo")
    response = {
        "ok": False,
        "message": "rien ne s'est produit",
        "data": []
    }

    db = config.get("db", "tools")
    col = config.get("collection", "users")
    action = config.get("action", "get")
    selector = config.get("selector", {})
    # selector["userAccess"] = { "$in": ["zaptom.pro@gmail.com"] }
    updator = config.get("updator")

    _id = selector.get('_id') if selector.get('_id') is not None else config.get("_id")
    if _id is not None:
        selector['_id'] = ObjectId(_id)
    # selector["userAccess"] = { "$in": ["zaptom.pro@gmail.com"] }

    updator = config.get("updator")

    try:
        print(f"Se connecter à MongoDB")
        client.start_session()
        print(f"Connecté à MongoDB {db} {col}")
        collection = client[db][col]

        if action.lower() in ('get', 'read'):
            response['data'] = list(collection.find(selector))

        elif action.lower() in ("add", "create", 'post'):
            creating = collection.insert_one(selector)
            response['ok'] = creating.acknowledged
            if response['ok'] == True:
                response['message'] = "Le document à bien été créé"
                response['data'] = response['data'] = list(collection.find({'_id': creating.inserted_id}))[0]
            else:
                response['message'] = 'Un probleme est survenu lors de la création du document'
                response['ok'] = False

        elif action.lower() in ('put', 'edit'):
            updating = collection.update_one(selector, updator)

            response['ok'] = updating.acknowledged
            if response['ok'] == False:
                response['message'] = 'Un probleme est survenu lors de la création du document'
                response['ok'] = False
                return response
            
            if updating.matched_count == 0:
                response['ok'] = False
                response['message'] = 'Aucun document trouvé'
            elif updating.matched_count == 1:
                response['message'] = "Le document à bien été modifié"
                response['data'] = list(collection.find({'_id': selector.get('_id')}))[0]
            else:
                response['message'] = "Les documents ont bien été modifiés"
                

        elif action.lower() in ("delete"):
            response['ok'] = collection.delete_one(selector).acknowledged
            if response['ok'] == True:
                response['message'] = 'le document a bien été détruit'
            else:
                response['message'] = 'le document n\'a pas été détruit'

        else:
            response['ok'] = False
            response['message'] = f'action "{action}" n\'existe pas'
            print(Fore.RED + response['message'])
        
        print(Style.RESET_ALL)

    except Exception as e:
        response['ok'] = False
        response['message'] = "Error: " + str(e)
        print(Fore.RED + response['message'])
        print(Style.RESET_ALL)

    # finally:
    #     client.close()

    response['client'] = client

    return response