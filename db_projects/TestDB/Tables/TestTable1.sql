CREATE TABLE `{{ database_name }}`.`TestTable1` (
  `UUID` STRING,
  `Id` BIGINT,
  `Data` STRING,
  `Type` STRING,
  `Time` TIMESTAMP
)
USING {{ format }}
LOCATION '{{ location }}'
