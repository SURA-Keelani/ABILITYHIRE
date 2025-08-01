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
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job` (
  `JobID` int NOT NULL AUTO_INCREMENT,
  `PostingDate` date NOT NULL,
  `Salary` decimal(10,2) NOT NULL,
  `City` varchar(255) NOT NULL,
  `Status` enum('Open','Closed','In Progress') NOT NULL DEFAULT 'Open',
  `jobtitle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `jobdescription` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PublisherID` int NOT NULL,
  `disability_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`JobID`),
  UNIQUE KEY `JobID_UNIQUE` (`JobID`),
  KEY `fk_job_publisher` (`PublisherID`),
  FULLTEXT KEY `JobTitle` (`jobtitle`),
  FULLTEXT KEY `ft_jobtitle_jobdescription` (`jobtitle`,`jobdescription`),
  CONSTRAINT `fk_job_publisher` FOREIGN KEY (`PublisherID`) REFERENCES `jobpublisher` (`PublisherID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
INSERT INTO `job` VALUES (20,'2023-11-05',42000.00,'Dubai','Open','Inclusive Education Coordinator','Develop accessible learning programs. Workplace has wheelchair ramps and sensory-friendly spaces. Sign language skills preferred.',17,NULL),(21,'2023-10-25',38000.00,'Riyadh','Open','Captioning Specialist','Create Arabic/English closed captions for media. Remote work available. Accommodations for hearing impairments provided.',23,NULL),(29,'2023-11-10',55000.00,'Abu Dhabi','Open','Disability Employment Consultant','Advise companies on inclusive hiring practices. Flexible schedule with hybrid work options. Chronic illness-friendly environment.',14,NULL),(30,'2023-11-02',32000.00,'Remote','Open','Virtual Assistant','Administrative support role with adjustable workload. Suitable for neurodiverse candidates or those with mobility challenges.',28,NULL),(31,'2023-10-28',65000.00,'Doha','In Progress','Accessible UX Designer','Design WCAG-compliant digital interfaces. Office has screen reader stations & ergonomic workstations. Autism-friendly workplace.',11,NULL),(32,'2023-11-07',45000.00,'Kuwait City','Open','Sign Language Interpreter','Provide interpretation services. Training available. Workplace offers mental health support and flexible breaks.',25,NULL),(33,'2023-11-03',40000.00,'Remote','Open','Content Writer (Disability Focus)','Create inclusive content about accessibility. Chronic pain-friendly schedule with adjustable deadlines. Voice-to-text accommodation available.',19,NULL),(34,'2023-10-30',52000.00,'Jeddah','Open','Inclusion Program Manager','Develop workplace accessibility initiatives. Office has wheelchair access and quiet rooms. PTSD-aware environment.',30,NULL),(35,'2023-11-08',36000.00,'Remote','Open','Online Therapy Coordinator','Match clients with disability specialists. Work-from-home with equipment provided. Accommodations for various disabilities available.',16,NULL),(38,'2025-05-17',123.00,'qwe','Open','qwe','qwe',20,NULL),(42,'2025-05-17',321.00,'asd','Open','asd','asd',20,NULL),(43,'2025-05-17',456.00,'fgh','Closed','fgh','fgh',6,NULL),(44,'2025-05-20',70000.00,'tyu','Open','tyu','tyu',6,NULL),(47,'2025-06-01',25000.00,'dubai','Open','Screen Reader','screen reader',6,NULL),(48,'2025-06-01',250000.00,'kjbnjk','Open','bnm','mjb',6,NULL),(50,'2025-06-01',25400.00,'Dubai','Open','screen Reader','A screen reader is a software application that converts digital text and other content displayed on a computer or mobile screen into synthesized speech or braille output. It allows users with visual impairments or blindness to navigate websites, read documents, and interact with digital devices independently by vocalizing on-screen information and providing keyboard-based navigation',5,'Epilepsy'),(51,'2025-06-01',5205.00,'yafa','Open','web devlopment','Remote',6,'Speech disability'),(52,'2025-06-02',250000.00,'irbid','Open','REMOTE CUSTOMER SUPPORT REPRESENTATIVE','We are committed to creating an inclusive and accessible work environment. We are seeking Customer Support Representatives who are passionate about helping others and can provide exceptional service via email, chat, or phone — all from the comfort of home.\r\n\r\nThis position is particularly suitable for individuals with physical, sensory, or mild cognitive disabilities, as it offers full remote work, reasonable accommodations, and assistive technologies as needed.',6,'Autism spectrum disorder'),(53,'2025-06-02',550.00,'irbid','Open','Customer Support Agent (Voice or Chat)','Join our inclusive customer service team as a Support Agent, helping customers resolve issues via chat or phone. Ideal for individuals with hearing or mobility impairments. Chat-based positions are available for those who prefer text communication.',11,'Muscular dystrophy'),(54,'2025-06-02',9500.00,'Amman','Open',' Content Writer / Blogger','We’re hiring Content Writers to create engaging articles, blog posts, or product descriptions. This job is perfect for people with disabilities who love writing and working independently from home.',11,'Multiple sclerosis'),(55,'2025-06-02',650000.00,'Texas','Open',' Graphic Designer','A creative and inclusive environment awaits a Graphic Designer to work on logos, social media visuals, and marketing materials. Ideal for candidates with physical disabilities who enjoy creative tools and visual storytelling.',38,'Autism spectrum disorder'),(56,'2025-06-02',95520.00,'Qater','Closed','QA Tester / Accessibility Tester','Join our tech team as a Quality Assurance (QA) Tester, especially testing the accessibility of web and mobile apps. This job is ideal for individuals with disabilities, as your insights help us improve digital inclusion.',32,'Hearing impairment'),(57,'2025-06-02',25800.00,'Dubai','Open',' Social Media Manager','Join our marketing team as a Social Media Manager, planning and posting engaging content for platforms like Instagram, LinkedIn, and Facebook. This role is perfect for individuals with disabilities who enjoy creativity, communication, and working from home.',6,'Speech disability'),(58,'2025-06-02',25564.00,'Qater','Open','Social Media Manager','Join our marketing team as a Social Media Manager, planning and posting engaging content for platforms like Instagram, LinkedIn, and Facebook. This role is perfect for individuals with disabilities who enjoy creativity, communication, and working from home.',37,'Epilepsy'),(59,'2025-06-02',65600.00,'Dubai','Open',' Document Scanning & Digitization Assistant','We are seeking a Scanning and Digitization Assistant to convert physical files into digital formats. This on-site role is suitable for people with mild physical disabilities and offers a calm, organized working environment.',37,'Amputation'),(60,'2025-06-02',65400.00,'Amman','Open','AUDIO CONTENT CREATOR / PODCAST EDITOR','We are looking for someone with a passion for sound and storytelling to join our team as an Audio Content Creator. If you are comfortable with sound editing and vocal recording, this role is a great fit — no screen use is required.\r\n\r\nKey Tools: Screen reader-compatible audio software (e.g., Audacity, Reaper)\r\nAccessibility: Keyboard navigation support, audio-only workflow',37,'Learning disability'),(61,'2025-06-02',45025.00,'tisas','Open','EMAIL SUPPORT REPRESENTATIVE (TEXT-ONLY)','Provide excellent customer service through written communication only. No voice or phone tasks are required. You’ll handle email tickets and live chat support.\r\n\r\nKey Tools: Helpdesk systems (e.g., Zendesk), Gmail, Intercom\r\nAccessibility: All communication is written, no verbal interactions needed',33,'Deafblindness'),(62,'2025-06-02',65056.00,'Amman','Open','Online Tutor / E-Learning Assistant','Passionate about teaching? Become an Online Tutor in subjects like math, English, or science. This flexible position is suitable for individuals with hearing or mobility impairments who want to support student learning from home.\r\n\r\nResponsibilities:\r\n\r\nConduct virtual lessons using Zoom or Google Meet\r\n\r\nProvide personalized help and feedback\r\n\r\nTrack student progress',33,'Spinal cord injury'),(63,'2025-06-02',65484.00,'Amman','Open','Virtual Bookkeeper / Accounting Assistant','We are hiring a detail-focused Virtual Bookkeeper to help with managing financial records, invoices, and basic accounting. This job suits individuals with physical disabilities or chronic illnesses who prefer working remotely.',33,'Mobility impairment'),(64,'2025-06-02',6580.00,'Amman','Open','WEB ACCESSIBILITY TESTER','Test websites for accessibility compliance using screen readers or keyboard navigation. Especially suitable for users who use these tools themselves.',33,'Amputation'),(65,'2025-06-02',65446.00,'Aqaba','Open','TRANSCRIPTIONIST','TRANSCRIPTIONIST',33,'Deafblindness'),(66,'2025-06-02',65450.00,'Amman','Open','Web Dvloper','remote',32,'Muscular dystrophy'),(67,'2025-06-03',65464.00,'Amman','Open','UI','Make a ui interface',32,'Mental health condition'),(68,'2025-06-04',65420.00,'Amman','Open','web devlobment','ui/ux design',32,'Speech disability'),(69,'2025-06-20',6540.00,'Amman','Open','Virtual Assistant','Manage emails, appointments, schedules, and online tasks.\r\n\r\nCan be done entirely from home.\r\n\r\nIdeal for individuals with mobility issues or anxiety disorders.',32,'Visual impairment'),(77,'2025-07-16',352220.00,'Amman','Open','Full stack','remotly - full stack ',32,'Cerebral palsy');
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
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
