import csv
import re

import requests
from bs4 import BeautifulSoup

def get_nonce(html_source: str) -> str | None:
    match = re.search(r'"nonce":\s*"([^"]+)"', html_source)
    return match.group(1) if match else None


def get_company_data(company_id: str, nonce: str):
    url = 'https://www.sequoiacap.com/wp-admin/admin-ajax.php'
    # Headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'Host': 'www.sequoiacap.com',
        'Origin': 'https://www.sequoiacap.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
        'Referer': 'https://www.sequoiacap.com/our-companies/?_stage_current=ipo',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Data to be sent in the POST request
    data = {
        'action': 'load_company_content',
        'post_id': str(company_id),
        'nonce': nonce,
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=data)
    return response.text


def parse_milestones(milestones_html: str) -> str | None:
    # Parse the HTML content
    milestones_soup = BeautifulSoup(milestones_html, 'html.parser')

    # Find the Milestones section
    milestones_section = None
    for h2 in milestones_soup.find_all('h2'):
        if h2.get_text(strip=True) == 'Milestones':
            milestones_section = h2.find_next('ul')
            break

    milestones = None
    if milestones_section:
        milestones = [li.get_text(strip=True) for li in milestones_section.find_all('li')]
    for milestone in milestones:
        if milestone.__contains__('IPO'):
            return milestone
    return None


url = 'https://www.sequoiacap.com/our-companies/?_stage_current=ipo'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')  # You may need to specify attributes to find the correct table
    nonce = get_nonce(response.text)

    # Step 4: Extract data from the table
    data = []
    for row in table.find_all('tr'):
        print(f'Processing row {row}')
        if 'data-target' in row.attrs:
            company_id = row.attrs['data-target'].split('-')[-1]
            more_info = get_company_data(company_id, nonce)
            company_milestones = parse_milestones(more_info)
        else:
            company_milestones = None
        cols = row.find_all(['td', 'th'])  # Get both header and data cells
        cols = [col.text.strip() for col in cols]  # Strip whitespace
        if cols[0] == 'Loading':
            continue
        cols.pop()
        if not company_milestones:
            cols.append('Milestones')
        else:
            cols.append(company_milestones)
            print(f'Processed row {cols}')
        data.append(cols)

    # Step 5: Write the data to a CSV file
    csv_file_path = 'table_data.csv'  # Specify the desired CSV file name
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print(f"Data has been written to {csv_file_path}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
