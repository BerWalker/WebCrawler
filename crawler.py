import re
import threading
import requests
from bs4 import BeautifulSoup

DOMAIN = "https://django-anuncios.solyd.com.br"
URL_CARS = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
PHONES = []

def fetch_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch URL")
    except Exception as error:
        print("Error while fetching the URL")
        print(error)

def parse_html(html_response):
    try:
        soup = BeautifulSoup(html_response, 'html.parser')
        return soup
    except Exception as error:
        print("Error parsing the HTML")
        print(error)

def extract_links(soup):
    try:
        parent_cards = soup.find("div", class_="ui three doubling link cards")
        cards = parent_cards.find_all("a")
    except:
        print("Error finding links")
        return None

    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except:
            pass

    return links

def extract_phone(soup):
    try:
        description = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except:
        print("Error finding description")
        return None

    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", description)
    if regex:
        return regex

def fetch_phones():
    while LINKS:
        try:
            ad_link = LINKS.pop(0)
        except IndexError:
            return None

        ad_response = fetch_url(DOMAIN + ad_link)

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
    formatted_phone = "{}{}{}\n".format(phone[0], phone[1], phone[2])
    try:
        with open("phones.csv", "a") as file:
            file.write(formatted_phone)
    except Exception as error:
        print("Error saving phone number")
        print(error)

if __name__ == "__main__":
    search_response = fetch_url(URL_CARS)
    if search_response:
        soup_search = parse_html(search_response)
        if soup_search:
            LINKS = extract_links(soup_search)

            THREADS = []
            for i in range(10):
                thread = threading.Thread(target=fetch_phones)
                THREADS.append(thread)

            for thread in THREADS:
                thread.start()

            for thread in THREADS:
                thread.join()
