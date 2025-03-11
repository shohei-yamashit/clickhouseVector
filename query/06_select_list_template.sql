SELECT
  chunk_text
FROM
  mame_db.vector_sample
WHERE
  hasSubstr(chunk_tokens, __VAR__)