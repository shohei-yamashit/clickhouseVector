from pydantic import BaseModel, Field
from datetime import datetime

class ChunkedDocument(BaseModel):
  """_summary_
  テキストファイルを読み込み、本文を空行で区切ってチャンクに分割する
  - all_documents: チャンクを結合した本文
  - url: ニュース記事のURL
  - timestamp: ニュース記事のタイムスタンプ
  - caption: ニュース記事のキャプション
  - chunks: 本文を空行で区切ったチャンクのリスト
  
  """
  all_documents: str
  url: str
  timestamp: str
  caption: str
  chunks: list[str]

def chunk_text(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

    # 先頭のURL、タイムスタンプ、キャプションを抽出
    url = lines[0].strip()
    timestamp = lines[1].strip()
    caption = lines[2].strip()

    # タイムスタンプを "YYYY-MM-DD hh:mm:ss" 形式に変換
    try:
        timestamp_dt = datetime.fromisoformat(timestamp)
        formatted_timestamp = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        formatted_timestamp = timestamp  # 変換に失敗した場合は元の形式を使用

    # 残りの本文を空行で分割
    body_lines = lines[3:]
    chunks = []
    current_chunk = []

    for line in body_lines:
      if line.strip() == '':
        if current_chunk:
          chunks.append(''.join(current_chunk).strip())
          current_chunk = []
      else:
        current_chunk.append(line)

    # 最後のチャンクを追加
    if current_chunk:
      chunks.append(''.join(current_chunk).strip())
    
    # chunksをすべて結合してall_documentsに格納
    all_documents = ''.join(chunks)

    return ChunkedDocument(
      all_documents=all_documents,
      url=url,
      timestamp=formatted_timestamp,
      caption=caption,
      chunks=chunks
    )

if __name__ == '__main__':
  # 使用例
  file_path = './text/it-life-hack/it-life-hack-6296655.txt'
  chunked_document = chunk_text(file_path)
  chunked_document_dict = chunked_document.model_dump()
  resitired_chunked_document = ChunkedDocument(**chunked_document_dict)
  print(resitired_chunked_document)