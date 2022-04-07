#!/usr/bin/env python3
import os
import sys

import requests
from requests.models import Response


def make_request(url: str, request_method: str = "GET", critical: bool = True, **kwargs) -> Response:
    try:
        response: Response = requests.request(method=request_method, url=url, **kwargs)
        response.raise_for_status()
        return response
    except requests.RequestException as error:
        text = f"Error opening URL, got '{type(error).__name__}' with following message:\n{error}"
        print(text)


def main():
    headers = {'authorization': f'Bearer {os.getenv("_TOKEN")}',
               'content-type': 'application/json'}

    url = f'https://api.github.com/repos/{os.getenv("GITHUB_REPOSITORY")}/actions/runs/{os.getenv("GITHUB_RUN_ID")}/jobs'

    r = make_request(url=url, request_method="GET", headers=headers)

    jobs = r.json()['jobs']
    for job in jobs:
        if job['name'] == os.getenv('GITHUB_JOB'):
            check_run_url = job['check_run_url']
            break

    data = {
        'name': 'GREAT NAME',
        'conclusion': 'failure',
        'output': {
            'title': 'MEGA TITLE',
            'summary': 'multiline\n summary\njob\naa',
            'text': 'additional text'
        }
    }

    r = make_request(url=check_run_url, request_method="PATCH", headers=headers, json=data)

    print(check_run_url)
    print('==============================')
    print(r.status_code)
    print('==============================')
    print(r.json())




if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)