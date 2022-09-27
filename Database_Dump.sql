-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: yazeed2abuhummos
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CURRENCY_CONV`
--

DROP TABLE IF EXISTS `CURRENCY_CONV`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CURRENCY_CONV` (
  `Currency` varchar(3) NOT NULL,
  `ChangeRate` float NOT NULL,
  PRIMARY KEY (`Currency`),
  UNIQUE KEY `Currency` (`Currency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CURRENCY_CONV`
--

/*!40000 ALTER TABLE `CURRENCY_CONV` DISABLE KEYS */;
INSERT INTO `CURRENCY_CONV` VALUES ('EUR',1.2),('GBP',1),('USD',1.6);
/*!40000 ALTER TABLE `CURRENCY_CONV` ENABLE KEYS */;

--
-- Table structure for table `DISCOUNTS`
--

DROP TABLE IF EXISTS `DISCOUNTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DISCOUNTS` (
  `Discount` float NOT NULL,
  `UpperBound` int NOT NULL,
  `LowerBound` int NOT NULL,
  PRIMARY KEY (`Discount`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DISCOUNTS`
--

/*!40000 ALTER TABLE `DISCOUNTS` DISABLE KEYS */;
INSERT INTO `DISCOUNTS` VALUES (0,45,0),(0.05,59,45),(0.1,79,60),(0.2,90,80);
/*!40000 ALTER TABLE `DISCOUNTS` ENABLE KEYS */;

--
-- Table structure for table `HOTELS`
--

DROP TABLE IF EXISTS `HOTELS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HOTELS` (
  `HotelLocation` varchar(64) NOT NULL,
  `NumberOfRooms` int NOT NULL,
  `PricePeak` int NOT NULL,
  `PriceOffPeak` int NOT NULL,
  `Description` varchar(500) NOT NULL DEFAULT 'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.',
  PRIMARY KEY (`HotelLocation`),
  UNIQUE KEY `HotelLocation` (`HotelLocation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HOTELS`
--

/*!40000 ALTER TABLE `HOTELS` DISABLE KEYS */;
INSERT INTO `HOTELS` VALUES ('Aberdeen',80,140,60,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Belfast',80,130,60,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Birmingham',90,150,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Bristol',90,140,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Cardiff',80,120,60,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Edinburgh',90,160,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Glasgow',100,150,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('London',120,200,80,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Manchester',110,180,80,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('New Castle',80,100,60,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Norwich',80,100,60,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Nottingham',100,120,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Oxford',80,180,70,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Plymouth',80,180,50,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.'),('Swansea',80,120,50,'Like real-life hotels, there are beautiful beds and TVs in the rooms. There is a pool for guests outside. Along with log cabins and mansions, there is also a fireplace in the suites.');
/*!40000 ALTER TABLE `HOTELS` ENABLE KEYS */;

--
-- Table structure for table `REFUNDS`
--

DROP TABLE IF EXISTS `REFUNDS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REFUNDS` (
  `Refund` float NOT NULL,
  `UpperBound` int NOT NULL,
  `LowerBound` int NOT NULL,
  PRIMARY KEY (`Refund`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REFUNDS`
--

/*!40000 ALTER TABLE `REFUNDS` DISABLE KEYS */;
INSERT INTO `REFUNDS` VALUES (0,29,0),(0.5,59,30),(1,90,60);
/*!40000 ALTER TABLE `REFUNDS` ENABLE KEYS */;

--
-- Table structure for table `RESERVATIONS`
--

DROP TABLE IF EXISTS `RESERVATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RESERVATIONS` (
  `ReservationId` int NOT NULL AUTO_INCREMENT,
  `UserEmail` varchar(64) DEFAULT NULL,
  `HotelLocation` varchar(64) NOT NULL,
  `RoomType` varchar(32) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `TotalPrice` int NOT NULL,
  `Currency` varchar(3) NOT NULL,
  `NumberOfPeople` int NOT NULL,
  `DateOfBooking` date NOT NULL,
  `Cancelled` tinyint(1) NOT NULL,
  PRIMARY KEY (`ReservationId`),
  UNIQUE KEY `ReservationId` (`ReservationId`),
  KEY `UserEmail` (`UserEmail`),
  KEY `HotelLocation` (`HotelLocation`),
  KEY `RoomType` (`RoomType`),
  KEY `Currency` (`Currency`),
  CONSTRAINT `RESERVATIONS_ibfk_1` FOREIGN KEY (`UserEmail`) REFERENCES `USERS` (`UserEmail`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `RESERVATIONS_ibfk_2` FOREIGN KEY (`HotelLocation`) REFERENCES `HOTELS` (`HotelLocation`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `RESERVATIONS_ibfk_3` FOREIGN KEY (`RoomType`) REFERENCES `ROOMS` (`RoomType`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `RESERVATIONS_ibfk_4` FOREIGN KEY (`Currency`) REFERENCES `CURRENCY_CONV` (`Currency`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10300 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RESERVATIONS`
--

/*!40000 ALTER TABLE `RESERVATIONS` DISABLE KEYS */;
/*!40000 ALTER TABLE `RESERVATIONS` ENABLE KEYS */;

--
-- Table structure for table `ROOMS`
--

DROP TABLE IF EXISTS `ROOMS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ROOMS` (
  `RoomType` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PercentageOfRooms` float NOT NULL,
  `PricePercentage` float NOT NULL,
  `MaxCapacity` int NOT NULL,
  `ExtraPriceForGuest` float NOT NULL,
  PRIMARY KEY (`RoomType`),
  UNIQUE KEY `RoomType` (`RoomType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROOMS`
--

/*!40000 ALTER TABLE `ROOMS` DISABLE KEYS */;
INSERT INTO `ROOMS` VALUES ('Double',0.5,0.2,2,0.1),('Family',0.2,0.5,6,0),('Standard',0.3,0,1,0);
/*!40000 ALTER TABLE `ROOMS` ENABLE KEYS */;

--
-- Table structure for table `USERS`
--

DROP TABLE IF EXISTS `USERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USERS` (
  `UserEmail` varchar(64) NOT NULL,
  `PasswordHash` varchar(128) NOT NULL,
  `UserFName` varchar(32) NOT NULL,
  `UserLName` varchar(32) NOT NULL,
  `UserAddress` varchar(256) NOT NULL,
  `UserPhone` varchar(15) NOT NULL,
  PRIMARY KEY (`UserEmail`),
  UNIQUE KEY `UserEmail` (`UserEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USERS`
--

/*!40000 ALTER TABLE `USERS` DISABLE KEYS */;
INSERT INTO `USERS` VALUES ('admin@hhotels.co.uk','$5$rounds=535000$VPVx8vG8FOwxYazm$BQttQV1ySdjbPw5tTET3oOazgEL9XZajR8rqjrvEAL2','admin','user','BS16','0192837465'),('user@gmail.com','$5$rounds=535000$.ZwQtyz3vFi8JWVF$KkF89VXVCantQC0utvjyYQfOcc95rhLGcKPX4/8y2e0','standard','user','hviwj','235790438904279');
/*!40000 ALTER TABLE `USERS` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-04 19:24:50
