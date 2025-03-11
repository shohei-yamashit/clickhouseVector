SELECT
  chunk_text
FROM
  mame_db.vector_sample
WHERE
  chunk_text LIKE '%__VAR__%'