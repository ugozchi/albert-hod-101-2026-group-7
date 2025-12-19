import re
from bs4 import BeautifulSoup

# Read HTML file with correct path
with open(r"C:\Users\thoma\Documents\COURS\Head of Data\albert-hod-101-2026-group-7\Parsing\Mails\Fri_01_Nov_2019_12_00_40_.html", 'r', encoding='utf-8') as f:
    html = f.read()

# Extract phone number with regex
phone = re.search(r'\+33\s*6\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}', html).group()
print(f"Phone: {phone}")

# Extract first order item
soup = BeautifulSoup(html, 'html.parser')
first_item = soup.find('table', {'role': 'listitem'}).find_all('p')[1].text.strip()
print(f"First item: {first_item}")