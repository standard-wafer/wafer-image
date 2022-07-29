from ariadne import QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
import uvicorn
import pymongo
import os

# mongo client
conn_str = os.environ['MONGODB_URL']
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

type_defs = gql("""
    type Query {
        todo: String!
    }

    type Mutation {
        create_todo(title: String!): String!
    }
""")

query = QueryType()
mutation = MutationType()

@query.field("todo")
def resolve_todo(_, info):
    request = info.context["request"]
    try:
        mydb = client["testdb"]
        mycol = mydb["testtbl"]

        x = mycol.find_one()
        return x["title"]

    except Exception:
        return "Unable to connect to the server."

@mutation.field("create_todo")
def resolve_create_todo(_, info, title):
    
    try:
        mydb = client["testdb"]
        mycol = mydb["testtbl"]
        mydict = { "title": title }
        x = mycol.insert_one(mydict)

        return title

    except Exception:
        return "Unable to connect to the server."


schema = make_executable_schema(type_defs, query, mutation)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")