from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    location_name="United States",
    keywords=[
        "average page rpm adsense"
    ]
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    language_code="en",
    location_code=2840,
    keywords=[
        "adsense blank ads how long"
    ],
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    location_name="United States",
    language_name="English",
    keywords=[        
        "leads and prospects"
    ],
    postback_url="https://your-server.com/postbackscript"
)
# POST /v3/keywords_data/google/search_volume/task_post
# in addition to 'search_volume' you can also set other parameters
# the full list of possible parameters is available in documentation
response = client.post("/v3/keywords_data/google/search_volume/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
