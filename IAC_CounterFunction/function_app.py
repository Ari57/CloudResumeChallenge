import azure.functions as func
from config import GetDatabase

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:

    client = GetDatabase()
    database = client["iac-db"]
    counter = database["website-counter"]

    filter = {"id": "counter"}
    updateDocument = {
        "$inc": {
            "count" : 1
        }
    }
    
    resetDocument = {
        "$set": {
            "count" : 0
        }
    }

    counter.update_one(filter, updateDocument)
    query = {"id": "counter"}
    count = counter.find_one(query)
    result = str(count["count"])
    client.close()
    return func.HttpResponse(result, status_code=200)