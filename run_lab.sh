#!/bin/bash

# Script สำหรับรัน Kafka Streams Pipeline Lab
# โครงสร้าง: Producer → Kafka → Stream Processing → Kafka → Consumer → CSV

echo "🚀 เริ่มรัน Kafka Streams Pipeline Lab"
echo "======================================"

# ตรวจสอบว่าอยู่ใน directory ที่ถูกต้อง
LAB_DIR="/Users/athens/241DE/Lab_Kafka_Streams_Pipeline"
VENV_PATH="/Users/athens/241DE/.venv/bin/activate"

if [ ! -d "$LAB_DIR" ]; then
    echo "❌ ไม่พบ directory: $LAB_DIR"
    exit 1
fi

cd "$LAB_DIR"

# ตรวจสอบ Python environment
if [ ! -f "$VENV_PATH" ]; then
    echo "❌ ไม่พบ Virtual Environment: $VENV_PATH"
    exit 1
fi

echo "✅ ตรวจสอบ Environment สำเร็จ"
echo ""

# ตรวจสอบ Kafka Cluster
echo "🔍 ตรวจสอบ Kafka Cluster..."
if ! docker ps | grep -q "broker"; then
    echo "❌ Kafka Cluster ไม่ทำงาน!"
    echo "   กรุณาเริ่ม Kafka ด้วย:"
    echo "   cd /Users/athens/241DE/cp-all-in-one/cp-all-in-one"
    echo "   docker compose up -d"
    exit 1
fi

echo "✅ Kafka Cluster ทำงานอยู่"
echo ""

# คำแนะนำการรัน
echo "📌 วิธีรัน Lab (เปิด 3 Terminal แยกกัน)"
echo "======================================"
echo ""
echo "1️⃣  Terminal 1 - Stream Processor (Faust Worker):"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python stream_processor.py worker -l info"
echo ""
echo "2️⃣  Terminal 2 - Consumer (Export CSV):"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python consumer_csv.py"
echo ""
echo "3️⃣  Terminal 3 - Producer (ส่งข้อมูล):"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python producer.py"
echo ""
echo "⚠️  ลำดับที่ถูกต้อง: Stream Processor → Consumer → Producer"
echo ""
echo "📊 ผลลัพธ์: ไฟล์ CSV จะถูกสร้างในโฟลเดอร์นี้"
echo "   ชื่อไฟล์: transactions_YYYYMMDD_HHMMSS.csv"
echo ""

# ถาม user ว่าต้องการรันอัตโนมัติหรือไม่
read -p "🤔 ต้องการเปิด Terminal อัตโนมัติหรือไม่? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔨 กำลังเปิด Terminal ..."
    
    # เปิด Terminal 1: Stream Processor
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo '⚙️  Stream Processor (Faust) กำลังเริ่ม...' && python stream_processor.py worker -l info\"
    end tell" &
    
    sleep 3
    
    # เปิด Terminal 2: Consumer
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo '🎧 Consumer กำลังเริ่ม...' && sleep 5 && python consumer_csv.py\"
    end tell" &
    
    sleep 3
    
    # เปิด Terminal 3: Producer
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo '🚀 Producer กำลังเริ่ม...' && sleep 8 && python producer.py\"
    end tell"
    
    echo "✅ เปิด Terminal ทั้งหมดเรียบร้อย"
else
    echo "📝 กรุณาเปิด Terminal 3 หน้าต่าง และรันตามคำแนะนำด้านบน"
fi

echo ""
echo "🎓 Happy Learning with Kafka Streams Pipeline!"
