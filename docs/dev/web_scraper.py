import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find and extract text data from various HTML elements
        text_data = ""
        for element in soup.find_all(["p", "article"]):
            text_data += element.get_text() + " "

        return text_data
    else:
        print("Failed to retrieve data from the website")
        return None


# Example usage:
url = "https://www.calltutors.com/blog/computer-science-topics/"
text_data = scrape_website(url)
if text_data:
    # Write the text data to a file with UTF-8 encoding
    file_path = "docs/dev/data/raw_data.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_data)

    print("Text data has been written to the file:", file_path)
