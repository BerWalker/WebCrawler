# WebCrawler

This WebCrawler was developed as a bonus module for the Solyd course. It is designed to extract links and phone numbers from car advertisements on the [Django Anúncios](https://django-anuncios.solyd.com.br) website. The application uses the `BeautifulSoup` library to parse HTML and `threading` to optimize the process by fetching multiple ads simultaneously.

## Features

- Collects car advertisement links.
- Extracts phone numbers from the ads.
- Saves phone numbers to a `CSV` file.
- Utilizes multiple threads to speed up the scraping process.

## How It Works

1. **Link Collection**: 
   The crawler fetches advertisement links from the main car listings page and stores them in a list.
   
2. **Phone Extraction**: 
   For each ad found, it parses the HTML to extract phone numbers using regular expressions.
   
3. **Saving Data**: 
   All found phone numbers are saved into a `phones.csv` file in the format: `Area Code + Phone Number`.

4. **Threads**: 
   Using `threading`, the crawler is able to make multiple requests in parallel, improving the performance of the scraping process.

## Files

### crawler.py

The main file containing the WebCrawler, responsible for the following tasks:

- **fetch_url(url)**: Sends an HTTP request to the provided URL and returns the HTML content of the page.
- **parse_html(html_response)**: Parses the HTML using the `BeautifulSoup` library.
- **extract_links(soup)**: Extracts advertisement links from the main page.
- **extract_phone(soup)**: Extracts phone numbers using regular expressions.
- **fetch_phones()**: Processes the links and extracts phone numbers from the ads.
- **save_phone(phone)**: Saves the extracted phone number to a `CSV` file.

### multi.py

This additional script demonstrates how to create threads for performing simultaneous web requests, using multiple threads to handle tasks efficiently.

```python
import time
import threading

def make_web_request():
    print("Making web request...")
    time.sleep(3)
    print("Finished web request")

# Creating multiple threads for web requests
thread_1 = threading.Thread(target=make_web_request)
thread_1.start()

thread_2 = threading.Thread(target=make_web_request)
thread_2.start()

thread_3 = threading.Thread(target=make_web_request)
thread_3.start()
```

## How to Run

1. Clone this repository:  
   ```bash  
   git clone https://github.com/berwalker/web-crawler.git  
   ```

2. Install the dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```

3. Run the WebCrawler:  
   ```bash  
   python crawler.py  
   ```

4. The phone numbers will be saved in the `phones.csv` file.
