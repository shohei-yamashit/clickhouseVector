-- テーブルの作成
CREATE TABLE IF NOT EXISTS mame_db.vector_sample
(
    id String,
    chunk_id Int32,
    url String,
    timestamp DateTime,
    document_path String,
    caption_text String,
    caption_tokens Array(String),
    caption_embedding Array(Float32),
    chunk_text String,
    chunk_tokens Array(String),
    chunk_embedding Array(Float32),
    all_text String
)
ENGINE = MergeTree()
ORDER BY id;