from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# get the task results by id
# GET /v3/serp/google/organic/task_get/advanced/$id
# in addition to 'advanced' you can also set other type parameters
# use the task identifier that you recieved upon setting a task
id = "12021127-0696-0087-0000-e7b313697ffc"
response = client.get("/v3/serp/google/organic/task_get/advanced/" + id)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"])) 
