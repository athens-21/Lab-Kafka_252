from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random

# เชื่อมต่อ Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# ข้อมูลจำลอง
products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphone']
customers = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

print("🚀 Producer เริ่มส่งข้อมูล Transaction ไปยัง Kafka...")
print("=" * 60)

try:
    # ส่งข้อมูล 10 รายการ
    for i in range(1, 11):
        # สร้างข้อมูล transaction
        transaction_data = {
            "transaction_id": i,
            "customer_name": random.choice(customers),
            "product": random.choice(products),
            "quantity": random.randint(1, 5),
            "price": random.randint(100, 5000),
            "timestamp": datetime.now().isoformat()
        }
        
        # ส่งข้อมูลไปยัง Topic 'transaction-raw'
        producer.send('transaction-raw', value=transaction_data)
        producer.flush()
        
        print(f"✅ ส่งข้อมูล Transaction #{i}: {transaction_data}")
        time.sleep(1)  # หน่วงเวลา 1 วินาที
        
except KeyboardInterrupt:
    print("\n⚠️  หยุดการส่งข้อมูล")
finally:
    producer.close()
    print("\n🏁 Producer ปิดการทำงาน")
