import logging
import subprocess

logging.basicConfig(level=logging.INFO)


def clone_repo(installation_access_token: str, owner: str, repo: str):
    p = subprocess.Popen(
        'git clone https://x-access-token:{}@github.com/{}/{}.git'.format(installation_access_token, owner, repo),
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logging.info(line)
