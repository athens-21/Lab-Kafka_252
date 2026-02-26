from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime

print("Stream Processing started")
print("=" * 60)

consumer = KafkaConsumer(
    'transaction-raw',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='stream-processor-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Stream Processor ready")
print("Waiting for messages from 'transaction-raw' topic...\n")

try:
    for message in consumer:
        try:
            transaction_dict = message.value
            print(f"\nReceived: {transaction_dict}")
            
            quantity = transaction_dict['quantity']
            price = transaction_dict['price']
            total_amount = quantity * price
            
            transaction_dict['total_amount'] = total_amount
            transaction_dict['processed_at'] = str(datetime.now())
            transaction_dict['status'] = 'processed'
            
            producer.send('transaction-processed', value=transaction_dict)
            producer.flush()
            
            print(f"Processed: transaction_id={transaction_dict['transaction_id']}, total_amount={total_amount}")
            print(f"Sent to 'transaction-processed' topic")
            
        except Exception as e:
            print(f"Error: {e}")
            
except KeyboardInterrupt:
    print("\n\nStopped")
finally:
    consumer.close()
    producer.close()
    print("Stream Processor closed")
