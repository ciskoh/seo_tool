from random import Random
from client import RestClient
# You can download this file from here https://api.dataforseo.com/v3/_examples/python/_python_Client.zip
client = RestClient("login", "password")

# using this method you can get summary for task
# GET /v3/on_page/summary/$id
id = "07281559-0695-0216-0000-c269be8b7592"
response = client.get("/v3/on_page/summary/" + id)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"])) 