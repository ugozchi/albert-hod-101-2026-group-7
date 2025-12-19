import requests
from bs4 import BeautifulSoup
import time

def scrape_quotes_page(url):
    """Scrape all quotes from a single page"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    quotes_list = []
    
    # Find all quote containers
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        # Extract quote text
        text = quote.find('span', class_='text').text.strip()
        
        # Extract author name
        author = quote.find('small', class_='author').text.strip()
        
        # Extract tags
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        
        quotes_list.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    
    return quotes_list

def find_next_page(soup):
    """Find the 'Next' button and return the next page URL"""
    next_button = soup.find('li', class_='next')
    if next_button:
        next_link = next_button.find('a')
        if next_link:
            return 'https://quotes.toscrape.com' + next_link['href']
    return None

def crawl_all_quotes():
    """Crawl all pages and collect all quotes"""
    base_url = 'https://quotes.toscrape.com/'
    current_url = base_url
    all_quotes = []
    page_count = 0
    
    while current_url:
        page_count += 1
        print(f"Scraping page {page_count}: {current_url}")
        
        # Get the page content
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape quotes from current page
        page_quotes = scrape_quotes_page(current_url)
        all_quotes.extend(page_quotes)
        print(f"  → Found {len(page_quotes)} quotes")
        
        # Find next page
        current_url = find_next_page(soup)
        
        # Be polite to the server
        time.sleep(0.5)
    
    print(f"\n✓ Total pages scraped: {page_count}")
    print(f"✓ Total quotes collected: {len(all_quotes)}")
    
    return all_quotes

# Run the crawler
if __name__ == "__main__":
    all_quotes = crawl_all_quotes()
    
    # Display first 3 quotes as example
    print("\n--- Sample Quotes ---")
    for i, quote in enumerate(all_quotes[:3], 1):
        print(f"\nQuote {i}:")
        print(f"  Text: {quote['text']}")
        print(f"  Author: {quote['author']}")
        print(f"  Tags: {quote['tags']}")
    
    # Optional: Save to JSON file
    import json
    with open('all_quotes.json', 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, indent=2, ensure_ascii=False)
    print("\n✓ Data saved to all_quotes.json")