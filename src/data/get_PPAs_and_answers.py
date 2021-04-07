# module to download ppas and answers from SERP api using
# data_for_seo api


# basic class to make requests

from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import keyring

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
def get_credentials(service_name = "dataforSeo", uname = "matteo.jriva@gmail.com"):
    """gets api credentials using keyring
    returns a list [user name, password]"""
    pw = keyring.get_password(service_name, uname)
    return [uname, pw]


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
    credentials = get_credentials()
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
    return client, post_data


# get - get response
# TODO: use code below to create function that outputs results$
def get_response(client, post_data, server ="/v3/serp/google/organic/task_post" ) -> dict:
    """uses a dict to create a request on dataforSeo api and returns the results as json
    parameters:
    client : Restclient object created with create_request
    post_data: dict created with create_request
    server: server to use for request

    returns json style list
    """
    response = client.post("/v3/serp/google/organic/task_post", post_data)
    if response['status_code'] == 20000:
        results = []
        for task in response['tasks']:
            print(task.keys())

            # 3 - another way to get the task results by id
            # GET /v3/serp/google/organic/task_get/advanced/$id
            if (task['id']):
                results.append(client.get("/v3/serp/google/organic/task_get/advanced/" + task['id']))
        return results
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

# extract - extract relevant_data from response
def extract_results(results, mode):
    """extract result from json style list returned by get_response:
    parameters:
    results:  json style list with results
    mode: "ppa" for questions, "link" for link of answers
    returns list of lists
    """
    for task in results['tasks']:
        clean_results=[]
        for r in task['result']:
            print(r.keys())
            if mode == "ppa":
                for r2 in r["items"]:
                    if r2["type"] == "people_also_ask":
                        for r3 in r2['items']:
                            print(r2['items'])
                            clean_results.append([r2['items']])
            if mode == "link":
                pass
            return clean_results
    # do something with result

def get_ppa_and_answers(str_list, **kwargs):
    client, post_data = create_request(str_list)
    results = get_response(client, post_data, **kwargs)
    extract_results(results,mode = "ppa")


if __name__ == '__main__':
    # TODO test this module

    str_list = [ "bla" + str(a) for a in range(10) ]
