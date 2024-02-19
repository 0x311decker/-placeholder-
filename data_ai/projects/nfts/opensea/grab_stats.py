import requests
import pandas as pd
from datetime import datetime

def fetch_all_opensea_events(collection_slug, event_type='sale', limit=50):
    print("Starting to fetch events from OpenSea API...")
    url = f'https://api.opensea.io/api/v2/events/collection/{collection_slug}'
    headers = {
        "accept": "application/json",
        "x-api-key": "f33792e26c2840d89a8e71314828b79c"
    }
    
    all_events = []
    next_cursor = None
    page_count = 0
    
    while True:
        print(f"Fetching page {page_count + 1}...")
        params = {
            #'after': after,
            #'before': before_timestamp,
            'event_type': event_type,
            'limit': limit,
            'next': next_cursor
        }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('asset_events', [])
            all_events.extend(events)
            page_count += 1
            next_cursor = data.get('next')  # Make sure to update the cursor here
            last_event_datetime = datetime.utcfromtimestamp(events[-1]['event_timestamp']).strftime('%Y-%m-%d %H:%M:%S+00:00') if events else "No events"
            print(f"Page {page_count} fetched. Total events fetched: {len(all_events)}. Last event datetime: {last_event_datetime}")
            
            if not events or not next_cursor:
                print("All pages fetched or no more events to fetch.")
                break
        else:
            print('Failed to fetch data:', response.status_code, response.text)
            break
    
    print(f"Total events fetched: {len(all_events)}")
    return all_events

def convert_to_dataframe(events):
    print("Converting events to DataFrame...")
    columns = ['timestamp', 'projectContact', 'transaction_hash', 'base', 'quote', 'exchange', 'datetime', 'price', 'base_volume', 'quote_volume']
    data = []
    
    for event in events:
        timestamp = event['event_timestamp']
        projectContract = event['nft'].get('contract') if event['nft'] else None
        transaction_hash = event.get('transaction')
        base = collection_slug
        exchange = 'opensea'
        datetime_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S+00:00')
        payment_info = event.get('payment')
        quote = payment_info.get('symbol') if payment_info else None
        quote_volume = float(payment_info['quantity']) / 10**payment_info['decimals'] if payment_info and payment_info.get('quantity') and 'decimals' in payment_info else None
        base_volume = float(event['quantity']) if 'quantity' in event else None
        price = quote_volume / base_volume if quote_volume and base_volume and base_volume > 0 else None
        data.append([timestamp, projectContract, transaction_hash, base, quote, exchange, datetime_str, price, base_volume, quote_volume])
    
    df = pd.DataFrame(data, columns=columns)
    print("Conversion to DataFrame completed.")
    return df

print("Script started.")
collection_slug = 'schizoposters'
events = fetch_all_opensea_events(
    collection_slug=collection_slug,
    #after=1635724800
)

if events:
    df = convert_to_dataframe(events)
    # Adjusting the file path to be dynamic based on collection_slug
    csv_file_path = fr"C:\Users\Reilly Decker\Desktop\opensea\{collection_slug}_sales_20240217.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"Data has been saved to {csv_file_path}")
else:
    print("No data to process or 'asset_events' key not in JSON response.")

print("Script finished.")