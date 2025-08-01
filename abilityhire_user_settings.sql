-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: abilityhire
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_settings`
--

DROP TABLE IF EXISTS `user_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_settings` (
  `setting_id` int NOT NULL AUTO_INCREMENT,
  `seeker_id` int DEFAULT NULL,
  `publisher_id` int DEFAULT NULL,
  `font_size` varchar(10) NOT NULL DEFAULT '16px',
  `notifications` tinyint(1) NOT NULL DEFAULT '1',
  `dark_theme` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`setting_id`),
  UNIQUE KEY `idx_seeker_settings` (`seeker_id`),
  UNIQUE KEY `idx_publisher_settings` (`publisher_id`),
  CONSTRAINT `user_settings_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `jobseeker` (`seekerID`) ON DELETE CASCADE,
  CONSTRAINT `user_settings_ibfk_2` FOREIGN KEY (`publisher_id`) REFERENCES `jobpublisher` (`PublisherID`) ON DELETE CASCADE,
  CONSTRAINT `chk_user_type` CHECK ((((`seeker_id` is not null) and (`publisher_id` is null)) or ((`seeker_id` is null) and (`publisher_id` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_settings`
--

LOCK TABLES `user_settings` WRITE;
/*!40000 ALTER TABLE `user_settings` DISABLE KEYS */;
INSERT INTO `user_settings` VALUES (1,1,NULL,'16px',1,0),(2,NULL,6,'16px',0,0),(7,NULL,32,'20px',1,0),(9,NULL,36,'20px',1,0),(16,NULL,37,'16px',1,0),(18,NULL,5,'18px',1,0),(19,29,NULL,'16px',1,0),(21,23,NULL,'16px',1,0),(24,21,NULL,'16px',1,0),(30,NULL,41,'16px',0,0),(33,NULL,33,'16px',1,0);
/*!40000 ALTER TABLE `user_settings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-20 18:56:03
