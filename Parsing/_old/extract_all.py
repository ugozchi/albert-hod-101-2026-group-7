import re
import json
from bs4 import BeautifulSoup

with open(r"C:\Users\thoma\Documents\COURS\Head of Data\albert-hod-101-2026-group-7\Parsing\Mails\Fri_01_Nov_2019_12_00_40_.html", 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
data = {}

# Extract customer phone
customer_phone = re.search(r'\+33\s*6\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}', html)
data['customer_phone'] = customer_phone.group().replace(' ', '') if customer_phone else None

# Extract customer info
all_paragraphs = soup.find_all('p')
customer_info = []
for i, p in enumerate(all_paragraphs):
    if 'text-align:right' in str(p.get('style', '')) and 'font-weight:bolder' in str(p.get('style', '')):
        # Found customer name
        data['customer_name'] = p.text.strip()
        # Next paragraphs are address
        for j in range(1, 4):
            if i+j < len(all_paragraphs):
                customer_info.append(all_paragraphs[i+j].text.strip())
        break

data['customer_address'] = ', '.join(customer_info) if customer_info else None

# Extract restaurant info
restaurant_info = []
for i, p in enumerate(all_paragraphs):
    if 'Le Pain Quotidien' in p.text:
        data['restaurant_name'] = p.text.strip()
        for j in range(1, 5):
            if i+j < len(all_paragraphs):
                text = all_paragraphs[i+j].text.strip()
                restaurant_info.append(text)
        break

if restaurant_info:
    data['restaurant_address'] = ', '.join(restaurant_info[:-1])
    data['restaurant_phone'] = restaurant_info[-1]

# Extract order number
order_match = re.search(r'Commande n° (\d+)', html)
data['order_number'] = order_match.group(1) if order_match else None

# Extract order items
items = []
for item_table in soup.find_all('table', {'role': 'listitem'}):
    all_p = item_table.find_all('p')
    if len(all_p) >= 3:
        item_data = {
            'quantity': all_p[0].text.strip(),
            'name': all_p[1].text.strip(),
            'options': [],
            'price': all_p[-1].text.strip()
        }
        # Extract options (in between name and price)
        for p in all_p[2:-1]:
            if p.text.strip():
                item_data['options'].append(p.text.strip())
        items.append(item_data)

data['items'] = items

# Extract pricing details
price_rows = soup.find_all('p', style=lambda x: x and 'font-size:15px' in x)
for i, p in enumerate(price_rows):
    text = p.text.strip()
    if 'Sous-total' in text and i+1 < len(price_rows):
        data['subtotal'] = price_rows[i+1].text.strip()
    elif 'Frais de livraison' in text and i+1 < len(price_rows):
        data['delivery_fee'] = price_rows[i+1].text.strip()
    elif 'Pourboire' in text and i+1 < len(price_rows):
        data['tip'] = price_rows[i+1].text.strip()
    elif 'Crédit' in text and i+1 < len(price_rows):
        data['credit'] = price_rows[i+1].text.strip()

# Extract total
total_p = soup.find('p', class_='total', style=lambda x: x and 'text-align:right' in x)
data['total'] = total_p.text.strip() if total_p else None

# Extract delivery person phone
delivery_phone = re.search(r'livreur.*?(\+33\d{9})', html, re.DOTALL)
data['delivery_person_phone'] = delivery_phone.group(1) if delivery_phone else None

# Extract order date from filename
data['order_date'] = 'Fri_01_Nov_2019_12_00_40'

# Save to JSON
with open('deliveroo_order_complete.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(json.dumps(data, indent=2, ensure_ascii=False))