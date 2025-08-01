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
-- Table structure for table `jobpublisher`
--

DROP TABLE IF EXISTS `jobpublisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobpublisher` (
  `PublisherID` int NOT NULL AUTO_INCREMENT,
  `FName` varchar(50) NOT NULL,
  `LName` varchar(50) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `PhoneNumber` varchar(15) NOT NULL,
  `City` varchar(255) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `disability_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PublisherID`),
  UNIQUE KEY `PublisherID_UNIQUE` (`PublisherID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `PhoneNumber_UNIQUE` (`PhoneNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobpublisher`
--

LOCK TABLES `jobpublisher` WRITE;
/*!40000 ALTER TABLE `jobpublisher` DISABLE KEYS */;
INSERT INTO `jobpublisher` VALUES (1,'rasheed','alomari','rasheedalomari2002@gmail.com','Rasheed1@','0770289119','irbid','jordan','irbid','Male',NULL),(5,'rsaleem','ahmad','rasheedalomari10@gmail.com','Rasheed1@','078955420','NEW YORK','jordan','ium-qais','Male','Chronic illness'),(6,'Rasheed','al omary','2020902042@yu.edu.jo','Rasheed1@','0789654222','Amman','jordan','um qais','Male','Mobility impairment'),(7,'asd','qwe','qweewrt@asd.com','Qweqwe1@','235','fgjh','dfg','dsfgd','Male',NULL),(8,'ty','ty','ty@gmail.com','t','909090','ty','ty','ty','Male',NULL),(9,'gh','gh','gh@gmail.com','g','679546735','gh','gh','gh','Female',NULL),(10,'nm','nm','nm@gmail.com','n','325546745','nm','nm','nm','Female',NULL),(11,'Ahmed','Al-Mansoori','ahmed.mansoori@example.com','securePass123','+971501234567','Dubai','UAE','Al Khail Road 15','Male',NULL),(12,'Fatima','Al-Haddad','fatima.haddad@mail.ae','Fh@2023!','+971552345678','Abu Dhabi','UAE','Khalifa City A, Villa 27','Female',NULL),(13,'Mohammed','Al-Saud','m.alsaud@ksa.com','Ksa@7890','+966550112233','Riyadh','Saudi Arabia','Olaya Street 45','Male',NULL),(14,'Layla','Abdullah','layla.abd@madaen.sa','Layla_2023','+966544445555','Jeddah','Saudi Arabia','Al Hamra District','Female',NULL),(15,'Youssef','El-Masry','y.elmasry@egyptmail.com','NileRiver1','+201002345678','Cairo','Egypt','Maadi Street 9','Male',NULL),(16,'Noura','Al-Khalifa','noura.khalifa@qatar.qa','Q@tar1234','+97433112233','Doha','Qatar','West Bay Area','Female',NULL),(17,'Khalid','Al-Bahar','k.bahar@batelco.com','BahrainSea#1','+97334001122','Manama','Bahrain','Seef District','Male',NULL),(18,'Amira','Al-Zahra','amira.zahra@omanpost.om','ZahraMount@2','+96891234567','Muscat','Oman','Al Khuwair','Female',NULL),(19,'Tariq','Hamdi','tariq.hamdi@jordanmail.jo','Petra1234','+962790123456','Amman','Jordan','Abdoun Circle','Male',NULL),(20,'Samira','Al-Farsi','samira.farsi@kwt.net','Kuwait@456','+96590011222','Kuwait City','Kuwait','Salmiya Block 4','Female',NULL),(21,'Hassan','Al-Maghrabi','h.maghrabi@casablanca.ma','Atlas2023!','+212612345678','Casablanca','Morocco','Ain Diab','Male',NULL),(22,'Leila','Ben Ali','leila.benali@tunis.tn','Carthage#7','+21650123456','Tunis','Tunisia','Lac 2','Female',NULL),(23,'Omar','Al-Hashemi','omar.hashemi@iraqpost.iq','Tigris123','+964770123456','Baghdad','Iraq','Al Mansour','Male',NULL),(24,'Rana','Al-Amir','rana.amir@lebanon.lb','CedarTree#5','+96170123456','Beirut','Lebanon','Hamra Street','Female',NULL),(25,'Yasin','Al-Mutawa','y.mutawa@yemenpost.ye','Sanaa2023','+967712345678','Sana\'a','Yemen','Hadda Street','Male',NULL),(26,'Aisha','Al-Nuaimi','a.nuaimi@sharjah.ae','Sharjah#8','+971565432109','Sharjah','UAE','Al Khan Area','Female',NULL),(27,'Faisal','Al-Rashid','f.rashid@ksa.com','NajdDesert1','+966544332211','Dammam','Saudi Arabia','King Fahd Road','Male',NULL),(28,'Mariam','El-Shenawy','m.shenawy@alexmail.eg','AlexSea2023','+201003334444','Alexandria','Egypt','San Stefano','Female',NULL),(29,'Ziad','Al-Khatib','z.khatib@syria.sy','Damascus7','+963931234567','Damascus','Syria','Malki Street','Male',NULL),(30,'Hala','Al-Marzouq','h.marzouq@kuwaitpost.kw','Marzouq_2023','+96597778888','Al Ahmadi','Kuwait','Fahaheel','Female',NULL),(31,'cvb','cvb','cvb@gmail.com','c','34562342','cvb','cvb','cvb','Male',NULL),(32,'sura','keelani','sura2@gmail.com','Sura@2002','0789564230','amman','jordan','st 30','Female','Amputation'),(33,'eyad','harb','eyadh@gamil.com','Eyad@2001h','0796231683','','jordan','','Male',''),(34,'hussam','harb','hus@gmail.com','Hussam@2005','0866547577','irbid','jordan','st30','Male',NULL),(35,'samer','harb','samer@gamil.com','Samer@2000','0799865420','irbid','jordan','st30-st','Male',NULL),(36,'sadden','abu hana','sadeen@gmail.com','Sadeen@2004','0779865432','Amman','Jordan','Abu-nusir','Female',NULL),(37,'heba','mahafzha','heba@gmail.com','Heba@2004','079875454','irbid','Jordan','kofor jaize','Female','Spinal cord injury'),(38,'Yousef','Harb','yousef@gmail.com','Yousef@1998','079658334','irbid','Jordan','AL-Huda mosuq','Male',NULL),(39,'Ameer','Hazem','ameer@gamil.com','Ameer@2001','0789556425','Abu_nusir','jordan','amaan','Male','viusal'),(40,'mohammed','hashem','sameer@gmail.com','Sameer@01','078899662','irbid','jordan','AL-barha','Male',NULL),(41,'ahmad','samer','ahamad5@gmail.com','Ahmad@2001','05555555','bd hnd','xbhhj','sgvgbc','Male',NULL),(42,'samer','hssan','samer@gmail.com','Samer@1999','0789456231','Amman','jordan','60 st','Male',NULL);
/*!40000 ALTER TABLE `jobpublisher` ENABLE KEYS */;
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
