from kafka import KafkaConsumer
import csv
import json
from datetime import datetime

consumer = KafkaConsumer(
    'transaction-processed',
    group_id='csv-export-group',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

csv_filename = f'transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

print("Consumer started")
print(f"Output file: {csv_filename}")
print("=" * 60)

with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    
    writer.writerow([
        'transaction_id',
        'customer_name',
        'product',
        'quantity',
        'price',
        'total_amount',
        'timestamp',
        'processed_at',
        'status'
    ])
    
    try:
        record_count = 0
        for message in consumer:
            decoded_string = message.value.decode("utf-8")
            print(f"\nReceived message (Offset: {message.offset})")
            
            try:
                data = json.loads(decoded_string)
                
                writer.writerow([
                    data.get('transaction_id', ''),
                    data.get('customer_name', ''),
                    data.get('product', ''),
                    data.get('quantity', 0),
                    data.get('price', 0),
                    data.get('total_amount', 0),
                    data.get('timestamp', ''),
                    data.get('processed_at', ''),
                    data.get('status', '')
                ])
                
                f.flush()
                
                record_count += 1
                print(f"Saved to CSV (Record #{record_count})")
                print(f"   Transaction ID: {data.get('transaction_id')}, "
                      f"Total: {data.get('total_amount')}")
                
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                
    except KeyboardInterrupt:
        print(f"\n\nStopped")
        print(f"Total records: {record_count}")
        print(f"CSV file: {csv_filename}")

print("\nConsumer closed")
