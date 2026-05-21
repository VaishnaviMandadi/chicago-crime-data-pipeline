SELECT
    year,
    month,
    crime_category,
    COUNT(*) AS total_crimes
FROM crime_data
GROUP BY
    year,
    month,
    crime_category
ORDER BY
    year,
    month,
    total_crimes DESC