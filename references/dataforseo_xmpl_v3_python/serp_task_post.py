from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# example #1 - a simple way to set a task
# this way requires you to specify a location, a language of search, and a keyword.
post_data[len(post_data)] = dict(
    language_code="en",
    location_code=2840,
    keyword="albert einstein1"
)
# example #2 - a way to set a task with additional parameters
# high priority allows us to complete a task faster, but you will be charged more.
# after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.
post_data[len(post_data)] = dict(
    language_name="English",
    location_name="United States",
    keyword="albert einstein2",
    priority=2,
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# example #3 - an alternative way to set a task
# all the parameters required to set a task are passed via the URL.
# after a task is completed, we will send the results according to the type you specified in the 'postback_data' field to the address you set in the 'postback_url' field.
post_data[len(post_data)] = dict(
    url="https://www.google.co.uk/search?q=einstein3&hl=en&gl=GB&uule=w+CAIQIFISCXXeIa8LoNhHEZkq1d1aOpZS",
    postback_data="html",
    postback_url="https://your-server.com/postbackscript"
)
# POST /v3/serp/google/organic/task_post
# in addition to 'google' and 'organic' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.post("/v3/serp/google/organic/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
