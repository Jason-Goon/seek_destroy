import requests
import csv

def fetch_company_data(api_url, params):
    response = requests.get(api_url, params=params, verify=False)  # SSL verification disabled
    response.raise_for_status()
    return response.json()

def save_to_csv(companies, batch_number):
    filename = f"companies_batch_{batch_number}.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Y-tunnus', 'company_name', 'address', 'website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companies)

def main():
    api_url = "https://avoindata.prh.fi/tr/v1/publicnotices"

    # Input parameters based on the documentation
    params = {
        'name': 'baari',      # Example search term
        'maxResults': 100,      # Fetch 100 results at a time
        'resultsFrom': 0,       # Start from the first result
    }
    
    all_companies = []
    batch_number = 1

    while True:
        data = fetch_company_data(api_url, params)
        companies = []

        for company in data.get('results', []):
            companies.append({
                'Y-tunnus': company.get('businessId'),
                'company_name': company.get('name'),
                'address': ', '.join([addr.get('street', '') + ' ' + addr.get('city', '') for addr in company.get('addresses', [])]),
                'website': company.get('website', '')
            })

        if not companies:
            print("No more companies found, stopping.")
            break

        all_companies.extend(companies)

        if len(all_companies) >= 100:
            save_to_csv(all_companies[:100], batch_number)
            all_companies = all_companies[100:]
            batch_number += 1
        
        params['resultsFrom'] += 100
    
    if all_companies:
        save_to_csv(all_companies, batch_number)

if __name__ == "__main__":
    main()
