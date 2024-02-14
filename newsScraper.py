#import os
import requests
from bs4 import BeautifulSoup
import json
import re
import csv

# headers = {"Authorization": "Bearer" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZDAzZDdkNmYtNmEzYy00YzZjLWI1NWMtOTU4MWM5MmFkZmI5IiwidHlwZSI6ImFwaV90b2tlbiJ9.cVgfXIwX5QZklAj1xoPSz4wCP1GfjRFutUeguyS-mQc"}
# AIurl = "https://api.edenai.run/v2/text/summarize"
# payload = {
#     "providers": "microsoft,connexun",
#     "language": "en",
#     "text": "Linux is a family of open-source Unix-like operating systems based on the Linux kernel, an operating system kernel first released on September 17, 1991, by Linus Torvalds. Linux is typically packaged in a Linux distribution.",
#     "fallback_providers": ""
# }

#TODO:
# Summarize news stories with Open AI API
class SummarizedNews:
    def __init__(self):
        """
        Constructor for initializing the object.
        """
        self.articleLinks = []
        self.articleTexts = []

    def scrapeArticleLinks(self, numArticles):
        """
        This function scrapes the CNBC website for the top specified number of news stories and gets the list of links to summarize.

        It adds to the newsLinks attribute.
        """
        link = "https://www.cnbc.com"
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')

        htmlClassHeadlines = soup.find_all('a', class_='LatestNews-headline')

        for i in range(0, numArticles):
            self.articleLinks.append(htmlClassHeadlines[i]['href'])

    #def summarizeText(self):

    def scrapeArticleTexts(self, numArticles):
        """
        Gathers the text of each article link.
        """
        for i in range(0, numArticles):
            html = requests.get(self.articleLinks[i])
            soup = BeautifulSoup(html.text, 'html.parser')

            htmlGroups = soup.find_all('div', class_='group')
            articleText = ""

            for i in range(0, len(htmlGroups)):
                htmlParagraphs = htmlGroups[i].find_all('p')
                articleTextSection = '\n'.join([htmlParagraphs.get_text() for htmlParagraphs in htmlParagraphs])

                articleText += articleTextSection

            self.articleTexts.append(articleText)




news = SummarizedNews()
news.scrapeArticleLinks(10)
news.scrapeArticleTexts(10)
for i in range(0, 10):
    print(news.articleTexts[i])
    print("\n")
