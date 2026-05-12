SELECT
  *
FROM
  `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE
  -- Filter to 2023 trips
  EXTRACT(YEAR FROM trip_start_timestamp) = 2023
  
  -- Filter to credit card payments only
  AND payment_type = 'Credit Card'
  
  -- Data Quality: Remove invalid rows (Zero miles/time/fare and negative tips)
  AND trip_miles > 0
  AND trip_seconds > 0
  AND fare > 0
  AND tips >= 0
  
  -- Data Quality: Drop rows missing critical location or business identifiers
  AND pickup_community_area IS NOT NULL
  AND company IS NOT NULL;