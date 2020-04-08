import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re
import networkx

import warnings


# 3.md: regular expressions #

def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def main():
    warnings.filterwarnings("ignore")

    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    
    # 1.md - authentication #

    # input your credentials here
    consumer_key = 'xxx'
    consumer_secret = 'xxx'
    access_token = 'xxx'
    access_token_secret = 'xxx'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    # 2.md - searching (similar to other 2.md, however rather than using all_tweets directly, the counts of each hashtag are kept track of in a list all_hashtags #
    search_term = "NBA -filter:retweets"

    tweets = tw.Cursor(api.search,
                       q=search_term,
                       lang="en",
                       since='2018-11-01').items(100)

    all_tweets = []
    all_hashtags = {}
    # this loop keeps count of all the hashtags
    for tweet in tweets:
        # note that in 3.md - this statement should be modified to include remove_url
        all_tweets.append(remove_url(tweet.text))
        for hashtag in tweet.entities['hashtags']:
            if hashtag['text'] not in all_hashtags.keys():
                all_hashtags[hashtag['text']] = 1
            else:
                all_hashtags[hashtag['text']] += 1
    print(all_hashtags)
    
    # 4.md - Generating list of most common hashtags into pie chart #
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    pie_hashtags = {"Other": 0}
    hashtag_total = sum(all_hashtags.values())
    for hashtag, num in all_hashtags.items():
        # threshold of 5% to be "allowed" on pie graph
        if num / hashtag_total >= 0.05:
            pie_hashtags['#' + hashtag] = all_hashtags[hashtag]
        else:
            pie_hashtags["Other"] += all_hashtags[hashtag]
    labels = pie_hashtags.keys()
    sizes = pie_hashtags.values()
    
    # 5.md - Plotting chart #
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


main()
