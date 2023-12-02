from tzmongo import mongo


# m = mongo({
#     "action": 'add',
#     "selector": {
#         "email": "test"
#     }
# })
# print(m)

# m = mongo({
#     "db": 'storage',
#     "collection": "tables",
#     "action": "edit",
#     "selector": {"_id": "65058f69a2556d1dca881977"},
#     "updator": {
#       "$push": {
#         'data': {
#           'salut': 'toi'
#         }
#       }
#     }
# })
# print(m)

m = mongo({
    'collection': 'automnations',
    "action": 'edit',
    "selector": {
        "_id": "64f91b86bd602b8bd6d2ea76"
    },
    'updator': {
        "$push": {
            "data": {"salut": 'toi'}
        }
    }
})
print(m)
