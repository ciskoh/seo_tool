from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# You can set only one task at a time
post_data[len(post_data)] = dict(
    target="dataforseo.com"
)
# POST /v3/traffic_analytics/similarweb/live
response = client.post("/v3/traffic_analytics/similarweb/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
