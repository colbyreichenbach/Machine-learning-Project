import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mlb_transactions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='datatable center')
    if not table:
        print("No table found at:", url)
        return pd.DataFrame()  # Return an empty DataFrame if no table is found

    transactions = []
    header_row = table.find('tr', class_='DraftTableLabel')
    if not header_row:
        print("No header row found in the table at:", url)
        return pd.DataFrame()  # Return an empty DataFrame if no header row is found

    headers = [header.text.strip() for header in header_row.find_all('td')]
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) != len(headers):
            continue  # Skip rows that do not match header count
        transaction_data = {headers[i]: cols[i].text.strip() for i in range(len(cols))}
        transactions.append(transaction_data)

    return pd.DataFrame(transactions)

def scrape_all_pages(base_url, start_date, end_date, start_record, records_per_page, max_pages):
    all_transactions = pd.DataFrame()
    for page_number in range(max_pages):
        start = start_record + page_number * records_per_page
        url = f"{base_url}?Player=&Team=&BeginDate={start_date}&EndDate={end_date}&InjuriesChkBx=yes&submit=Search&start={start}"
        df_transactions = scrape_mlb_transactions(url)
        if df_transactions.empty:
            print("No more data found, ending scrape at page:", page_number)
            break  # Stop if a page returns no results
        all_transactions = pd.concat([all_transactions, df_transactions], ignore_index=True)

    # Save all transactions to a CSV file
    all_transactions.to_csv('/Users/colbyreichenbach/desktop/Baseball Injury Prediction/mlb_injury_transactionsv1.csv', index=False)
    print("Data saved to 'mlb_injury_transactions.csv'")
    return all_transactions

# Example usage
base_url = 'https://www.prosportstransactions.com/baseball/Search/SearchResults.php'
start_date = '2017-01-01'
end_date = '2022-12-31'
all_transactions = scrape_all_pages(base_url, start_date, end_date, 0, 25, 439)  # Adjust max_pages as needed
