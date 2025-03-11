#!/bin/bash
# データの検索
curl 'http://localhost:18123/?password=changeme' --data-binary @query/07_query_log_string.sql