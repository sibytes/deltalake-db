CREATE OR REPLACE TABLE `{{ database_name }}`.`TestTable2` (
  `UUID` STRING,
  `Id` BIGINT,
  `Data` STRING,
  `Type` STRING,
  `Time` TIMESTAMP
)
USING {{ format }}
LOCATION '{{ location }}'