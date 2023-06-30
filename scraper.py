import requests
from bs4 import BeautifulSoup
import pandas as pd


class Scraper:
    def __init__(self):
        # Setting up class variables
        self.base_url = "https://quotes.toscrape.com"
        self.current_page = 1
        self.pages_needed = 5
        self.data = []

    def get_data(self):
        # Retrieve data from the current page
        url = f"{self.base_url}/page/{self.current_page}/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        quote_data = soup.find_all("div", {"class": "quote"})

        for quote in quote_data:
            # Extract quote, author, and tags from each quote element
            tags = [tag_html.text for tag_html in quote.find("div", {"class": "tags"}).find_all("a", {"class": "tag"})]

            self.data.append({
                "quote": quote.find("span", {"class": "text"}).text,
                "author": quote.find("small", {"class": "author"}).text,
                "tags": tags
            })

    def next_page(self):
        # Move to the next page if the current page is within the required range
        if self.current_page <= self.pages_needed:
            self.current_page += 1
            return True
        else:
            self.save_data()
            return False

    def save_data(self):
        # Save the scraped data to a CSV file
        df = pd.DataFrame(self.data)
        df.to_csv("data/quotes.csv", index=False)


if __name__ == "__main__":
    # Create an instance of the Scraper class
    scraper = Scraper()

    # Iterate through pages and scrape data
    while scraper.next_page():
        scraper.get_data()
