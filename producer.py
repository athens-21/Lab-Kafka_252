from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphone']
customers = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

print("Producer started")
print("=" * 60)

try:
    for i in range(1, 11):
        transaction_data = {
            "transaction_id": i,
            "customer_name": random.choice(customers),
            "product": random.choice(products),
            "quantity": random.randint(1, 5),
            "price": random.randint(100, 5000),
            "timestamp": datetime.now().isoformat()
        }
        
        producer.send('transaction-raw', value=transaction_data)
        producer.flush()
        
        print(f"Sent transaction #{i}: {transaction_data}")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nStopped")
finally:
    producer.close()
    print("\nProducer closed")
