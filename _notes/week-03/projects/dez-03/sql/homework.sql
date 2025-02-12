-- Question 3. Trip Segmentation Count
--	During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

-- 1. Up to 1 mile
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance <= 1;
-- 104802

-- 2. In between 1 (exclusive) and 3 miles (inclusive),
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 1
AND trip_distance <= 3;
-- 198924

-- 3. In between 3 (exclusive) and 7 miles (inclusive),
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 3
AND trip_distance <= 7;
-- 109603


-- 4. In between 7 (exclusive) and 10 miles (inclusive),
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 7
AND trip_distance <= 10;
-- 27678

-- 5. Over 10 miles
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 10 
-- 35189

-- Misc Sh*t
/*


	SELECT * FROM green_tripdata ORDER BY 1 ASC;


	SELECT 
	    lpep_pickup_datetime,
	    lpep_dropoff_datetime,
	    CASE
	        WHEN DATE(lpep_pickup_datetime) != DATE(lpep_dropoff_datetime) THEN 'The records cross dates'
	        ELSE 'The records do not cross dates'
	    END AS date_cross_check
	FROM green_tripdata;
	
	SELECT * FROM (
	SELECT 
	    lpep_pickup_datetime,
	    lpep_dropoff_datetime,
	    CASE
	        WHEN DATE(lpep_pickup_datetime) != DATE(lpep_dropoff_datetime) THEN 1
	        ELSE 0
	    END AS date_cross_check
	FROM green_tripdata
	) AS tbl_date_cross_check 
	WHERE date_cross_check=1;
*/