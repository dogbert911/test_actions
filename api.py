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
    os.getenv('GITHUB_REPOSITORY')

    headers = {'authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}',
               'content-type': 'application/json'}

    url = f'https://api.github.com/repos/{os.getenv("GITHUB_REPOSITORY")}/actions/runs/{os.getenv("GITHUB_RUN_ID")}/jobs'

    response = make_request(url=url, request_method="GET", headers=headers)
    print(response)




if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)