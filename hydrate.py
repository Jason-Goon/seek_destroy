import csv
import json
import requests
from bs4 import BeautifulSoup
import time
import os

def scrape_finder_details(business_name):
    search_url = f"https://www.finder.fi/search?what={business_name.replace(' ', '%20')}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    details = {
        'name': business_name,
        'address': 'Not found',
        'phone_number': 'Not found',
        'gmail': 'Not found',
        'description': 'Not found'
    }

    try:
        # Find the first result in the search results
        result = soup.find('div', class_='result-container')
        if result:
            details['address'] = result.find('div', class_='address').text.strip() if result.find('div', class_='address') else 'Not found'
            details['phone_number'] = result.find('div', class_='phone').text.strip() if result.find('div', class_='phone') else 'Not found'
            details['gmail'] = result.find('a', class_='email').text.strip() if result.find('a', class_='email') else 'Not found'
            details['description'] = result.find('div', class_='description').text.strip() if result.find('div', class_='description') else 'Not found'
    except Exception as e:
        print(f"Could not scrape details for {business_name}: {e}")

    return details

def process_file(file_path):
    hydrated_data = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            business_name = row.get('company_name')
            print(f"Processing: {business_name}")
            details = scrape_finder_details(business_name)
            hydrated_data.append(details)
            time.sleep(2)  # Sleep to avoid rate limiting or being blocked

    return hydrated_data

def save_to_json(data, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print(f"Hydrated data saved to {output_file}")

def main():
    input_dir = input("Enter the directory path where the filtered CSVs are located: ")
    output_file = input("Enter the path to save the output JSON file: ")

    all_hydrated_data = []


    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            print(f"\nProcessing file: {file_path}")
            hydrated_data = process_file(file_path)
            all_hydrated_data.extend(hydrated_data)

    # Save the combined data to a JSON file
    save_to_json(all_hydrated_data, output_file)

if __name__ == "__main__":
    main()
