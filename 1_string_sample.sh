#!/bin/bash
INPUT=$1

cat ./query/05_select_string_sample.sql | 
  sed "s/__VAR__/${INPUT}/" |
  curl 'http://localhost:18123/?password=changeme' --data-binary @-