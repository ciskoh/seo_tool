from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    location_code=1023191,
    language_code="en",
    keyword="RustyBrick, Inc."
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    location_name="New York,New York,United States",
    language_name="English",
    keyword="RustyBrick, Inc.",
    priority=2,
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# POST /v3/business_data/google/my_business_info/task_post
response = client.post("/v3/business_data/google/my_business_info/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
