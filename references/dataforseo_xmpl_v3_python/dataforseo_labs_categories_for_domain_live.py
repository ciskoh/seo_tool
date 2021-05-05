from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    target="dataforseo.com",
    location_name="United States",
    language_name="English",
    filters=[
        ["metrics.organic.count", ">=", 100],
        "and", 
        [
            ["metrics.organic.pos_1", ">", 0],
            "or",
            ["metrics.paid.count", "in", [ 1, 2 ]]
        ]
    ]
)
# POST /v3/dataforseo_labs/categories_for_domain/live
response = client.post("/v3/dataforseo_labs/categories_for_domain/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
