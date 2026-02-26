from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime

print("⚙️  Stream Processing เริ่มทำงาน...")
print("=" * 60)

# สร้าง Consumer อ่านจาก transaction-raw
consumer = KafkaConsumer(
    'transaction-raw',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='stream-processor-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# สร้าง Producer ส่งไปยัง transaction-processed
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("✅ Stream Processor พร้อมแล้ว!")
print("🔄 รอรับข้อมูลจาก 'transaction-raw' topic...\n")

try:
    for message in consumer:
        try:
            # รับข้อมูล RAW
            transaction_dict = message.value
            print(f"\n📥 รับข้อมูล RAW: {transaction_dict}")
            
            # ประมวลผล: คำนวณ total_amount
            quantity = transaction_dict['quantity']
            price = transaction_dict['price']
            total_amount = quantity * price
            
            # เพิ่มข้อมูลที่ประมวลผลแล้ว
            transaction_dict['total_amount'] = total_amount
            transaction_dict['processed_at'] = str(datetime.now())
            transaction_dict['status'] = 'processed'
            
            # ส่งข้อมูลที่ประมวลผลแล้วไปยัง Topic ใหม่
            producer.send('transaction-processed', value=transaction_dict)
            producer.flush()
            
            print(f"✅ ประมวลผลสำเร็จ: transaction_id={transaction_dict['transaction_id']}, total_amount={total_amount}")
            print(f"📤 ส่งข้อมูลไปยัง 'transaction-processed' topic")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            
except KeyboardInterrupt:
    print("\n\n⚠️  หยุดการทำงาน")
finally:
    consumer.close()
    producer.close()
    print("🏁 Stream Processor ปิดการทำงาน")
