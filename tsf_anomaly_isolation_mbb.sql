CREATE TABLE `tsf`.`anomaly_isolation_mbb` (
  `Date` VARCHAR(45) NOT NULL,
  `Open` DECIMAL(18,6) NULL,
  `High` DECIMAL(18,6) NULL,
  `Low` DECIMAL(18,6) NULL,
  `Close` DECIMAL(18,6) NULL,
  `Adj_Close` DECIMAL(18,6) NULL,
  `Volume` INT NULL,
  `Anomaly_Flag` INT NULL,
  `Yesterday_Close` DECIMAL(18,6) NULL,
  `Percentage_Change` DECIMAL(18,6) NULL
  PRIMARY KEY (`Date`));

 CREATE TABLE `tsf-project-344410.`.`anomaly_isolation` (
  `Date` VARCHAR(45),
  `Open` DECIMAL(18,2),
  `High` DECIMAL(18,2),
  `Low`  DECIMAL(18,2),
  `Close` DECIMAL(18,2),
  `Adj_Close` DECIMAL(18,2),
  `Volume` INT,
  `Anomaly_Flag` INT,
  `Yesterday_Close` DECIMAL(18,2),
  `Percentage_Change` DECIMAL(18,2))
  