SELECT
  # Selects specific columns from ports table 
  ports.ifName AS Interface,
  ports.ifOperStatus AS Status,
  ports.ifAdminStatus AS Admin,
  ports.ifSpeed AS Speed,
  ports.ifAlias AS Description,
  s13ihw.IP AS "IP Address",

  # Formats MAC Address to match between data sources.  ie, aabbcc112233 to AA:BB:CC:11:22:33
  CONCAT_WS(
    ':',
    UPPER(SUBSTR((ports_fdb.mac_address), 1, 2)),
    UPPER(SUBSTR((ports_fdb.mac_address), 3, 2)),
    UPPER(SUBSTR((ports_fdb.mac_address), 5, 2)),
    UPPER(SUBSTR((ports_fdb.mac_address), 7, 2)),
    UPPER(SUBSTR((ports_fdb.mac_address), 9, 2)),
    UPPER(SUBSTR((ports_fdb.mac_address), 11, 2))
  ) AS "MAC Address",

  # Selects specific columns from s13ihw table, which contains data exported from IHW
  #GROUP_CONCAT(s13ihw.Hostname SEPARATOR ' | ') AS "Hostname(s)",
  # Hostname should be Data to include the correct information for hosts.
  s13ihw.Data AS "Hostname",
  s13ihw.Make,
  s13ihw.Model,
  s13ihw.SerialNumber AS "Serial Number",
  s13ihw.Location

FROM
  ports

  # Matches similar fields from different tables, devices/ports (device_id), ports/ports_fdb (port_id), and ports_fdb/s13ihw (mac_address/MAC)
  LEFT JOIN devices ON ports.device_id = devices.device_id
  LEFT JOIN ports_fdb ON ports.port_id = ports_fdb.port_id
  LEFT JOIN s13ihw ON ports_fdb.mac_address = s13ihw.MAC

WHERE
  #Uses $switch variable to select which switch to view, using dropdown box
  devices.sysName = '$switch'

  #Filter out unwanted data
  AND ports.ifType NOT LIKE "prop%"
  AND ports.ifName NOT LIKE "Po%"
  AND ports.ifName NOT LIKE "CPU"
  AND ports.ifName NOT LIKE "Vl%"
  AND ports.ifName NOT LIKE "lag%"
  AND ports.ifName NOT LIKE "mgmt%"
  #Filter out uplinks
  #AND ports.ifName NOT LIKE "GigabitEthernet8"
  #AND ports.ifAlias NOT LIKE "Uplink"

#Filters out ports with duplicate ifName values.  This needs to be modified to be more useful
#GROUP BY ports.ifName

#Ensures results are ordered correctly.  Ex: Gi1/0/1, Gi1/0/2, etc
ORDER BY
  ports.port_id,
  s13ihw.Data