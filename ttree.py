# !/usr/bin/python

import urllib2
import sys
from bs4 import BeautifulSoup

visited_tweets = {}


class Tweet:
    def __init__(self, tweet_id, author, content, children):
        self.tweet_id = tweet_id
        self.author = author
        self.content = content
        self.children = children

    def display_tweet(self, indent):
        res = indent + self.author + ": " + self.content + "\n"
        for child in self.children:
            res += child.display_tweet(indent + "  ")
        return res


def find_tweet(tweet_id):
    if tweet_id in visited_tweets:
        return visited_tweets[tweet_id]

    response = urllib2.urlopen("https://twitter.com/statuses/" + str(tweet_id))
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    author = soup.find("div", class_="follow-bar").contents[1]['data-screen-name']
    content = "".join(soup.find("p", class_="TweetTextSize--26px").strings)
    children = []

    for raw_child in soup.find_all("div", class_="ThreadedConversation-tweet"):
        child_tweet = find_tweet(raw_child.contents[1]['data-item-id'])
        if child_tweet.tweet_id not in visited_tweets:
            children.append(child_tweet)
            visited_tweets[child_tweet.tweet_id] = child_tweet
    return Tweet(tweet_id, author, content, children)


print(find_tweet(sys.argv[1]).display_tweet(""))
