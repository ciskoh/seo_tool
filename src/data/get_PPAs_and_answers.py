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
            response_ready = connection.getresponse()
            return loads(response_ready.read().decode())
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
    if not kwargs.get("credentials"):
        raise FileNotFoundError("missing dataForSEO credentials")
    credentials = kwargs.get("credentials")
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
            keyword=st_ if isinstance(st_, str) else str(st_),
            priority=kwargs.get("priority",1)
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
    server = kwargs.get("server", "/v3/serp/google/organic/task_post")
    response_ready = client.post(server, post_data)
    return response_ready


def check_api_connection(post_data, response) -> list:
    """ checks connection with api by verifying error codes and number of tasks between
    post_data/requests and response
    parameters:
    post_data: dictionary with requests
    response: json response form server

    Returns list of tasks id to be downloaded
    """
    # check status code
    if response['status_code'] != 20000:
        raise ConnectionError(f"Status code is not ok: {response['status_message']}")
    # check
    id_list = []
    for a, b in zip(post_data.values(), response['tasks']):
        if a['keyword'] != b['data']['keyword']:
            raise ConnectionError("task is missing")
        else:
            id_list.append(b['id'])
    return id_list


# TODO: expose sleep time and test computation time with different sleep times
def download_results(client, response_ready, id_list, **kwargs) -> list:
    """download the results requested with send_request
    returns the results as json style list
    parameters:
    client : Restclient object created with create_request
    post_data: dict created with create_request
    id_list: list of id from current request

    Optional parameters:
    server: server to use for request

    returns json style list
    """
    # set optional arguments
    server = kwargs.get("server", "/v3/serp/google/organic/task_get/advanced/")
    if response_ready['status_code'] == 20000:
        results = []
        # this loop ensure that results are collected when they are ready
        count = 0
        while id_list and (count < 1000) :
            if count >= 1:
                print(f"...this might take a while(x {count})... ")
                print(f"...still {len(id_list)} items to go! ")
            count += 1
            for id in id_list:
                temp_res = client.get(server + id)
                if temp_res['tasks'][0]['result']:
                    results.append(temp_res['tasks'][0]['result'][0])
                    id_list.remove(id)
                    break
            time.sleep(0.2)
            if (count == 999) and id_list:
                raise ConnectionError("could not load all results!!!")
        return results
    else:
        print("error. Code: %d Message: %s" % (response_ready["status_code"], response_ready["status_message"]))


# extract - extract relevant_data from response_ready
def extract_results(results, mode, limit=50):
    """extract result from json style list returned by download_results:
    parameters:
    results:  json style - list with results
    mode: str- "ppa" for questions, "organic" for link of answers
    limit: int - max number of items per keyword

    Returns list of lists
    """
    clean_results = {}
    for r in results:
        if mode == "ppa":
            for n, item in enumerate(r['items']):
                if item["type"] == "people_also_ask":
                    ppas = [i['title'] for i in item['items']]
                    clean_results[r['keyword']] = ppas
        if mode == "link":
            links = [item['url'] for item in r['items'] if item['type'] == 'organic']
            clean_results[r['keyword']] = links[:limit]
    return clean_results
    # do something with result


# Main function
def main(str_list, **kwargs):
    if not kwargs.get("credentials"):
        kwargs['credentials'] = get_credentials()
    client, post_data = create_request(str_list, priority=2, **kwargs)
    response = send_request(client, post_data)
    id_list = check_api_connection(post_data, response)
    results = []
    # this cycle downloads the task once they are ready
    while len(results) < len(str_list):
        print("Downloading results...")
        response_ready = client.get("/v3/serp/google/organic/tasks_ready")
        results += download_results(client, response_ready, id_list)
        if len(results) < len(str_list):
            print("...this might take a while...")
            time.sleep(15)
        else:
            print("all queries downloaded!")
    # extract relevant results
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
    import json
    import os

    str_list = ["What is a damselfish?", "where is a damselfish?", "how is a damselfish?"]
    clean_res = main(str_list)
    if not os.path.exists("../../data/raw/clean_results.json"):
        with open("../../data/raw/clean_results.json", "w") as file:
            json.dump(clean_res, file)
    print(clean_res)
