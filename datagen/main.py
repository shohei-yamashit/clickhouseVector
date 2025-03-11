import random
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from modules.document import get_documents_by_path, list_txt_files, Document
import csv
import gzip
import shutil

OUT_CSV_PATH = 'output.csv'
SEED = 42

class Counter:
    lock = Lock()
    
    def process_file(self, file_path):
        documents = get_documents_by_path(file_path)
        with self.lock:
            with open(OUT_CSV_PATH, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for document in documents:
                    
                    writer.writerow([
                        document.id, document.chunk_id, document.url, document.timestamp, document.document_path,
                        document.caption_text.replace('\n', ' ').replace('\r', ' '), 
                        document.caption_tokens, document.caption_embedding,
                        document.chunk_text.replace('\n', ' ').replace('\r', ' '), 
                        document.chunk_tokens, document.chunk_embedding, document.all_text.replace('\n', ' ').replace('\r', ' ')
                    ])
                
                    # 書き込みが確実にディスクに反映されるようにフラッシュする
                    f.flush()
                    os.fsync(f.fileno())

def worker(counter: Counter, file_paths):
    """各スレッドで実行される関数"""
    for file_path in file_paths:
        counter.process_file(file_path)

def chunk_list(lst, chunk_size):
    """リストを指定したチャンクサイズで分割する関数"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def main():
    target_dir = ['./text/it-life-hack', './text/movie-enter', './text/sports-watch']
        
    # 入力テキストリスト
    nested_txt_files = [list_txt_files(dir) for dir in target_dir]
    
    # ファイルリストを平坦化し、ランダムに4%を選定
    file_list = [file for sublist in nested_txt_files for file in sublist]
    sample_size = max(1, int(len(file_list) * 0.06))
    # randomのシード値を設定
    random.seed(SEED)
    
    sampled_file_list = random.sample(file_list, sample_size)
    
    # 出力ファイルが存在する場合は削除
    if os.path.exists(OUT_CSV_PATH):
        os.remove(OUT_CSV_PATH)
    
    # スレッド数を定義
    num_threads = 4
    
    # 各スレッドに割り当てるメッセージの数を計算
    chunks = chunk_list(sampled_file_list, len(sampled_file_list) // num_threads)
    
    counter = Counter()
    
    # ThreadPoolExecutorを使用してスレッドプールを作成
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # スレッドをプールに提出
        futures = [executor.submit(worker, counter, chunks[i]) for i in range(num_threads)]
    
    with open(OUT_CSV_PATH, 'rb') as f_in:
        with gzip.open(f"{OUT_CSV_PATH}.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    print("All threads have finished.")

if __name__ == "__main__":
    main()