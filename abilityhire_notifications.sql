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
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `job_id` int NOT NULL,
  `message` text NOT NULL,
  `status` varchar(10) NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_notifications_sender` (`sender_id`),
  KEY `fk_notifications_receiver` (`receiver_id`),
  KEY `fk_notifications_job` (`job_id`),
  CONSTRAINT `fk_notifications_job` FOREIGN KEY (`job_id`) REFERENCES `job` (`JobID`) ON DELETE CASCADE,
  CONSTRAINT `fk_notifications_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `jobpublisher` (`PublisherID`) ON DELETE CASCADE,
  CONSTRAINT `fk_notifications_sender` FOREIGN KEY (`sender_id`) REFERENCES `jobseeker` (`seekerID`) ON DELETE CASCADE,
  CONSTRAINT `notifications_chk_1` CHECK ((`status` in (_utf8mb4'read',_utf8mb4'unread')))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,23,32,69,'New application received for your job: Virtual Assistant','read','2025-06-20 15:51:22','apply'),(2,23,33,65,'Khaled applied to your job: TRANSCRIPTIONIST','read','2025-06-20 15:57:36','apply'),(3,27,32,69,'Maya applied to your job: Virtual Assistant','read','2025-06-20 15:59:52','apply'),(4,21,32,69,'سرى applied to your job posted by sura: Virtual Assistant','read','2025-06-20 16:04:10','apply'),(5,23,6,57,'Khaled applied to your job posted by Rasheed:  Social Media Manager','unread','2025-06-20 16:08:34','apply'),(6,23,30,34,'Khaled applied to your job posted by Hala: Inclusion Program Manager','unread','2025-06-20 16:11:27','apply'),(7,21,6,51,'سرى applied to your job posted by Rasheed: web devlopment','unread','2025-06-20 16:22:35','apply'),(8,21,33,61,'سرى applied to your job posted by eyad: EMAIL SUPPORT REPRESENTATIVE (TEXT-ONLY)','read','2025-06-20 16:26:05','apply');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-20 18:56:02
