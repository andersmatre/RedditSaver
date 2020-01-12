"""Input Verifier

Module containing the verify_inputs() that checks whether the
given inputs are valid or not.
"""


import praw
from prawcore import NotFound
from prawcore import OAuthException


def verify_inputs(**kwargs):
    """Checks if inputs are valid

    This function is used to check whether the given inputs
    are valid or not. In particular it is used in conjuction with the
    save_subreddit(). This is done to avoid starting a thread and then
    immediately exiting out of it if the inputs are invalid.

    This also gives an easier way to notify the user that the
    inputs are invalid via the GUI.

    :param kwargs:
    :return:
    """
    kw = kwargs
    valid = True

    if not kw["subreddit"]:
        valid = False
    else:
        reddit = praw.Reddit(client_id=kw["client_id"],
                             client_secret=kw["client_secret"],
                             user_agent=kw["user_agent"])

        for subreddit in kw["subreddit"].split("+"):
            try:
                reddit.subreddits.search_by_name(subreddit, exact=True)
            except NotFound:
                valid = False

    try:
        pass  # FIXME
        # logic to check for valid reddit credentials goes here
    except OAuthException:
        valid = False

    try:
        pass  # FIXME
        # Logic to check if paths are goes here
    except OSError:
        valid = False

    if valid:
        return True
    else:
        return False
