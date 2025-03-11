#!/bin/bash

# 初期化スクリプトを実行
curl 'http://localhost:18123/?password=changeme' --data-binary @query/00_drop_db.sql
curl 'http://localhost:18123/?password=changeme' --data-binary @query/01_init_db.sql
curl 'http://localhost:18123/?password=changeme' --data-binary @query/02_init_table.sql

# 圧縮されたCSVファイルを解凍してデータを挿入
gzip -d -c data/sample.csv.gz | 
  curl "http://localhost:18123/?password=changeme&query=$(cat query/03_insert_csv.sql | sed "s/ /+/g")" --data-binary @-

# データの確認
curl 'http://localhost:18123/?password=changeme' --data-binary @query/04_select_one.sql