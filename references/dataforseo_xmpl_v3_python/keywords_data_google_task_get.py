from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# in addition to 'search_volume' you can also set other parameters
# the full list of possible parameters is available in documentation
# GET /v3/keywords_data/google/search_volume/tasks_ready
response = client.get("/v3/keywords_data/google/search_volume/tasks_ready")
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response['status_code'] == 20000:
    results = []
    for task in response['tasks']:
        if (task['result'] and (len(task['result']) > 0)):
            for resultTaskInfo in task['result']:
                # 2 - using this method you can get results of each completed task
				# GET /v3/keywords_data/google/search_volume/task_get/$id
                if(resultTaskInfo['endpoint']):
                    results.append(client.get(resultTaskInfo['endpoint']))
                '''
                # 3 - another way to get the task results by id
                # GET /v3/keywords_data/google/search_volume/task_get/$id              
                if(resultTaskInfo['id']):
                    results.append(client.get("/v3/keywords_data/google/search_volume/task_get/" + resultTaskInfo['id']))
                '''
    print(results)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"])) 
