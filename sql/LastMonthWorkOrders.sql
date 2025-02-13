SELECT * 
FROM "tWorkOrders" 
WHERE "RequestCreateDatetime" >= date_trunc('MONTH', CURRENT_DATE - INTERVAL '1 MONTH')
	AND  "RequestCreateDatetime" >= date_trunc('MONTH', CURRENT_DATE)