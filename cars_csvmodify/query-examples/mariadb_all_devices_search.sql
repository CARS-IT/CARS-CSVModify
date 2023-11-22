# Create a Common Table Expression that includes the common filter data for s13ihw, s14ihw and s15iwh
WITH filtered_data AS (
  SELECT
    devices.sysName,
    ports_fdb.mac_address,
    ports.ifName,
    ports.ifSpeed,
    ports.ifType,
    ports.ifAlias
  FROM
    ports
    LEFT JOIN devices ON ports.device_id = devices.device_id
    LEFT JOIN ports_fdb ON ports.port_id = ports_fdb.port_id
  WHERE
    ports.ifName NOT IN ("Gi1/0/24", "Gi1/0/48", "Te1/0/4", "24", "28", "GigabitEthernet8", "GigabitEthernet1", "g8", "xg12", "28", "ethernet1/1/23:1", "ethernet1/1/28:1")
    AND ports.ifType NOT LIKE "prop%"
    AND ports.ifName NOT LIKE "Po%"
    AND ports.ifName NOT LIKE "CPU"
    AND ports.ifName NOT LIKE "Vl%"
    AND ports.ifName NOT LIKE "lag%"
    AND ports.ifName NOT LIKE "mgmt%"
)

# s13ihw
SELECT
  filtered_data.sysName AS "Switch Name",
  filtered_data.ifName AS Interface,
  filtered_data.ifSpeed AS Speed,
  filtered_data.ifAlias AS "Port Description",
  s13ihw.Data AS "Hostname",
  CONCAT_WS(
    ':',
    UPPER(SUBSTR((filtered_data.mac_address), 1, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 3, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 5, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 7, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 9, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 11, 2))
  ) AS "MAC Address",
  s13ihw.IP AS "IP Address",
  s13ihw.Make,
  s13ihw.Model,
  s13ihw.SerialNumber AS "Serial Number",
  s13ihw.Location
FROM
  filtered_data
  LEFT JOIN s13ihw ON filtered_data.mac_address = s13ihw.MAC
WHERE
  CASE WHEN '$hsearch' LIKE '' THEN s13ihw.Data = NULL ELSE s13ihw.Data LIKE CONCAT('%','$hsearch','%') END
  OR CASE WHEN '$msearch' LIKE '' THEN s13ihw.MAC = NULL ELSE s13ihw.MAC LIKE CONCAT('%',REPLACE(REPLACE(REPLACE('$msearch',":",""),"-",""),".",""),'%') END
  OR CASE WHEN '$ip' LIKE '' THEN s13ihw.IP = NULL ELSE s13ihw.IP LIKE CONCAT('%','$ip','%') END
  OR CASE WHEN '$sn' LIKE '' THEN s13ihw.SerialNumber = NULL ELSE s13ihw.SerialNumber LIKE CONCAT('%','$sn','%') END

UNION ALL

# s14ihw
SELECT
  filtered_data.sysName AS "Switch Name",
  filtered_data.ifName AS Interface,
  filtered_data.ifSpeed AS Speed,
  filtered_data.ifAlias AS "Port Description",
  s14ihw.Data AS "Hostname",
  CONCAT_WS(
    ':',
    UPPER(SUBSTR((filtered_data.mac_address), 1, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 3, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 5, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 7, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 9, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 11, 2))
  ) AS "MAC Address",
  s14ihw.IP AS "IP Address",
  s14ihw.Make,
  s14ihw.Model,
  s14ihw.SerialNumber AS "Serial Number",
  s14ihw.Location
FROM
  filtered_data
  LEFT JOIN s14ihw ON filtered_data.mac_address = s14ihw.MAC
WHERE
  CASE WHEN '$hsearch' LIKE '' THEN s14ihw.Data = NULL ELSE s14ihw.Data LIKE CONCAT('%','$hsearch','%') END
  OR CASE WHEN '$msearch' LIKE '' THEN s14ihw.MAC = NULL ELSE s14ihw.MAC LIKE CONCAT('%',REPLACE(REPLACE(REPLACE('$msearch',":",""),"-",""),".",""),'%') END
  OR CASE WHEN '$ip' LIKE '' THEN s14ihw.IP = NULL ELSE s14ihw.IP LIKE CONCAT('%','$ip','%') END
  OR CASE WHEN '$sn' LIKE '' THEN s14ihw.SerialNumber = NULL ELSE s14ihw.SerialNumber LIKE CONCAT('%','$sn','%') END

UNION ALL

# s15ihw
SELECT
  filtered_data.sysName AS "Switch Name",
  filtered_data.ifName AS Interface,
  filtered_data.ifSpeed AS Speed,
  filtered_data.ifAlias AS "Port Description",
  s15ihw.Data AS "Hostname",
  CONCAT_WS(
    ':',
    UPPER(SUBSTR((filtered_data.mac_address), 1, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 3, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 5, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 7, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 9, 2)),
    UPPER(SUBSTR((filtered_data.mac_address), 11, 2))
  ) AS "MAC Address",
  s15ihw.IP AS "IP Address",
  s15ihw.Make,
  s15ihw.Model,
  s15ihw.SerialNumber AS "Serial Number",
  s15ihw.Location
FROM
  filtered_data
  LEFT JOIN s15ihw ON filtered_data.mac_address = s15ihw.MAC
WHERE
  CASE WHEN '$hsearch' LIKE '' THEN s15ihw.Data = NULL ELSE s15ihw.Data LIKE CONCAT('%','$hsearch','%') END
  OR CASE WHEN '$msearch' LIKE '' THEN s15ihw.MAC = NULL ELSE s15ihw.MAC LIKE CONCAT('%',REPLACE(REPLACE(REPLACE('$msearch',":",""),"-",""),".",""),'%') END
  OR CASE WHEN '$ip' LIKE '' THEN s15ihw.IP = NULL ELSE s15ihw.IP LIKE CONCAT('%','$ip','%') END
  OR CASE WHEN '$sn' LIKE '' THEN s15ihw.SerialNumber = NULL ELSE s15ihw.SerialNumber LIKE CONCAT('%','$sn','%') END
