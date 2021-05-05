from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    keyword="phone",
    location_name="United States",
    language_name="English",
    filters=[
        ["keyword_data.impressions_info.ad_position_average", ">", 1],
        "and", 
        [
            ["keyword_data.impressions_info.cpc_max", "<", 0.5],
            "or",
            ["keyword_data.impressions_info.daily_clicks_max", ">=", 10]
        ]
    ]
)
# POST /v3/dataforseo_labs/related_keywords/live
response = client.post("/v3/dataforseo_labs/related_keywords/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
