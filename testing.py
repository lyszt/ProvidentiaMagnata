import requests
from bs4 import BeautifulSoup

url = f"https://www.bing.com/search?q=\"aldynor\""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
#print(soup.prettify())
results = []

for item in soup.find_all("li", {"class": "b_algo"}):
    link = item.find("a")["href"]
    snippet = item.find("p")  # Bing typically places the description in a <p> tag

    if snippet:
        snippet_text = snippet.get_text()
    else:
        snippet_text = "No description available"

    results.append(snippet_text)

print(results)