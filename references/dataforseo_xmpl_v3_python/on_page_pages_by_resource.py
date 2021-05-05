from random import Random
from client import RestClient
# You can download this file from here https://api.dataforseo.com/v3/_examples/python/_python_Client.zip

#client = RestClient("login", "password")
client = RestClient("vadym.borovok@gmail.com", "LSx1AEg4cwUEHIGJ")

post_data = dict()
# simple way to get a result
post_data[len(post_data)] = dict(
    id="07281559-0695-0216-0000-c269be8b7592",
    url="https://dataforseo.com/wp-content/plugins/wp-video-lightbox/wp-video-lightbox.css?ver=4.7.18"
)
# POST /v3/on_page/pages_by_resource
# the full list of possible parameters is available in documentation
response = client.post("/v3/on_page/pages_by_resource", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
