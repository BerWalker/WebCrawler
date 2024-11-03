import re
import threading
import requests
from bs4 import BeautifulSoup

# Global containers
LINKS = []
PHONES = []
LINKS_LOCK = threading.Lock()  # To handle thread-safe access to LINKS

def fetch_url(url):
    """Fetches the HTML content of a URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch URL: {url}")
    except Exception as error:
        print(f"Error while fetching URL {url}: {error}")

def parse_html(html_response):
    """Parses HTML response using BeautifulSoup."""
    try:
        return BeautifulSoup(html_response, 'html.parser')
    except Exception as error:
        print(f"Error parsing HTML: {error}")

def extract_links(soup, card_selector="div.ui.three.doubling.link.cards", link_tag="a"):
    """Extracts links from the soup based on a selector."""
    try:
        parent_cards = soup.select_one(card_selector)
        cards = parent_cards.find_all(link_tag) if parent_cards else []
    except Exception as error:
        print(f"Error finding links with selector {card_selector}: {error}")
        return []

    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except KeyError:
            pass  # Skip if 'href' is missing
    return links

def extract_phone(soup, description_selector="div.sixteen.wide.column", regex_pattern=None):
    """Extracts phone numbers using regex from a description located by a selector."""
    if regex_pattern is None:
        regex_pattern = r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})"

    try:
        description = soup.select(description_selector)[2].get_text().strip()
        regex = re.findall(regex_pattern, description)
        return regex if regex else []
    except (IndexError, AttributeError) as error:
        print(f"Error finding phone number in description: {error}")
        return []

def fetch_phones(domain):
    """Fetches phone numbers from links in the LINKS list."""
    while True:
        with LINKS_LOCK:
            if not LINKS:
                break
            ad_link = LINKS.pop(0)

        ad_response = fetch_url(domain + ad_link)
        if ad_response:
            ad_soup = parse_html(ad_response)
            if ad_soup:
                phones = extract_phone(ad_soup)
                if phones:
                    for phone in phones:
                        print("Phone found:", phone)
                        PHONES.append(phone)
                        save_phone(phone)

def save_phone(phone):
    """Saves phone numbers to a CSV file."""
    formatted_phone = "{}{}{}\n".format(phone[0], phone[1], phone[2])
    try:
        with open("phones.csv", "a") as file:
            file.write(formatted_phone)
    except Exception as error:
        print(f"Error saving phone number {phone}: {error}")

if __name__ == "__main__":
    domain = input("Enter the base domain (e.g., https://example.com): ").strip()
    target_url = input("Enter the target URL for ads (e.g., https://example.com/ads): ").strip()
    card_selector = input(
        "Enter the CSS selector for ad cards (default: 'div.ui.three.doubling.link.cards'): ").strip() or "div.ui.three.doubling.link.cards"

    search_response = fetch_url(target_url)
    if search_response:
        soup_search = parse_html(search_response)
        if soup_search:
            LINKS = extract_links(soup_search, card_selector=card_selector)

            threads = []
            for _ in range(10):  # Creating 10 threads for concurrent fetching
                thread = threading.Thread(target=fetch_phones, args=(domain,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
