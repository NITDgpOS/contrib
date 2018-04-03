import requests

def get_repositories(username):
    """Returns the repositories of a user using the Github API."""
    repos_url = 'https://api.github.com/users/{}/repos'.format(username)
    response = requests.get(repos_url)
    repos = []
    if response.status_code == 200:
        repos = response.json()
    return repos
