# Dog Picture Scraper

This Python script is designed to scrape a website in order to find pictures of dogs. It's part of a task for a developer interview at Baires Dev.

## Getting Started

Follow the steps below to set up and run the application.

### Prerequisites

- Python 3.x installed on your machine.

### Installation

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/cesardlinx/dog-picture-scraper.git
    ```

2. Navigate to the project directory.

    ```bash
    cd dog-picture-scraper
    ```

3. Create a virtual environment.

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment.

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. Install dependencies.

    ```bash
    pip install -r requirements.txt
    ```

### Usage

Run the script by executing the following command in your terminal or command prompt:

```bash
python main.py
```

## Answer to Interview Questions

1. How can we automate the login of the page?

If the website requires authentication, we can automate the login process using the requests library. We can modify the script to include login credentials and session management. For example:

```python
import requests

# Provide login credentials
login_payload = {
    'username': 'your_username',
    'password': 'your_password'
}

# Create a session to persist the login session
with requests.Session() as session:
    # Perform login
    login_response = session.post('https://www.freeimages.com/signin', data=login_payload)

    # Check if login was successful (inspect login_response)
    if login_response.status_code == 200:
        # Continue with the scraping using the session...
    else:
        print("Login failed.")
```

2. How can we scale the extractor to get thousands of pages per hour?

In order to scale the extractor for higher throughput, we should consider using asynchronous programming with the asyncio library and making asynchronous HTTP requests with aiohttp. This allows the script to send multiple requests concurrently, improving overall performance. For example:

```python
import asyncio
import aiohttp

BASE_URL = 'https://www.freeimages.com/search/dogs'

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def main():
    # this is just an example we should make a for loop in order to create all the urls
    urls = [f'{BASE_URL}/1', f'{BASE_URL}/2', ...]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls]
        pages_content = await asyncio.gather(*tasks)

        # Process the pages_content using BeautifulSoup ...

if __name__ == '__main__':
    asyncio.run(main())
```

Another solution is to use a scraping framework such as Scrapy. Scrapy is also able to handle Asynchronous requests, making large-scale scraping operations easier, faster, and in a more efficient way. 

