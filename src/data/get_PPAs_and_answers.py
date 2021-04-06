# module to download ppas and answers from SERP api using
# data_for_seo api


# basic class to make requests

from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)

# post - create request

def create_request(credentials, str_list, **kwargs) -> dict:
    """function to create request dictionary for SERP API
    parameters:
    credentials: uname and pw for DataForSeo
    str_list: list of string for the call

    optional named arguments may include:
    language_code: str default "en"
    location_code: int default 2840

    Returns dictionary for call
     """
    client = RestClient(credentials[0], credentials[1])
    post_data = dict()

    # set optional arguments
    if not language_code:
        language_code = "en"
    if not location_code:
        location_code = 2840

    if len(str_list) >= 100:
        raise IndexError("maximum number of question is 100")

    # create dict post_data
    for st_ in str_list:
        post_data[len(post_data)] = dict(
            language_code=language_code,
            location_code=location_code,
            keyword=_st
        )
    return post_data


# get - get response
# TODO: use code below to create function that outputs results
response = client.post("/v3/serp/google/organic/task_post", post_data)
if response['status_code'] == 20000:
    results = []
    for task in response['tasks']:
        print(task.keys())

        # 3 - another way to get the task results by id
        # GET /v3/serp/google/organic/task_get/advanced/$id
        if (task['id']):
            results.append(client.get("/v3/serp/google/organic/task_get/advanced/" + task['id']))
    # print(results[0][0])
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

# extract - extract relevant_data from response
#TODO finish extracting PPAa
if response["status_code"] == 20000:
    for r in response['tasks'][0]['result']:
        print(r.keys())
        for r2 in r["items"]:
            if r2["type"] == "people_also_ask":
                for r3 in r2['items']:
                    print(r2['items'])
            print("\n")
    # do something with result

#TODO create tests for this module