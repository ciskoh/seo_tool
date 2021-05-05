from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# example #1 - a simple way to set a task
post_data[len(post_data)] = dict(
    target="dataforseo.com"
)
# example #2 - a way to set a task with additional parameters
# this way you need to specify a domain of the website in the field "target".
# after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.
post_data[len(post_data)] = dict(
    target="dataforseo.com",
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# POST /v3/traffic_analytics/similarweb/task_post
response = client.post("/v3/traffic_analytics/similarweb/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
