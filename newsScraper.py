#import os
import requests
from bs4 import BeautifulSoup
import re
import csv

#TODO:
# Summarize news stories with Open AI API
class SummarizedNews:
    def __init__(self):
        """
        Constructor for initializing the object.

        This function creates the `newsLinks` attribute as an empty list to store news links.
        """
        self.newsLinks = []

    def scrapeNewsLinks(self):
        """
        This function scrapes the CNBC website for the top 10 news stories and gets the list of links to summarize.

        It adds to the newsLinks attribute.
        """
        url = f'https://www.cnbc.com'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            htmlHeadlines = soup.find_all('a', class_='LatestNews-headline')

            for i in range(0, 10):
                self.newsLinks.append(htmlHeadlines[i]['href'])
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    def summarizeNewsLink(self):





news = SummarizedNews()
news.scrapeNewsLinks()
print(news.newsLinks)
