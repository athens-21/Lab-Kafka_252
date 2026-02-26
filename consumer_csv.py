from kafka import KafkaConsumer
import csv
import json
from datetime import datetime

# เชื่อมต่อ Kafka Consumer
consumer = KafkaConsumer(
    'transaction-processed',  # อ่านจาก Topic ที่ประมวลผลแล้ว
    group_id='csv-export-group',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# กำหนดชื่อไฟล์ CSV พร้อม timestamp
csv_filename = f'transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

print("🎧 Consumer เริ่มรับข้อมูลจาก Kafka และ Export เป็น CSV...")
print(f"📄 ไฟล์จะถูกบันทึกเป็น: {csv_filename}")
print("=" * 60)

# เปิดไฟล์ CSV สำหรับเขียนข้อมูล
with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    
    # เขียน Header ของ CSV
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
            # ถอดรหัส bytes เป็น string
            decoded_string = message.value.decode("utf-8")
            print(f"\n📥 รับข้อมูลจาก Kafka (Offset: {message.offset})")
            
            try:
                # แปลง JSON string เป็น dictionary
                data = json.loads(decoded_string)
                
                # เขียนข้อมูลลง CSV
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
                
                # บันทึกลงไฟล์ทันที
                f.flush()
                
                record_count += 1
                print(f"✅ บันทึกลง CSV สำเร็จ! (รายการที่ {record_count})")
                print(f"   Transaction ID: {data.get('transaction_id')}, "
                      f"Total: {data.get('total_amount')} บาท")
                
            except json.JSONDecodeError:
                print("❌ ข้อมูลที่ส่งมาไม่ใช่รูปแบบ JSON")
                
    except KeyboardInterrupt:
        print(f"\n\n⚠️  หยุดการรับข้อมูล")
        print(f"📊 สรุป: บันทึกข้อมูลทั้งหมด {record_count} รายการ")
        print(f"✅ ไฟล์ CSV: {csv_filename}")

print("\n🏁 Consumer ปิดการทำงาน")
