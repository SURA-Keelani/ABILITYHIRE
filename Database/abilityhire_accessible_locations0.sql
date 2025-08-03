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
-- Table structure for table `accessible_locations`
--

DROP TABLE IF EXISTS `accessible_locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accessible_locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  `features` text,
  `address` varchar(255) DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `opening_hours` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessible_locations`
--

LOCK TABLES `accessible_locations` WRITE;
/*!40000 ALTER TABLE `accessible_locations` DISABLE KEYS */;
INSERT INTO `accessible_locations` VALUES (1,'المركز الوطني للصحة النفسية – الفحيص','mental health','دعم نفسي, وصول كرسي متحرك','الفحيص, الأردن',32.0027,35.7829,'+962-6-1234567','9:00 AM - 5:00 PM'),(2,'مركز إرادة – مركز تأهيل وتشغيل الأشخاص ذوي الإعاقة','rehabilitation, employment training','تدريب مهني, لغة إشارة, دعم حركي','عمّان, الأردن',31.9741,35.9023,'+962-6-2345678','8:00 AM - 4:00 PM'),(3,'مركز زها الثقافي – عمّان','cultural, disability activities','أنشطة ترفيهية, مساحات آمنة, وصول حركي','عمّان, الأردن',31.9802,35.8577,'+962-6-3456789','10:00 AM - 6:00 PM'),(4,'جمعية الشلل الدماغي الأردنية – عمّان','rehabilitation','تأهيل, دعم تعليمي, مدخل خاص','عمّان, الأردن',31.971,35.9042,'+962-6-4567890','9:00 AM - 5:00 PM'),(5,'مركز الأمل للتربية الخاصة – إربد','special education','تعليم فردي, برامج تعديل سلوك','إربد, الأردن',32.5569,35.8469,'+962-2-5678901','8:30 AM - 3:30 PM'),(6,'مركز الحياة الأفضل – الزرقاء','rehabilitation','تدريب, دمج مجتمعي','الزرقاء, الأردن',32.0613,36.088,'+962-5-6789012','9:00 AM - 5:00 PM'),(7,'أكاديمية المكفوفين – طبربور','education, visual impairment','تعليم برايل, مواد صوتية, ممرات مرشدة','طبربور, الأردن',32.0145,35.9393,'+962-6-7890123','8:00 AM - 4:00 PM'),(8,'مستشفى الجامعة الأردنية – عمّان','medical, visual and mobility support','خدمات طبية شاملة, دعم حركي وبصري','عمّان, الأردن',32.0015,35.8709,'+962-6-8901234','24 ساعة');
/*!40000 ALTER TABLE `accessible_locations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-20 19:40:06
