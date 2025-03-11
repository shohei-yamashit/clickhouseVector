WITH hassubstr_table AS (
    SELECT
        row_number() OVER (ORDER BY query_start_time DESC) AS row_number,
        'hasSubstr' AS type,
        query_start_time,
        query_duration_ms
    FROM
        system.query_log
    WHERE
        query LIKE '%hasSubstr%'
        AND query NOT LIKE '%system.query_log%'
    ORDER BY
        query_start_time DESC
    LIMIT 4
),
like_table AS (
    SELECT
        row_number() OVER (ORDER BY query_start_time DESC) AS row_number,
        'liketable' AS type,
        query_start_time,
        query_duration_ms
    FROM
        system.query_log
    WHERE
        query LIKE '%LIKE%'
        AND query NOT LIKE '%system.query_log%'
    ORDER BY
        query_start_time DESC
    LIMIT 4
)

SELECT
    hassubstr_table.row_number,
    hassubstr_table.type,
    hassubstr_table.query_start_time,
    hassubstr_table.query_duration_ms,
    like_table.type,
    like_table.query_start_time,
    like_table.query_duration_ms
FROM
    hassubstr_table
JOIN
    like_table
ON
    hassubstr_table.row_number = like_table.row_number
ORDER BY
    hassubstr_table.row_number
LIMIT 4