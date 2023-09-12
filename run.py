from tzmongo.main import mongo


m = mongo({
    "action": 'add',
    "selector": {
        "email": "test"
    }
})
print(m)
