import requests
from pytz import UTC as utc
from datetime import datetime

from django.conf import settings
from django.utils import timezone
from core.models import UserProfile, Repository


def get_repositories(username):
    """Returns the repositories of a user using the Github API."""
    repos_url = 'https://api.github.com/users/{}/repos?\
    per_page=100&page='.format(username)
    page = 1
    repos = []
    while True:
        response = requests.get(repos_url+str(page))
        if response.status_code == 200:
            if len(response.json()) == 0:
                break
            repos.extend(response.json())
            if len(response.json()) < 100:
                break
        page += 1
    return repos


def update_contributions(user_profile):
    """Counts the number of contributions of the user. Contribution is counted
    only when
      1. Committing to a non-forked repository's default or gh-pages branch.
      2. Opening an issue.
      3. Proposing a pull request.
      4. Reviewing a pull request.
      5. Co-authoring a commit on a repository's default or gh-pages branch.
      6. Creating a repository.
      7. Creating a repository by forking.
    For now, the master branch is treated as the default branch."""
    contribution_events = {
        # Triggered on a push to a repository branch
        "PushEvent": push_contributions,

        # Triggered when an issue is assigned, unassigned, labeled, unlabeled,
        # opened, edited, milestoned, demilestoned, closed, or reopened
        "IssuesEvent": issues_contributions,

        # Triggered when a pull request is assigned, unassigned, labeled,
        # unlabeled, opened, edited, closed, reopened, or synchronized,
        # also when a pull request review is requested or removed
        "PullRequestEvent": pull_request_contributions,

        # Triggered when a pull request review is submitted into a
        # non-pending state, the body is edited, or the review is dismissed
        "PullRequestReviewEvent": pull_request_review_contributions,

        # Triggered when a repository, branch, or tag is created
        "CreateEvent": creation_contributions,

        # Triggered when the user forks a repository
        "ForkEvent": fork_creation_contributions,
    }

    update_timestamp = user_profile.last_updated
    if not update_timestamp:
        # Initialise the timestamp as the first of the current month
        update_timestamp = utc.localize(
            datetime(year=datetime.today().year,
                     month=datetime.today().month,
                     day=1)
        )

    page = 1
    username = user_profile.user.username
    looping = True
    contributions = 0

    while looping:
        events_url = 'https://api.github.com/users/{}/events?page={}\
                     &client_id={}&client_secret={}'.format(
                        username, page, settings.SOCIAL_AUTH_GITHUB_KEY,
                        settings.SOCIAL_AUTH_GITHUB_SECRET
                     )
        response = requests.get(events_url)
        if response.status_code == 200:
            events = response.json()
            for event in events:
                event_timestamp = utc.localize(
                    datetime.strptime(event['created_at'],
                                      "%Y-%m-%dT%H:%M:%SZ")
                )
                if event_timestamp < update_timestamp:
                    looping = False
                    break
                e = event['type']
                if e in contribution_events:
                    contributions += contribution_events[e](event)
        else:
            looping = False
        page += 1

    user_profile.contributions += contributions
    user_profile.last_updated = timezone.now()
    user_profile.save()


def push_contributions(event):
    """Function to count contributions attributed to pushing commits.
    Return number of distinct commits if pushed to non-forked repository's
    master or gh-pages branch, 0 otherwise."""

    repo = event['repo']['name']
    username = event['actor']['login']

    try:
        name = UserProfile.objects.get(user__username=username).name
    except UserProfile.DoesNotExist:
        name = ""
    count = 0

    # Try to check if the repository is in database and if it is forked
    try:
        forked = Repository.objects.get(repo=repo).is_fork

    # The repo belongs to an organisation the user is a part of
    except Repository.DoesNotExist:
        forked = False

    if not forked:
        branch = event['payload']['ref'].split('/')[-1]
        if branch in ['master', 'gh-pages']:
            for commit in event['payload']['commits']:
                if commit['author']['name'] in [name, username]:
                    count += 1

    return count


def issues_contributions(event):
    """Function to count contributions attributed to opening an issue.
    Return 1 if an issue is opened, 0 otherwise."""
    count = 0
    if event['payload']['action'] == 'opened':
        count += 1
    return count


def pull_request_contributions(event):
    """Function to count contributions attributed to opening a pull request.
    Return 1 if a pull request is opened, 0 otherwise."""
    count = 0
    if event['payload']['action'] == 'opened':
        count += 1
    return count


def pull_request_review_contributions(event):
    """Function to count contributions attributed to submitting a pull request
    review. Return 1 if a PR review request is submitted, 0 otherwise."""
    count = 0
    if event['payload']['action'] == 'submitted':
        count += 1
    return count


def creation_contributions(event):
    """Function to count contributions attributed to creating a repository.
    Return 1 if a repository has been created, 0 otherwise. Also save the
    repository object in the database."""
    count = 0
    if event['payload']['ref_type'] == 'repository':
        repo = event['repo']['name']
        username = event['actor']['login']
        try:
            user = UserProfile.objects.get(user__username=username)
            Repository.objects.create(owner=user, repo=repo)
        except UserProfile.DoesNotExist:
            pass
        count += 1

    return count


def fork_creation_contributions(event):
    """Function to count contributions attributed to creating a repository by
    forking. Return 1 and save the repository object in the database."""
    repo = event['payload']['forkee']['full_name']
    username = event['actor']['login']
    try:
        user = UserProfile.objects.get(user__username=username)
        Repository.objects.create(owner=user, repo=repo, is_fork=True)
    except UserProfile.DoesNotExist:
        pass

    return 1
