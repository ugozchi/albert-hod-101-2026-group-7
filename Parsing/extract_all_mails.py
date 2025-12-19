import re
import json
import os
from bs4 import BeautifulSoup

# Path to the Mails folder
mails_folder = "./Mails"

# List to store all orders
all_orders = []

# Loop through all HTML files in the folder
for filename in os.listdir(mails_folder):
    if filename.endswith('.html'):
        filepath = os.path.join(mails_folder, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        data = {'filename': filename}
        
        # Extract customer phone
        customer_phone = re.search(r'\+33\s*6\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}', html)
        data['customer_phone'] = customer_phone.group().replace(' ', '') if customer_phone else None
        
        # Extract customer info
        all_paragraphs = soup.find_all('p')
        customer_info = []
        for i, p in enumerate(all_paragraphs):
            if 'text-align:right' in str(p.get('style', '')) and 'font-weight:bolder' in str(p.get('style', '')):
                data['customer_name'] = p.text.strip()
                for j in range(1, 4):
                    if i+j < len(all_paragraphs):
                        customer_info.append(all_paragraphs[i+j].text.strip())
                break
        
        data['customer_address'] = ', '.join(customer_info) if customer_info else None
        
        # Extract restaurant info
        restaurant_info = []
        for i, p in enumerate(all_paragraphs):
            if 'Le Pain Quotidien' in p.text or 'font-weight:bolder' in str(p.get('style', '')):
                restaurant_name = p.text.strip()
                if restaurant_name and len(restaurant_name) > 3 and restaurant_name != data.get('customer_name'):
                    data['restaurant_name'] = restaurant_name
                    for j in range(1, 5):
                        if i+j < len(all_paragraphs):
                            text = all_paragraphs[i+j].text.strip()
                            if text and not text.startswith('Regis'):
                                restaurant_info.append(text)
                    break
        
        if restaurant_info and len(restaurant_info) > 0:
            data['restaurant_address'] = ', '.join(restaurant_info[:-1]) if len(restaurant_info) > 1 else None
            data['restaurant_phone'] = restaurant_info[-1] if restaurant_info else None
        
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
                for p in all_p[2:-1]:
                    if p.text.strip():
                        item_data['options'].append(p.text.strip())
                items.append(item_data)
        
        data['items'] = items
        
        # Extract pricing
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
        
        # Add to list
        all_orders.append(data)
        print(f"Processed: {filename}")

# Save all orders to one JSON file
with open('all_deliveroo_orders.json', 'w', encoding='utf-8') as f:
    json.dump(all_orders, f, indent=2, ensure_ascii=False)

print(f"\nTotal orders processed: {len(all_orders)}")
print("All data saved to: all_deliveroo_orders.json")