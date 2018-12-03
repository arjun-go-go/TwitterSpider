# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='twitter_tweets',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=twitter_tweets.settings']},
)