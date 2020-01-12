"""Reddit Saver

Script that allows the user to gather information about posts on the website
www.reddit.com.

This tool allows for a wide range of sorting parameters and if selected
it will save the information it gathers on the specified output path.
"""


import praw
import pandas as pd
import datetime as dt
import requests
import os


# TODO, check for duplicate posts in csv file and not just images
# TODO, add the possibility to save > 1000 posts at the time
# TODO, split this function into multiple smaller chunks


def save_subreddit(**kwargs):
    """Scrapes the website www.reddit.com.

    Loops through a list of posts based on a wide range of
    parameters and appends the results to a queue when it is finished.

    If selected it will also save images it finds aswell as creating
    a CSV file with the each posts information.

    :param kwargs:
    :return None:
    """
    kw = kwargs
    print("reached")

    # Create a reddit instance with valid credentials
    reddit = praw.Reddit(client_id=kw["client_id"],
                         client_secret=kw["client_secret"],
                         user_agent=kw["user_agent"])

    # Intialize a dict to store as a csv file
    info_dict = {
        "title": [],
        "selftext": [],
        "score": [],
        "num_comments": [],
        "created": [],
        "url": [],
        "id": [],
    }

    # Keep track of how the save went
    save_results = {
        "Images saved": 0,
        "Duplicate images": 0,
        "Posts with invalid/no image": 0,
        "CSV entries saved": 0,
        "Invalid posts": 0
    }

    # Get all the posts that fit the specified parameters
    subreddit = reddit.subreddit(kw["subreddit"])
    if kw["sort"] in ["hot", "new", "rising"]:
        posts = (getattr(subreddit, kw["sort"])(limit=kw["amount"]))
    else:
        posts = (getattr(subreddit, kw["sort"])(limit=kw["amount"], time_filter=kw["time"]))

    # Set a path to the save folder
    if kw["subfolder"]:
        _imagepath = f"{kw['imagepath']}/{kw['subreddit']}Images/"
        _csvpath = f"{kw['csvpath']}/{kw['subreddit']}CSV/"
    else:
        _imagepath = f"{kw['imagepath']}/"
        _csvpath = f"{kw['csvpath']}/"

    if not os.path.exists(_imagepath) and kw["save_img"]:
        os.makedirs(_imagepath)
    if not os.path.exists(_csvpath) and kw["save_csv"]:
        os.makedirs(_csvpath)

    # Loop through each post found in the specified subreddit
    for submission in posts:

        # Keep track of the state of the post
        invalid_post = False
        duplicate_image = False

        # Check for keywords in the title
        if kw["keywords"]:
            match = False
            for word in kw["keywords"]:
                if word.lower() in submission.title.lower() or submission.selftext.lower():
                    match = True
            if not match:
                invalid_post = True

        # Remove bad characters
        file_name = f"{submission.title[:50]} § {submission.score} § {submission.id}"
        for ch in ['\\', '/', '"', '?', '*', '<', '>', '|', ':', '[', ']', "."]:
            if ch in file_name:
                file_name = file_name.replace(ch, "")

        # Check if post is allready saved as image
        for file in os.listdir(_imagepath):
            if "§" in file:
                if submission.id in file.split("§")[2]:
                    duplicate_image = True

        # Check for score requirements
        if kw["min_score"]:
            if not submission.score > kw["min_score"]:
                invalid_post = True
        if kw["max_score"]:
            if not submission.score < kw["max_score"]:
                invalid_post = True

        if not invalid_post:
            # Save images to folder if the save_img parameter is true
            if kw["save_img"]:
                if not duplicate_image:
                    if "i.redd.it" in submission.url:
                        with open(_imagepath + file_name + ".jpg", 'wb') as f:
                            f.write(requests.get(submission.url).content)
                            save_results["Images saved"] += 1
                    else:
                        save_results["Posts with invalid/no image"] += 1
                else:
                    save_results["Duplicate images"] += 1

            if kw["save_csv"]:

                # Append information about the post to the dict if the save_csv parameter is true
                for value in info_dict:
                    if value == "created":
                        info_dict[value].append(dt.datetime.fromtimestamp(getattr(submission, value)))
                    else:
                        info_dict[value].append(getattr(submission, value))
                save_results["CSV entries saved"] += 1
        else:
            save_results["Invalid posts"] += 1

        # Send a progress status to the GUI update queue
        total = 0
        total += save_results["Images saved"]
        total += save_results["Duplicate images"]
        total += save_results["Invalid posts"]
        total += save_results["Posts with invalid/no image"]
        progress = round((total / posts.limit) * 100)
        kw["queue"].put({"progress": progress})

    # Create a dataframe with the post information and then create a csv file with said dataframe
    if kw["save_csv"]:
        data = pd.DataFrame(info_dict)
        files = os.listdir(_csvpath)
        data.to_csv(f"{_csvpath}{str(subreddit)}-{str(len(files))}.csv", mode="a", header=False)

    kw["queue"].put(save_results)
    print(f"Successfully saved r/{subreddit}")
