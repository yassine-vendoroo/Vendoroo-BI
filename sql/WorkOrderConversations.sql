SELECT 
    cm."Id", 
    cm."SendDatetime", 
    cm."FK_WorkOrderId" "WorkOrderId", 
    cm."MessageType",
    cm."ChannelType", 
	CASE 
        WHEN cm."AgentIdType" = 4 THEN 'AI'
        WHEN u."FK_RoleId" = 1 THEN 'PropertyManager'
        WHEN u."FK_RoleId" = 2 THEN 'Assistant'
        WHEN u."FK_RoleId" = 3 THEN 'Resident'
        WHEN u."FK_RoleId" = 4 THEN 'Technician'
        WHEN u."FK_RoleId" = 5 THEN 'Vendor'
        WHEN u."FK_RoleId" = 6 THEN 'Estimator'
        WHEN u."FK_RoleId" = 7 THEN 'Owner'
        WHEN u."FK_RoleId" = 8 THEN 'ExternalAutomatedCommunicator'
        WHEN u."FK_RoleId" = 9 THEN 'Supervisor'
        WHEN u."FK_RoleId" = 100 THEN 'SuperAdmin'
        ELSE 'Unknown'
    END AS "SenderRoleName",
    CASE 
        WHEN ur."FK_RoleId" = 1 THEN 'PropertyManager'
        WHEN ur."FK_RoleId" = 2 THEN 'Assistant'
        WHEN ur."FK_RoleId" = 3 THEN 'Resident'
        WHEN ur."FK_RoleId" = 4 THEN 'Technician'
        WHEN ur."FK_RoleId" = 5 THEN 'Vendor'
        WHEN ur."FK_RoleId" = 6 THEN 'Estimator'
        WHEN ur."FK_RoleId" = 7 THEN 'Owner'
        WHEN ur."FK_RoleId" = 8 THEN 'ExternalAutomatedCommunicator'
        WHEN ur."FK_RoleId" = 9 THEN 'Supervisor'
        WHEN ur."FK_RoleId" = 100 THEN 'SuperAdmin'
        ELSE 'Unknown'
    END AS "ReceiverRoleName",
    cm."Text", 
    cm."AIData",
    wo."Name" AS "WorkOrderName"
    
FROM 
    public."tChatMessages" cm
JOIN 
    public."tWorkOrders" wo ON cm."FK_WorkOrderId" = wo."Id"
JOIN 
    public."tUsers" u ON cm."FK_SenderId" = u."Id"
LEFT JOIN 
    public."tUsers" ur ON cm."FK_RecieverId" = ur."Id"
WHERE  
    cm."IsDeleted" = false
    AND cm."MessageType" != 1005
    AND NOT (cm."MessageType" = 0 AND (cm."Text" = '' OR cm."Text" IS NULL) AND cm."FK_RecieverId" is NULL)
    -- AND (cm."ChannelType" IN (1, 2, 3) OR cm."MessageType" = 1000 OR cm."MessageType" IN (1034, 1035, 1036, 1037))
    AND cm."FK_WorkOrderId" IN ({WorkOrderIds})
ORDER BY
    cm."SendDatetime" ASC
