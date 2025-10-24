import os
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flatten_json import flatten
from datetime import datetime, timezone
import subprocess
import time
from update_utils.update_markets import update_markets
import polars as pl # Added polars import

# Global runtime timestamp - set once when program starts
RUNTIME_TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# Columns to save
COLUMNS_TO_SAVE = ['timestamp', 'maker', 'makerAssetId', 'makerAmountFilled', 'taker', 'takerAssetId', 'takerAmountFilled', 'transactionHash']

if not os.path.isdir('goldsky'):
    os.mkdir('goldsky')

def get_latest_timestamp():
    """Get the latest timestamp from orderFilled.parquet, or 0 if file doesn't exist"""
    cache_file = 'goldsky/orderFilled.parquet'
    print(f"DEBUG: Checking for cache file at absolute path: {os.path.abspath(cache_file)}")
    file_exists_check = os.path.isfile(cache_file)
    print(f"DEBUG: os.path.isfile(cache_file) returned: {file_exists_check}")
    
    if not file_exists_check:
        print("No existing file found, starting from beginning of time (timestamp 0)")
        return 0
    
    try:
        # Use Polars to read the last timestamp from the Parquet file
        df = pl.read_parquet(cache_file)
        if len(df) > 0 and 'timestamp' in df.columns:
            last_timestamp = df.select(pl.col('timestamp')).tail(1).item()
            readable_time = datetime.fromtimestamp(int(last_timestamp), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f'Resuming from timestamp {last_timestamp} ({readable_time})')
            return int(last_timestamp)
    except Exception as e:
        print(f"Error reading latest file with Polars: {e}")
    
    # Fallback to beginning of time
    print("Falling back to beginning of time (timestamp 0)")
    return 0

def scrape(at_once=1000):
    QUERY_URL = "https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/orderbook-subgraph/0.0.1/gn"
    print(f"Query URL: {QUERY_URL}")
    print(f"Runtime timestamp: {RUNTIME_TIMESTAMP}")
    
    # Get starting timestamp from latest file
    last_value = get_latest_timestamp()
    count = 0
    total_records = 0

    print(f"\nStarting scrape for orderFilledEvents")
    
    output_file = 'goldsky/orderFilled.parquet' # Updated to Parquet
    print(f"Output file: {output_file}")
    print(f"Saving columns: {COLUMNS_TO_SAVE}")

    while True:
        q_string = '''query MyQuery {
                        orderFilledEvents(orderBy: timestamp 
                                             first: ''' + str(at_once) + '''
                                             where: {timestamp_gt: "''' + str(last_value) + '''"}) {
                            fee
                            id
                            maker
                            makerAmountFilled
                            makerAssetId
                            orderHash
                            taker
                            takerAmountFilled
                            takerAssetId
                            timestamp
                            transactionHash
                        }
                    }
                '''

        query = gql(q_string)
        transport = RequestsHTTPTransport(url=QUERY_URL, verify=True, retries=3)
        client = Client(transport=transport)
        
        try:
            res = client.execute(query)
        except Exception as e:
            print(f"Query error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue
        
        if not res['orderFilledEvents'] or len(res['orderFilledEvents']) == 0:
            print(f"No more data for orderFilledEvents")
            break

        df = pl.DataFrame([flatten(x) for x in res['orderFilledEvents']])
        
        # Sort by timestamp and update last_value
        df = df.sort('timestamp')
        last_value = df.select(pl.col('timestamp')).tail(1).item()
        
        readable_time = datetime.fromtimestamp(int(last_value), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f"Batch {count + 1}: Last timestamp {last_value} ({readable_time}), Records: {len(df)}")
        
        count += 1
        total_records += len(df)

        # Remove duplicates
        df = df.unique()

        # Filter to only the columns we want to save
        df_to_save = df.select(COLUMNS_TO_SAVE)

        # Save to file
        if os.path.isfile(output_file):
            existing_df = pl.read_parquet(output_file)
            combined_df = pl.concat([existing_df, df_to_save]).unique()
            combined_df.write_parquet(output_file)
        else:
            df_to_save.write_parquet(output_file)

        if len(df) < at_once:
            break

    print(f"Finished scraping orderFilledEvents")
    print(f"Total new records: {total_records}")
    print(f"Output file: {output_file}")

def update_goldsky():
    """Run scraping for orderFilledEvents"""
    print(f"\n{'='*50}")
    print(f"Starting to scrape orderFilledEvents")
    print(f"Runtime: {RUNTIME_TIMESTAMP}")
    print(f"{'='*50}")
    try:
        scrape()
        print(f"Successfully completed orderFilledEvents")
    except Exception as e:
        print(f"Error scraping orderFilledEvents: {str(e)}")