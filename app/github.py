import time

import jwt
import requests
from django.conf import settings

REPO_NAME = "django-forge/forge-pro"


def get_github_session():
    """
    Gets an authenticated session as the specific app installation
    with access to the django-forge repo
    """
    time_since_epoch_in_seconds = int(time.time())

    payload = {
        "iat": time_since_epoch_in_seconds,
        "exp": time_since_epoch_in_seconds + (10 * 60),
        "iss": settings.GITHUB_APP_ID,
    }

    actual_jwt = jwt.encode(payload, settings.GITHUB_APP_PRIVATE_KEY, algorithm="RS256")

    response = requests.post(
        f"https://api.github.com/app/installations/{settings.GITHUB_APP_INSTALLATION_ID}/access_tokens",
        headers={"Authorization": f"Bearer {actual_jwt}"},
    )
    response.raise_for_status()
    token = response.json()["token"]

    session = requests.Session()
    session.headers.update(
        {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    )
    return session


# TODO staff view to show outstanding invitations?
# https://docs.github.com/en/rest/reference/collaborators#invitations


def invite_username_to_repo(username):
    """
    You are limited to sending 50 invitations to a repository per 24 hour period.
    https://docs.github.com/en/rest/reference/collaborators#add-a-repository-collaborator
    """
    response = get_github_session().put(
        f"https://api.github.com/repos/{REPO_NAME}/collaborators/{username}",
        json={"permission": "pull"},
    )
    response.raise_for_status()


def remove_username_from_repo(username):
    response = get_github_session().delete(
        f"https://api.github.com/repos/{REPO_NAME}/collaborators/{username}",
    )
    response.raise_for_status()


def get_deploy_keys_for_repo():
    """
    https://docs.github.com/en/rest/reference/repos#list-deploy-keys
    """
    next_url = f"https://api.github.com/repos/{REPO_NAME}/keys"
    keys = []
    while next_url:
        response = get_github_session().get(next_url, params={"per_page": 100})
        response.raise_for_status()
        keys += response.json()
        next_url = response.links.get("next", {}).get("url")
    return keys


def add_deploy_key_to_repo(public_key, title):
    """
    https://docs.github.com/en/rest/reference/repos#add-a-deploy-key
    """
    response = get_github_session().post(
        f"https://api.github.com/repos/{REPO_NAME}/keys",
        json={"key": public_key, "title": title, "read_only": True},
    )
    response.raise_for_status()


def remove_deploy_key_from_repo(public_key):
    """
    https://docs.github.com/en/rest/reference/repos#remove-a-deploy-key
    """
    for key in get_deploy_keys_for_repo():
        if key["key"] == public_key:
            response = get_github_session().delete(
                f"https://api.github.com/repos/{REPO_NAME}/keys/{key['id']}"
            )
            response.raise_for_status()
            return

    raise ValueError(f"Deploy key not found on repo: {public_key}")
