# module to download ppas and answers from SERP api using
# data_for_seo api


# basic class to make requests

from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import time
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
            headers = {'Authorization': 'Basic %s' % base64_bytes}
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
def get_credentials(service_name="dataforSeo", uname="matteo.jriva@gmail.com"):
    """gets api credentials using keyring
    returns a list [user name, password]"""
    pw = keyring.get_password(service_name, uname)
    return [uname, pw]


def create_request(str_list, **kwargs):
    """function to create request dictionary for SERP API
    parameters:
    credentials: uname and pw for DataForSeo
    str_list: list of string for the call

    optional named arguments may include:
    language_code: str default "en"
    location_code: int default 2840

    Returns dictionary for call
     """
    # set optional arguments
    credentials = kwargs.get("credentials", get_credentials())
    language_code = kwargs.get("language_code", "en")
    location_code = kwargs.get("location_code", 2840)
    # check str_list
    if len(str_list) >= 100:
        raise IndexError("maximum number of question is 100")
    # create request
    client = RestClient(credentials[0], credentials[1])
    # create dict post_data
    post_data = dict()
    for st_ in str_list:
        post_data[len(post_data)] = dict(
            language_code=language_code,
            location_code=location_code,
            keyword=st_
        )
    return client, post_data

def send_request(client, post_data, **kwargs):
    """uses a dict to create a request on dataforSeo api
    parameters:
    client : Restclient object created with create_request
    post_data: dict created with create_request

    Optional parameters:
    server: server to use for request

    returns json style list"""
    # set optional arguments
    server = kwargs.get("server", "/v3/serp/google/organic/")
    post_server = server + "task_post"
    get_server = server + "task_get/advanced/"
    response = client.post(post_server, post_data)
    return response

# get - get response
# TODO: use code below to create function that outputs results$
def download_results(client, response, **kwargs) -> list:
    """download the results requested with send_request
    returns the results as json style list
    parameters:
    client : Restclient object created with create_request
    post_data: dict created with create_request

    Optional parameters:
    server: server to use for request

    returns json style list
    """
    # set optional arguments
    server = kwargs.get("server", "/v3/serp/google/organic/")
    post_server = server + "task_post"
    get_server = server + "task_get/advanced/"

    if response['status_code'] == 20000:
        results = []
        for task in response['tasks']:
            if task['id']:
                # this loop ensure that results are actually collected
                for n in range(100):
                    temp_res = client.get(get_server + task['id'])
                    if temp_res['tasks'][0]['result']:
                        print(f"downloaded results for a question")
                        results.append(temp_res['tasks'][0])
                        break
                    else:
                        if n == 0:
                            print("...this might take a while...")
                        # time.sleep(0.5)
        return results
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))


# extract - extract relevant_data from response
def extract_results(results, mode):
    """extract result from json style list returned by download_results:
    parameters:
    results:  json style list with results
    mode: "ppa" for questions, "organic" for link of answers
    returns list of lists
    """
    clean_results = []
    for r in results:
        if mode == "ppa":
            for n, item in enumerate(r['result'][0]['items']):
                if item["type"] == "people_also_ask":
                    ppas = [i['title'] for i in item['items']]
                    clean_results.append(ppas)
        if mode == "link":
            clean_results.append([item['url'] for item in r['result'][0]['items'] if item['type']=='organic'])
    return clean_results
    # do something with result

# Main function
def main(str_list, **kwargs):
    print(f" collecting results for {len(str_list)} questions")
    # get results from REST API
    # request data from api & download results
    client, post_data = create_request(str_list)
    response = send_request(client, post_data)
    results = download_results(client, response)
    # todo insert error here in case results do not appear

    #extract relevant results
    clean_results = {}
    if not kwargs.get("mode"):
        clean_results['ppa'] = extract_results(results, mode="ppa")
        clean_results['link'] = extract_results(results, mode="link")
    else:
        clean_results[kwargs.get("mode")] = extract_results(results, mode=kwargs.get("mode"))

    for k in clean_results:
        print(f"downloaded {k}s for {len(clean_results[k])} questions")
    return clean_results


if __name__ == '__main__':
    # TODO test this module

    str_list = ["What is a damselfish?"] * 3
    main(str_list)
