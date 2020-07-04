import requests
from datetime import datetime
from datetime import timedelta
from datetime import date


def return_file_name(file_name):
    return f"https://site.example/api2/repos/repo_name/directory/{file_name}"


def return_dir_name():
    return f"https://site.example/api2/repos/repo_name/directory/"


def return_headers():
    return {
        "Authorization": "Token token",
        "Accept": "application/json; charset=utf-8; indent=4"
           }


def request_api_get_list_of_traces(dir_name, headers):
    return requests.get(dir_name, headers=headers)


def find_outdated_traces(list_of_traces, delta, today):
    results = []
    for i in list_of_traces:
        name = i["name"]
        trace_time = date.fromtimestamp(i["mtime"])
        if (today - delta) > trace_time:
            link = return_file_name(name)
            results.append(link)
    results.sort()
    return results


def write_results_to_file(results):
    with open("traces.txt", "w") as file:
        for element in results:
            file.write(element)
            file.write("\n")


def delete_file(file_name, headers):
    return requests.delete(file_name, headers=headers)


def main():
    delta = timedelta(weeks=1)
    today = date.today()
    start = datetime.now()
    print("Script starts at:", start)
    directory = return_dir_name()
    headers = return_headers()
    list_of_traces = request_api_get_list_of_traces(directory, headers)
    print("Status code of request:", list_of_traces.status_code)
    results = find_outdated_traces(list_of_traces.json(), delta, today)
    write_results_to_file(results)
    cnt = 0
    for i in results:
        delete_file(i, headers)
        cnt += 1
        print(cnt)
    end = datetime.now()
    print("Script starts at:", start)
    print("Script ends at:", end)
    print("Script run time:", end - start)
    print("Traces in repository:", len(list_of_traces.json()))
    print("Traces was deleted:", len(results))
    print("Traces left in repository:", (
            len(list_of_traces.json()) - len(results)))


if __name__ == '__main__':
    main()
