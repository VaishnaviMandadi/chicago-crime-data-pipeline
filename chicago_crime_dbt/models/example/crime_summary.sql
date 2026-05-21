SELECT
    primary_type,
    COUNT(*) AS total_crimes
FROM crime_data
GROUP BY primary_type
ORDER BY total_crimes DESC