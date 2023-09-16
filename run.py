from tzmongo import mongo


# m = mongo({
#     "action": 'add',
#     "selector": {
#         "email": "test"
#     }
# })
# print(m)

m = mongo({
    "db": 'storage',
    "collection": "tables",
    "action": "edit",
    "selector": {"_id": "65058f69a2556d1dca881977"},
    "updator": {
      "$push": {
        'data': {
          'salut': 'toi'
        }
      }
    }
})
print(m)
