from random import Random
from client import RestClient
# You can download this file from here https://api.dataforseo.com/v3/_examples/python/_python_Client.zip
client = RestClient("login", "password")

rnd = Random()
post_data = dict()
# example #1 - a simple way to set a task
post_data[rnd.randint(1, 30000000)] = dict(
    target="dataforseo.com",
    max_crawl_pages=10
)
# example #2 - a way to set a task with additional parameters
post_data[rnd.randint(1, 30000000)] = dict(
    target="dataforseo.com",
    max_crawl_pages=10,
    load_resources=True,
    enable_javascript=True,
    custom_js="meta = {}; meta.url = document.URL; meta;",
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# POST /v3/on_page/task_post
# the full list of possible parameters is available in documentation
response = client.post("/v3/on_page/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
