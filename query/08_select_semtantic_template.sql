SELECT chunk_text FROM mame_db.vector_sample
ORDER BY
  cosineDistance(chunk_embedding, __VAR__) ASC
LIMIT 5