# การส่งการบ้าน - Kafka Streams Pipeline

**วิชา:** DE241  
**ที่ส่ง:** `/Users/athens/241DE/Lab_Kafka_Streams_Pipeline`

---

## โครงสร้าง Pipeline

```
Producer → เขียนข้อมูลลง Streaming Log (Kafka) ที่ topic transaction-raw
                                    ↓
Stream Processing → อ่านจาก Streaming Log (Kafka) (transaction-raw) ⬆️
                  → ประมวลผล (คำนวณ total_amount)
                  → เขียนกลับเข้า Streaming Log (Kafka) (transaction-processed) ⬇️
                                    ↓
Consumer → อ่านจาก Streaming Log (Kafka) (transaction-processed) ⬆️
         → Export เป็น CSV file ➡️
```

---

## ไฟล์ในโปรเจกต์

- `producer.py` - ส่งข้อมูล transaction ไปยัง Kafka
- `stream_processor.py` - ประมวลผลข้อมูลและส่งต่อ
- `consumer_csv.py` - รับข้อมูลและ export เป็น CSV
- `run_lab.sh` - Script สำหรับรัน Lab
- `transactions_*.csv` - ไฟล์ผลลัพธ์

---

## วิธีรัน

```bash
# Terminal 1: Stream Processor
cd /Users/athens/241DE/Lab_Kafka_Streams_Pipeline
source /Users/athens/241DE/.venv/bin/activate
python stream_processor.py

# Terminal 2: Consumer
cd /Users/athens/241DE/Lab_Kafka_Streams_Pipeline
source /Users/athens/241DE/.venv/bin/activate
python consumer_csv.py

# Terminal 3: Producer
cd /Users/athens/241DE/Lab_Kafka_Streams_Pipeline
source /Users/athens/241DE/.venv/bin/activate
python producer.py
```
