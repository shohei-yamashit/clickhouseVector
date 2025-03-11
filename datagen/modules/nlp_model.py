from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer
import torch

MODEL_NAME = "cl-nagoya/ruri-large"
# モデルとトークナイザーをダウンロード
model = SentenceTransformer(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

def get_embeddings(text):
    """
    テキストの埋め込みベクトルを取得する関数

    Args:
        text (str): 入力テキスト

    Returns:
        torch.Tensor: 埋め込みベクトル
    """
    embeddings = model.encode(text, convert_to_tensor=True)
    return embeddings

def tokenize_text(text):
    """
    テキストをトークン化する関数

    Args:
        text (str): 入力テキスト

    Returns:
        list: トークンのリスト
    """
    tokens = tokenizer.tokenize(text)
    return tokens