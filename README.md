# WebCrawler

This WebCrawler is a bonus module developed for the Solyd course. It’s designed to extract links and phone numbers from advertisements on various websites, allowing flexible configurations for different domains. The application uses BeautifulSoup for HTML parsing, requests for HTTP requests, and threading for concurrent processing to speed up data extraction.

## Features

- **Flexible URL Configuration**: User can input any domain and target URL, making the crawler adaptable to multiple sites.
- **Dynamic Link and Phone Extraction**: Configurable CSS selectors to locate advertisement links and phone numbers.
- **Multi-threading for Efficiency**: Uses threading to fetch data from multiple ads simultaneously, improving performance.
- **CSV Export**: Extracted phone numbers are saved in a phones.csv file in a standard format.

## How It Works

1. **Input Configuration**: 
The user is prompted to input the base domain, target URL, and optional CSS selectors for locating ad links and phone numbers.
   
2. **Link Collection**: 
The crawler retrieves advertisement links from the provided URL based on the specified CSS selector, storing these links in a list.
   
3. **Phone Extraction**: 
For each ad, the crawler parses the HTML and extracts phone numbers using a regular expression pattern. The extraction process is flexible, allowing users to adjust the pattern if needed.

5. **Saving Data**: 
   All extracted phone numbers are saved to a phones.csv file in the format: Area Code + Phone Number.

6. **Concurrent Requests**
   Using threading, the crawler can handle multiple requests at once, increasing data retrieval speed.

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

## Requirements

- **Python 3.x**
- **Libraries:** requests e BeautifulSoup4

You can install the required libraries using:

```bash
pip install requests beautifulsoup4
```
