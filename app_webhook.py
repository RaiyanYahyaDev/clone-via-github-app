import json
import sys

import requests
from flask import Flask, request

from clone_repository import *
from generate_jwt import *

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

jwt_token = ""


@app.route('/', methods=["POST"])
def webhook():
    print(request.get_data())
    webhook_data = json.loads(request.get_data())
    if webhook_data['action']:
        logging.info("Webhook triggered with {} action".format(webhook_data['action']))
        if webhook_data['action'] == "added" or "created":
            global jwt_token
            jwt_token = generate_jwt()
            if 'repositories_added' in webhook_data:
                repo_name = webhook_data['repositories_added'][0]['name']
            else:
                repo_name = webhook_data['repositories'][0]['name']
            install_access_token = get_installation_access_token(jwt_token, repo_name,
                                                                 webhook_data['installation']['access_tokens_url'])
            clone_repo(install_access_token, webhook_data['installation']['account']['login'], repo_name)
    logging.info('done')


def get_installation_access_token(jwt_token: str, repo_name: str, installation_token_url: str):
    logging.info("Getting access token for repo {}".format(repo_name))
    github_token_response = requests.post(installation_token_url, headers={"Authorization": "Bearer " + jwt_token,
                                                                           "Accept": "application/vnd.github.machine-man-preview+json"})
    if github_token_response.status_code == 201:
        return github_token_response.json()['token']
    else:
        logging.info("Could not get installation access token. Github responded with a status of {}".format(
            github_token_response.status_code))
        sys.exit(1)


if __name__ == '__main__':
    app.run(debug=True)
