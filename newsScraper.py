import requests
from bs4 import BeautifulSoup
import json
import time



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

        Parameters:
            numArticles: Number of articles you want to get links from.
        """
        link = "https://www.cnbc.com"
        html = requests.get(link)

        if html.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {html.status_code}")
            return

        soup = BeautifulSoup(html.text, 'html.parser')

        htmlClassHeadlines = soup.find_all('a', class_='LatestNews-headline')

        for i in range(0, numArticles):
            self.articleLinks.append(htmlClassHeadlines[i]['href'])

    def summarizeText(self, text):
        """
        Returns the summary of a passed in article.

        Parameters:
            text: A string that you want to be summarized, preferably an article.

        Returns:
            The AI result in a string.
        """
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZDAzZDdkNmYtNmEzYy00YzZjLWI1NWMtOTU4MWM5MmFkZmI5IiwidHlwZSI6ImFwaV90b2tlbiJ9.cVgfXIwX5QZklAj1xoPSz4wCP1GfjRFutUeguyS-mQc"}
        AIurl = "https://api.edenai.run/v2/text/summarize"
        payload = {
            "providers": "openai",
            "language": "en",
            "text": text,
            "num_sentences": 5,
            "fallback_providers": "cohere, alephalpha, emvista, nlpcloud"
        }

        response = requests.post(AIurl, json=payload, headers=headers)

        result = json.loads(response.text)

        return result['openai']['result']

    def scrapeArticleTexts(self, numArticles):
        """
        Gathers the text of each article link.

        Parameters:
            numArticles: Number of articles you want to get text from.
        """
        for i in range(0, numArticles):
            html = requests.get(self.articleLinks[i])
            soup = BeautifulSoup(html.text, 'html.parser')

            if html.status_code != 200:
                print(f"Failed to retrieve the page. Status code: {html.status_code}")
                return

            htmlGroups = soup.find_all('div', class_='group')
            articleText = ""

            for i in range(0, len(htmlGroups)):
                htmlParagraphs = htmlGroups[i].find_all('p')
                articleTextSection = '\n'.join([htmlParagraphs.get_text() for htmlParagraphs in htmlParagraphs])

                articleText += articleTextSection

            self.articleTexts.append(articleText)

    def storeSummaries(self):
        """
        Writes all article summaries to a text file.
        """
        f = open("summaries.txt", "w+")
        f.close()

        for i in range(0, len(self.articleTexts)):
            f = open("summaries.txt", "a")
            f.write("Link: ")
            f.write(self.articleLinks[i])
            f.write("\nSummary: \n")
            f.write(self.summarizeText(self.articleTexts[i]).replace(". ", ".\n"))

            time.sleep(3)
            f.write("\n\n\n")

            f.close()



news = SummarizedNews()
news.scrapeArticleLinks(5)
news.scrapeArticleTexts(5)
news.storeSummaries()
