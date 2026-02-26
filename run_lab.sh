#!/bin/bash

echo "Starting Kafka Streams Pipeline Lab"
echo "======================================"

LAB_DIR="/Users/athens/241DE/Lab_Kafka_Streams_Pipeline"
VENV_PATH="/Users/athens/241DE/.venv/bin/activate"

if [ ! -d "$LAB_DIR" ]; then
    echo "Error: Directory not found: $LAB_DIR"
    exit 1
fi

cd "$LAB_DIR"

if [ ! -f "$VENV_PATH" ]; then
    echo "Error: Virtual Environment not found: $VENV_PATH"
    exit 1
fi

echo "Environment check: OK"
echo ""

echo "Checking Kafka Cluster..."
if ! docker ps | grep -q "broker"; then
    echo "Error: Kafka Cluster is not running!"
    echo "   Please start Kafka:"
    echo "   cd /Users/athens/241DE/cp-all-in-one/cp-all-in-one"
    echo "   docker compose up -d"
    exit 1
fi

echo "Kafka Cluster: Running"
echo ""

echo "How to run Lab (3 separate terminals)"
echo "======================================"
echo ""
echo "Terminal 1 - Stream Processor:"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python stream_processor.py"
echo ""
echo "Terminal 2 - Consumer (Export CSV):"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python consumer_csv.py"
echo ""
echo "Terminal 3 - Producer:"
echo "   cd $LAB_DIR"
echo "   source $VENV_PATH"
echo "   python producer.py"
echo ""
echo "Order: Stream Processor -> Consumer -> Producer"
echo ""
echo "Output: CSV file will be created in this folder"
echo "   Filename: transactions_YYYYMMDD_HHMMSS.csv"
echo ""

read -p "Open terminals automatically? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Opening terminals..."
    
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo 'Stream Processor starting...' && python stream_processor.py\"
    end tell" &
    
    sleep 3
    
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo 'Consumer starting...' && sleep 5 && python consumer_csv.py\"
    end tell" &
    
    sleep 3
    
    osascript -e "tell application \"Terminal\"
        do script \"cd '$LAB_DIR' && source '$VENV_PATH' && echo 'Producer starting...' && sleep 8 && python producer.py\"
    end tell"
    
    echo "All terminals opened"
else
    echo "Please open 3 terminals and run the commands above"
fi

echo ""
echo "Kafka Streams Pipeline Lab"
