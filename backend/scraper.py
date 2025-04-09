import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time

visited = set()

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def is_internal_link(link, base_domain):
    parsed = urlparse(link)
    return parsed.netloc == "" or base_domain in parsed.netloc

def clean_text(text):
    cleaned_text = re.sub(r"\n\s*\n", "\n\n", text)
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)
    return cleaned_text.strip()
    
def clean_links(links, base_domain):
    valid = []
    for link in links:
        if link.startswith(("mailto:", "tel:", "javascript:")):
            continue
        if is_valid_url(link) and is_internal_link(link, base_domain):
            valid.append(link)
    return valid

def scrape_page(url):
    print(f"Scraping: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Skip anything that’s not HTML
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            print(f"Skipped non-HTML content: {url}")
            return "", []

        soup = BeautifulSoup(response.content, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = clean_text(soup.get_text(separator="\n"))
        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
        links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]

        return text, links

    except Exception as e:
        print(f"Failed: {url} – {e}")
        return "", []


def crawl(seed_urls, base_domain, max_depth=2):
    data = {}
    queue = [(url, 0) for url in seed_urls]

    while queue:
        current_url, depth = queue.pop(0)

        if current_url in visited or depth > max_depth:
            continue
        visited.add(current_url)

        content, links = scrape_page(current_url)
        if content:
            data[current_url] = content

        for link in clean_links(links, base_domain):
            if link not in visited:
                queue.append((link, depth + 1))



        time.sleep(0.5)  # Be respectful

    return data

if __name__ == "__main__":
    # Placeholder: Add more seed URLs here as needed
    seed_urls = [
        "https://www.depaul.edu/Pages/default.aspx",  # homepage (still included)
        "https://www.depaul.edu/about/Pages/default.aspx",
        "https://www.depaul.edu/admission-and-aid/Pages/default.aspx",
        "https://www.depaul.edu/academics/Pages/default.aspx",
        "https://www.depaul.edu/student-life/Pages/default.aspx",
        "https://academics.depaul.edu/calendar/Pages/default.aspx",
        "https://www.cdm.depaul.edu/academics/Pages/default.aspx"   
    ]

    domain = "cdm.depaul.edu"
    results = crawl(seed_urls, base_domain=domain, max_depth=3)

    # Save results
    with open("scraped_output.txt", "w", encoding="utf-8") as f:
        for url, content in results.items():
            f.write(f"--- {url} ---\n")
            f.write(content + "\n\n")
    
    print("Crawling completed. Total pages scraped:", len(results))

# This script will crawl the specified seed URLs, scrape their content, and save it to "scraped_output.txt".