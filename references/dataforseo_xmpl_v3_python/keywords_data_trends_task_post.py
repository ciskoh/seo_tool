from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    location_name="United States",
    date_from="2019-01-01",
    date_to="2020-01-01",
    keywords=[
        "seo api"
    ]
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    location_name="United States",
    date_from="2019-01-01",
    date_to="2020-01-01",
    type="youtube",
    category_code=3,
    keywords=[
        "seo api",
        "rank api"
    ],
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    location_name="United States",
    date_from="2019-01-01",
    date_to="2020-01-01",
    type="youtube",
    category_code=3,
    keywords=[
        "seo api",
        "rank api"
    ],
    postback_url="https://your-server.com/postbackscript"
)
# POST /v3/keywords_data/google_trends/explore/task_post
response = client.post("/v3/keywords_data/google_trends/explore/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
