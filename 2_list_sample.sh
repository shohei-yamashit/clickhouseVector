#!/bin/bash
INPUT=$1

TEST_URL="http://localhost:13000/hello"
ENDPOINT_URL="http://localhost:13000/tokenize"

# URLが利用可能になるまでポーリング
while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$TEST_URL" \
        -H "accept: text/plain" \
        -H "Content-Type: application/json" \
        )
    
    if [ "$response" -eq 200 ]; then
        break
    else
        echo "Error: Unable to reach $TEST_URL. Retrying in 5 seconds..."
        sleep 5  # 5秒待機してから再試行
    fi
done

tokens=$(curl -s -X 'POST' \
    "$ENDPOINT_URL" \
    -H "accept: text/plain" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"${INPUT}\"}" | jq -c | sed "s/\"/'/g")

cat ./query/06_select_list_template.sql | 
  sed "s/__VAR__/${tokens}/" |
  curl 'http://localhost:18123/?password=changeme' --data-binary @-