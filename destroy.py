import os
import csv
import requests
from googlesearch import search
from bs4 import BeautifulSoup

def is_valid_website(url):
    try:
        print(f"Checking website: {url}")
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            print("Website returned 404, keeping the company.")
            return False
       
        soup = BeautifulSoup(response.content, 'html.parser')
        body_text = soup.get_text(strip=True)
        if len(body_text) > 100:
            print("Website is valid and has content, destroying the company.")
            return True
        else:
            print("Website has minimal content, keeping the company.")
            return False
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}, keeping the company.")
        return False

def find_website(company_name):
    print(f"Searching for website for company: {company_name}")
    query = f"{company_name} site:.fi"  
    try:
        for url in search(query, num_results=5):
            if is_valid_website(url):
                return url
        return None
    except Exception as e:
        print(f"Error during search for {company_name}: {e}")
        return None

def process_file(file_path, output_dir):
    print(f"\nProcessing file: {file_path}")
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        companies_to_keep = []
        seen_companies = set()  

        for row in reader:
            company_name = row.get('company_name')

         
            if company_name in seen_companies:
                continue
            seen_companies.add(company_name)

            website = row.get('website')
            print(f"\nCompany: {company_name}")
            if not website:
                website = find_website(company_name)
                if website:
                    row['website'] = website

            print(f"Website: {website if website else 'No website found'}")

            if website and is_valid_website(website):
                print(f"Company '{company_name}' will be destroyed (filtered out).")
            else:
                print(f"Company '{company_name}' will be kept.")
                companies_to_keep.append(row)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

 
    output_file = os.path.join(output_dir, f"filtered_{os.path.basename(file_path)}")
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Y-tunnus', 'company_name', 'address', 'website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companies_to_keep)
    
    print(f"Finished processing {file_path}. Results saved to {output_file}.")

def main():
 
    input_dir = input("Enter the directory path where the CSV batches are located: ")
    output_dir = input("Enter the directory path where the filtered CSVs should be saved: ")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            process_file(file_path, output_dir)

if __name__ == "__main__":
    main()
