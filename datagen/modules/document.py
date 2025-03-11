import hashlib
from modules.chunk import chunk_text, ChunkedDocument
from modules.nlp_model import get_embeddings, tokenize_text
from typing import List
from pydantic import BaseModel
import os

class Document(BaseModel):
    """
    実際のCSVレコード
    - id
    - url
    - time_stamp
    - document_path
    - caption
    - caption_tokens
    - caption_embedding
    - chunk_text
    - chunk_tokens
    - chunk_embedding
    - all_text
    - all_embedding
    - caption_similarity: caption_embeddingとchunk_embeddingの類似度
    """
    id: str
    chunk_id: int
    url: str
    timestamp: str
    document_path: str
    caption_text: str
    caption_tokens: list[str]
    caption_embedding: list[float]
    chunk_text: str
    chunk_tokens: list[str]
    chunk_embedding: list[float]
    all_text: str

def get_documents_by_path(in_path: str) -> List[Document]:
    """
    ドキュメントをチャンクに分割し、各チャンクをCSVに書き込む
    """
    result = []
    chunkedDocument: ChunkedDocument = chunk_text(in_path)
    for i in range(len(chunkedDocument.chunks)):
        chunk = chunkedDocument.chunks[i]
        caption_embedding = get_embeddings(chunkedDocument.caption)
        chunk_embedding = get_embeddings(chunk)
        document_hash = hashlib.sha256(f"{in_path}".encode('utf-8')).digest().hex()
        document = Document(
            id=f"{document_hash}-{i}",
            chunk_id=i,
            url=chunkedDocument.url,
            timestamp=chunkedDocument.timestamp,
            document_path=in_path,
            caption_text=chunkedDocument.caption,
            caption_tokens=tokenize_text(chunkedDocument.caption),
            caption_embedding=caption_embedding,
            chunk_text=chunk,
            chunk_tokens=tokenize_text(chunk),
            chunk_embedding=chunk_embedding,
            all_text=chunkedDocument.all_documents,
        )
        result.append(document)
    return result

def list_txt_files(directory):
    """
    指定されたディレクトリ内のすべての .txt ファイル名の一覧を返す関数

    Args:
        directory (str): ディレクトリのパス

    Returns:
        list: .txt ファイル名のリスト
    """
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_files.append("{}/{}".format(directory, filename))
    return txt_files
  
if __name__ == '__main__':
    in_path = './text/it-life-hack/it-life-hack-6296655.txt'
    out_path = './output.csv'
    documents = get_documents_by_path(in_path)
    print(documents)
    print("完了しました")
    