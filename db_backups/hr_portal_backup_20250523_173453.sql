-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: hr_portal
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add department',7,'add_department'),(26,'Can change department',7,'change_department'),(27,'Can delete department',7,'delete_department'),(28,'Can view department',7,'view_department'),(29,'Can add handbook pdf',8,'add_handbookpdf'),(30,'Can change handbook pdf',8,'change_handbookpdf'),(31,'Can delete handbook pdf',8,'delete_handbookpdf'),(32,'Can view handbook pdf',8,'view_handbookpdf'),(33,'Can add designation',9,'add_designation'),(34,'Can change designation',9,'change_designation'),(35,'Can delete designation',9,'delete_designation'),(36,'Can view designation',9,'view_designation'),(37,'Can add employee bisp',10,'add_employeebisp'),(38,'Can change employee bisp',10,'change_employeebisp'),(39,'Can delete employee bisp',10,'delete_employeebisp'),(40,'Can view employee bisp',10,'view_employeebisp'),(41,'Can add leave type',11,'add_leavetype'),(42,'Can change leave type',11,'change_leavetype'),(43,'Can delete leave type',11,'delete_leavetype'),(44,'Can view leave type',11,'view_leavetype'),(45,'Can add leave',12,'add_leave'),(46,'Can change leave',12,'change_leave'),(47,'Can delete leave',12,'delete_leave'),(48,'Can view leave',12,'view_leave'),(49,'Can add handbook acknowledgement',13,'add_handbookacknowledgement'),(50,'Can change handbook acknowledgement',13,'change_handbookacknowledgement'),(51,'Can delete handbook acknowledgement',13,'delete_handbookacknowledgement'),(52,'Can view handbook acknowledgement',13,'view_handbookacknowledgement'),(53,'Can add project',14,'add_project'),(54,'Can change project',14,'change_project'),(55,'Can delete project',14,'delete_project'),(56,'Can view project',14,'view_project'),(57,'Can add task',15,'add_task'),(58,'Can change task',15,'change_task'),(59,'Can delete task',15,'delete_task'),(60,'Can view task',15,'view_task'),(61,'Can add task record',16,'add_taskrecord'),(62,'Can change task record',16,'change_taskrecord'),(63,'Can delete task record',16,'delete_taskrecord'),(64,'Can view task record',16,'view_taskrecord'),(65,'Can add emp leave type',17,'add_empleavetype'),(66,'Can change emp leave type',17,'change_empleavetype'),(67,'Can delete emp leave type',17,'delete_empleavetype'),(68,'Can view emp leave type',17,'view_empleavetype'),(69,'Can add task record',18,'add_taskrecord'),(70,'Can change task record',18,'change_taskrecord'),(71,'Can delete task record',18,'delete_taskrecord'),(72,'Can view task record',18,'view_taskrecord'),(73,'Can add employee bisp history',19,'add_employeebisphistory'),(74,'Can change employee bisp history',19,'change_employeebisphistory'),(75,'Can delete employee bisp history',19,'delete_employeebisphistory'),(76,'Can view employee bisp history',19,'view_employeebisphistory'),(77,'Can add leave type history',20,'add_leavetypehistory'),(78,'Can change leave type history',20,'change_leavetypehistory'),(79,'Can delete leave type history',20,'delete_leavetypehistory'),(80,'Can view leave type history',20,'view_leavetypehistory'),(81,'Can add message',21,'add_message'),(82,'Can change message',21,'change_message'),(83,'Can delete message',21,'delete_message'),(84,'Can view message',21,'view_message'),(85,'Can add project history',22,'add_projecthistory'),(86,'Can change project history',22,'change_projecthistory'),(87,'Can delete project history',22,'delete_projecthistory'),(88,'Can view project history',22,'view_projecthistory'),(89,'Can add task history',23,'add_taskhistory'),(90,'Can change task history',23,'change_taskhistory'),(91,'Can delete task history',23,'delete_taskhistory'),(92,'Can view task history',23,'view_taskhistory'),(93,'Can add learning video',24,'add_learningvideo'),(94,'Can change learning video',24,'change_learningvideo'),(95,'Can delete learning video',24,'delete_learningvideo'),(96,'Can view learning video',24,'view_learningvideo'),(97,'Can add imagetask record',25,'add_imagetaskrecord'),(98,'Can change imagetask record',25,'change_imagetaskrecord'),(99,'Can delete imagetask record',25,'delete_imagetaskrecord'),(100,'Can view imagetask record',25,'view_imagetaskrecord'),(101,'Can add employee emergency contact',26,'add_employeeemergencycontact'),(102,'Can change employee emergency contact',26,'change_employeeemergencycontact'),(103,'Can delete employee emergency contact',26,'delete_employeeemergencycontact'),(104,'Can view employee emergency contact',26,'view_employeeemergencycontact'),(105,'Can add employee document',27,'add_employeedocument'),(106,'Can change employee document',27,'change_employeedocument'),(107,'Can delete employee document',27,'delete_employeedocument'),(108,'Can view employee document',27,'view_employeedocument'),(109,'Can add employee education',28,'add_employeeeducation'),(110,'Can change employee education',28,'change_employeeeducation'),(111,'Can delete employee education',28,'delete_employeeeducation'),(112,'Can view employee education',28,'view_employeeeducation'),(113,'Can add employee bank details',29,'add_employeebankdetails'),(114,'Can change employee bank details',29,'change_employeebankdetails'),(115,'Can delete employee bank details',29,'delete_employeebankdetails'),(116,'Can view employee bank details',29,'view_employeebankdetails'),(117,'Can add employee experience',30,'add_employeeexperience'),(118,'Can change employee experience',30,'change_employeeexperience'),(119,'Can delete employee experience',30,'delete_employeeexperience'),(120,'Can view employee experience',30,'view_employeeexperience'),(121,'Can add employee personal details',31,'add_employeepersonaldetails'),(122,'Can change employee personal details',31,'change_employeepersonaldetails'),(123,'Can delete employee personal details',31,'delete_employeepersonaldetails'),(124,'Can view employee personal details',31,'view_employeepersonaldetails'),(125,'Can add resignation application',32,'add_resignationapplication'),(126,'Can change resignation application',32,'change_resignationapplication'),(127,'Can delete resignation application',32,'delete_resignationapplication'),(128,'Can view resignation application',32,'view_resignationapplication'),(129,'Can add holiday',33,'add_holiday'),(130,'Can change holiday',33,'change_holiday'),(131,'Can delete holiday',33,'delete_holiday'),(132,'Can view holiday',33,'view_holiday'),(133,'Can add exit email',34,'add_exitemail'),(134,'Can change exit email',34,'change_exitemail'),(135,'Can delete exit email',34,'delete_exitemail'),(136,'Can view exit email',34,'view_exitemail'),(137,'Can add employee checklist',35,'add_employeechecklist'),(138,'Can change employee checklist',35,'change_employeechecklist'),(139,'Can delete employee checklist',35,'delete_employeechecklist'),(140,'Can view employee checklist',35,'view_employeechecklist'),(141,'Can add exit document',36,'add_exitdocument'),(142,'Can change exit document',36,'change_exitdocument'),(143,'Can delete exit document',36,'delete_exitdocument'),(144,'Can view exit document',36,'view_exitdocument');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'','2025-05-23 09:15:49.567096',0,'apurvmalviya@gmail.com','','','apurvmalviya@gmail.com',0,1,'2025-04-09 12:41:58.622959'),(2,'','2025-05-23 09:10:09.086807',0,'yash@gmail.com','','','yash@gmail.com',0,1,'2025-04-09 14:09:25.744547'),(3,'','2025-05-22 11:52:26.704184',0,'nischal@gmail.com','','','nischal@gmail.com',0,1,'2025-04-09 14:21:07.835754'),(4,'','2025-04-17 05:30:25.751108',0,'dev@gmail.com','','','dev@gmail.com',0,1,'2025-04-10 12:48:49.077399'),(5,'','2025-05-21 06:07:51.510834',0,'gaurav@gmail.com','','','gaurav@gmail.com',0,1,'2025-04-17 10:05:20.774716'),(6,'','2025-05-01 06:52:01.891910',0,'devesh@gmail.com','','','devesh@gmail.com',0,1,'2025-04-22 07:36:24.100376'),(7,'','2025-05-05 07:28:26.235944',0,'uday@gmail.com','','','uday@gmail.com',0,1,'2025-05-02 11:45:34.203143'),(8,'','2025-05-22 09:58:52.883351',0,'nikhil12@gmail.com','','','nikhil12@gmail.com',0,1,'2025-05-02 12:14:48.557245'),(9,'','2025-05-02 12:25:46.578110',0,'tavevebum@gmail.com','','','tavevebum@gmail.com',0,1,'2025-05-02 12:25:46.566282'),(10,'','2025-05-03 05:53:17.602674',0,'mohit@gmail.com','','','mohit@gmail.com',0,1,'2025-05-02 12:58:58.349782'),(11,'','2025-05-08 06:46:38.329259',0,'suraj@gmail.com','','','suraj@gmail.com',0,1,'2025-05-07 10:26:58.010623'),(12,'','2025-05-13 10:50:23.512760',0,'sahil@gmail.com','','','sahil@gmail.com',0,1,'2025-05-13 10:46:16.106439'),(13,'','2025-05-14 09:47:27.104037',0,'chandresh@gmail.com','','','chandresh@gmail.com',0,1,'2025-05-14 09:47:27.091147');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatbox_message`
--

DROP TABLE IF EXISTS `chatbox_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatbox_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `project_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Chatbox_message_user_id_ea11d20e_fk_HR_App_employeebisp_id` (`user_id`),
  KEY `Chatbox_message_project_id_120aa466_fk_Project_project_id` (`project_id`),
  CONSTRAINT `Chatbox_message_project_id_120aa466_fk_Project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`),
  CONSTRAINT `Chatbox_message_user_id_ea11d20e_fk_HR_App_employeebisp_id` FOREIGN KEY (`user_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatbox_message`
--

LOCK TABLES `chatbox_message` WRITE;
/*!40000 ALTER TABLE `chatbox_message` DISABLE KEYS */;
INSERT INTO `chatbox_message` VALUES (1,'Ac','2025-04-22 06:51:26.369193',2,NULL),(2,'hello','2025-04-22 06:51:54.139477',2,NULL),(3,'hello','2025-04-22 06:52:23.052817',3,NULL),(4,'hello','2025-04-22 06:58:59.350156',3,NULL),(5,'asc','2025-04-25 09:04:33.664195',1,1),(6,'harekrsna','2025-04-25 09:05:05.278776',1,1),(7,'sa','2025-04-25 09:05:22.103517',2,1),(8,'sscas','2025-04-25 09:13:49.970077',2,1),(9,'a','2025-04-25 09:16:16.927078',2,1),(10,'kn','2025-04-25 09:18:59.857617',2,1),(11,'dvd','2025-04-25 09:20:09.745718',3,2),(12,'sdv','2025-04-25 09:20:13.629515',3,2),(13,'hello','2025-05-22 09:23:15.310508',1,1);
/*!40000 ALTER TABLE `chatbox_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(21,'Chatbox','message'),(5,'contenttypes','contenttype'),(7,'HR_App','department'),(9,'HR_App','designation'),(17,'HR_App','empleavetype'),(29,'HR_App','employeebankdetails'),(10,'HR_App','employeebisp'),(19,'HR_App','employeebisphistory'),(35,'HR_App','employeechecklist'),(27,'HR_App','employeedocument'),(28,'HR_App','employeeeducation'),(26,'HR_App','employeeemergencycontact'),(30,'HR_App','employeeexperience'),(31,'HR_App','employeepersonaldetails'),(36,'HR_App','exitdocument'),(34,'HR_App','exitemail'),(13,'HR_App','handbookacknowledgement'),(8,'HR_App','handbookpdf'),(33,'HR_App','holiday'),(24,'HR_App','learningvideo'),(12,'HR_App','leave'),(11,'HR_App','leavetype'),(20,'HR_App','leavetypehistory'),(32,'HR_App','resignationapplication'),(14,'Project','project'),(22,'Project','projecthistory'),(15,'Project','task'),(23,'Project','taskhistory'),(16,'Project','taskrecord'),(6,'sessions','session'),(25,'Timesheet','imagetaskrecord'),(18,'Timesheet','taskrecord');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'HR_App','0001_initial','2025-04-09 11:58:25.057828'),(2,'contenttypes','0001_initial','2025-04-09 11:58:25.127825'),(3,'auth','0001_initial','2025-04-09 11:58:26.356085'),(4,'admin','0001_initial','2025-04-09 11:58:26.606109'),(5,'admin','0002_logentry_remove_auto_add','2025-04-09 11:58:26.622367'),(6,'admin','0003_logentry_add_action_flag_choices','2025-04-09 11:58:26.637890'),(7,'contenttypes','0002_remove_content_type_name','2025-04-09 11:58:26.844145'),(8,'auth','0002_alter_permission_name_max_length','2025-04-09 11:58:26.971006'),(9,'auth','0003_alter_user_email_max_length','2025-04-09 11:58:27.018089'),(10,'auth','0004_alter_user_username_opts','2025-04-09 11:58:27.034150'),(11,'auth','0005_alter_user_last_login_null','2025-04-09 11:58:27.135830'),(12,'auth','0006_require_contenttypes_0002','2025-04-09 11:58:27.140329'),(13,'auth','0007_alter_validators_add_error_messages','2025-04-09 11:58:27.157213'),(14,'auth','0008_alter_user_username_max_length','2025-04-09 11:58:27.281705'),(15,'auth','0009_alter_user_last_name_max_length','2025-04-09 11:58:27.450176'),(16,'auth','0010_alter_group_name_max_length','2025-04-09 11:58:27.486426'),(17,'auth','0011_update_proxy_permissions','2025-04-09 11:58:27.523528'),(18,'auth','0012_alter_user_first_name_max_length','2025-04-09 11:58:27.678794'),(19,'sessions','0001_initial','2025-04-09 11:58:27.752072'),(20,'HR_App','0002_leave_reject_date_leave_reject_reason','2025-04-09 13:56:57.416491'),(21,'HR_App','0003_alter_leave_status','2025-04-10 11:12:32.339901'),(22,'HR_App','0004_auto_20250410_1533','2025-04-10 10:03:51.030613'),(23,'HR_App','0005_auto_20250410_1534','2025-04-10 10:06:33.192634'),(24,'HR_App','0006_leave_half_day_type_name','2025-04-10 10:06:33.242108'),(25,'Project','0001_initial','2025-04-11 09:43:18.583593'),(26,'Project','0002_alter_task_status','2025-04-12 11:47:25.703302'),(27,'Project','0003_taskrecord','2025-04-14 07:30:27.096619'),(28,'HR_App','0007_remove_employeebisp_availed_leave_and_more','2025-04-14 08:35:11.790750'),(29,'HR_App','0008_remove_leavetype_availed_leave_and_more','2025-04-15 05:53:40.583335'),(30,'Project','0004_delete_taskrecord','2025-04-15 07:59:15.896234'),(31,'Timesheet','0001_initial','2025-04-15 07:59:15.999961'),(32,'HR_App','0009_alter_leave_options_leave_created_at','2025-04-15 11:07:11.399033'),(33,'HR_App','0010_leavetype_effective_after_value','2025-04-17 11:12:18.060841'),(34,'HR_App','0011_alter_employeebisp_aadhar_card_and_more','2025-04-21 08:42:50.135199'),(35,'HR_App','0012_employeebisp_status_employeebisp_timestamp_and_more','2025-04-21 10:18:29.758709'),(36,'HR_App','0013_employeebisphistory','2025-04-21 10:19:32.350171'),(37,'HR_App','0014_leavetype_is_deleted_leavetype_timestamp_and_more','2025-04-21 10:52:50.939606'),(38,'HR_App','0015_alter_leavetype_status','2025-04-21 11:13:21.662142'),(39,'Chatbox','0001_initial','2025-04-22 05:55:50.813259'),(40,'Chatbox','0002_message_project','2025-04-22 07:06:03.109986'),(41,'Project','0005_project_status_project_timestamp_project_version_and_more','2025-04-22 11:27:07.852844'),(42,'Project','0006_task_status_field_taskhistory_status_field_and_more','2025-04-22 12:47:36.103701'),(43,'HR_App','0016_alter_leave_half_day_type_name','2025-04-23 08:48:33.170093'),(44,'HR_App','0017_learningvideo','2025-04-24 07:33:11.339397'),(45,'HR_App','0018_leave_timestamp','2025-04-24 12:22:21.754231'),(46,'HR_App','0019_handbookacknowledgement_timestamp_and_more','2025-04-25 11:04:52.557773'),(47,'Timesheet','0002_imagetaskrecord','2025-04-26 07:16:08.351479'),(48,'Timesheet','0003_remove_imagetaskrecord_task_name_and_more','2025-04-26 07:26:28.028601'),(49,'HR_App','0020_employeebankdetails_employeedocument_and_more','2025-05-01 05:47:53.056335'),(50,'HR_App','0021_rename_phone_number_employeepersonaldetails_tell_number_and_more','2025-05-01 06:16:34.170142'),(51,'HR_App','0022_employeeeducation_priority_and_more','2025-05-02 10:01:53.378314'),(52,'HR_App','0023_employeebisp_reported_to_and_more','2025-05-02 12:37:59.499370'),(53,'HR_App','0024_employeebisphistory_created_at','2025-05-06 11:19:50.670871'),(54,'HR_App','0025_employeebisp_created_at','2025-05-06 12:55:21.730036'),(55,'Project','0007_projecthistory_created_at_taskhistory_created_at','2025-05-07 10:42:14.469178'),(56,'HR_App','0026_resignationapplication','2025-05-13 09:12:36.705802'),(57,'HR_App','0027_employeebisp_employee_ids_and_more','2025-05-13 10:05:44.919870'),(58,'HR_App','0028_holiday','2025-05-15 06:43:05.000816'),(59,'HR_App','0029_exitemail','2025-05-16 06:04:01.659585'),(60,'HR_App','0030_exitemail_employee','2025-05-16 07:50:07.178277'),(61,'HR_App','0031_exitemail_resignation','2025-05-16 09:17:03.442451'),(62,'HR_App','0032_employeechecklist','2025-05-20 07:56:53.996374'),(63,'HR_App','0033_exitdocument','2025-05-20 10:14:02.743354'),(64,'HR_App','0034_resignationapplication_hr_approved_and_more','2025-05-20 12:14:38.094453'),(65,'HR_App','0035_alter_resignationapplication_hr_approved_and_more','2025-05-20 13:16:56.560938'),(66,'HR_App','0036_employeechecklist_timestamp_exitdocument_timestamp_and_more','2025-05-21 07:50:34.678773'),(67,'HR_App','0037_resignationapplication_status','2025-05-21 09:22:14.077785'),(68,'Project','0008_projecthistory_team_members','2025-05-21 12:59:17.276181'),(69,'HR_App','0038_alter_learningvideo_section','2025-05-22 06:24:32.537281');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5e13zqy35j8zqtj34l1vfz92zmw9lqvu','.eJxVkDFvgzAQhf9KxJwQY8CYTE2rSu0QqWqHjNZhX8AJGGSbKGnV_15DMjST5e-9u3t3P5GA0TdidGiFVtEmSqLlf1aBPKGZBHUEU_ex7I23uoonS3xXXbzrFbbPd-9DgwZcE6pTnleyJDQhNDxVkaUJkyA5P3DFGGcMpGQlL5OyyIAryVjFUs4OWDCAgs9NHTqneyPwMmh7jTY0LykhZBlhN7T9FXHeIPn3N9BhGL4dRnte7KA96ytEkw66DRwm3t3wUz3BsF4XDLZv5zrVaaOdt-B7G7BCp2sDPoQI6tvn4vWCcvT6jEF8Ga1F472eR1JC8xXJV3S654ftD7rF9w7qSVt3qDSshxsVg5ZuvW_Au-0wiNkkbuXZinABXlAqjvvafCXfccrirBCYJAyoyuLjUIf-2oCcUggP7iRacF7Y0Tym-P0DfKugsw:1uHg0k:97JEYofpv7Re-1rbDvExxQrNN8FlkQT5rZsOwvAG8TA','2025-06-20 09:45:18.600843'),('9zi2w8950p6q9zrggm5sqrmf4ni421gq','.eJxVj71uwyAURl8l8pw4BjsYZ2paVWqHSFU7ZETXcGOT2hgBjpJWffdiJ0M7Ic757t93ImAMrRg9OqFVsk1IsvzLapCfaCahTmCaIZWDCU7X6RRJ79an-0Fh93jP_mvQgm9jdc43tawySjIan7oscsIkSM6PXDHGGQMpWcUrUpUFcCUZq1nO2RFLBlDyualH7_VgBF6sdtdkSzcVzbJsmWBvu-GKOF9A_vwN9BiH7-zozos9dGd9hWTyoLvIYeL9DT80E4zn9THghm6uU7022gcHYXARK_S6MRDiEtG-vC-eLyjHoM8Y5dPoHJoQ9DySZnSzyjYrkkf15oaj7vC1h2Zy6x6VhrW9UWG19OtDC8HvrBVzSNzKi1XGBQRBqTgdGvNBvtKcpUUpkBAGVBXpyTbJzy9o45Sv:1uEnBD:01SNvhMfv0BXQa-3_KK4o3tM1yAbcum3pJ3_G5DLE0I','2025-06-12 10:48:11.708615'),('aaxmd4c2s7s0pw7zpdbiwc7uhl2katns','.eJxVj8FugzAQRH-l8jlxDARjckrbUyulrdRDjtZiL-AEjGWD1Kjqv9eQSE1Pq503O6P9JhKmsZVTQC-NJjuSkdW9VoE6o52BPoFtBqoGO3pT0dlCbzTQw6Cxe7p5_wW0ENo5VuSVKlmasDSOqthmCVeghKiF5lxwDkrxUpRJWWxBaMV5xTPBayw4QCGW0IAhmMFK_HLGX8guzcuUMbYi2LtuuCAuH2R3u4UeY_mbCaqFjswETBcVe1X2zbzHn_rI_NDN5gNYaNBHQWMwjYUxdkb9EzoMD3_0efIe7TiapSJlab5m-TrhEX34oTYdvvTRGtmmR21g466qdEaFzbGFMTw6JxeTvJ5v47mEUSaFnN5Px7N-pWlJMyYLAJ3UOaMn15CfX0L1jjE:1uFqxz:7JDIa5GZSGLPK_5sDRhPYDHWKFxwfLeT_zR0nj0gVLk','2025-06-15 09:02:55.725475'),('e5zex6omfls6ifes736o7htscyui4g20','.eJxVj81ugzAQhN_F59QxBozJqb-qeqjUW4_WYi_gFLBlQ9So6rvX0KhKT6udb2ZW-0UULHOvlohBWUMOpCS7a60B_YHTCswRps5R7aY52IauFnqhkb46g8P9xfuvoIfYp3Quy0bXjGeMp9FURZ4JDVrKVhohpBCgtahlndVVAdJoIRqRS9FiJQAquZVGjNG6SeGnt-FMDrysOWNsR3D0gzsjbh-UV_sEI6bjz7AEOJEVgB2S0G3Cbbeu6aMxoeCG1fp0iSbFYLTdBHM6mcAjnnBwHkMiD0sIOM2z3do54-UNK26yKqG34Fo74MsI3cr2IxoLe_-rKm913L_3MMc779VmUn9xoWBWWUVzRjOuilybllcNPfqOfP8AM2iJ1g:1u5Nen:TNE6NaVphiOIpn-PvmsQRW1unlyRvTlGxQwh9HEXaPQ','2025-05-17 11:43:49.538561'),('fg6k7571tdgdc4qs6ba69trbi6b73ucs','.eJxVj09vgjAYh7-K4awIBUrxNLcs2Q4my3bw2Ly0r1CFlrTF6JZ99xX0ME9Nn-f3_vuJOIy-5aNDy5WMNlEaLf-zGsQJ9STkEXRjYmG0t6qOp0h8ty7eGYnd8z370KAF14bqjBW1qBKSJiQ8dZlnKRUgGDswSSmjFISgFavSqsyBSUFpTTNGD1hSgJLNTR06p4zmeBmUvUYbUlQkSZJlhP3QmSvifEH676-hxzB8O4z2vNhBd1ZXiCYPqgscJt7f8FMzwXBeHwLWdHOd7JVWzlvwxgYs0alGgw9LBPv2uXi9oBi9OmOQL6O1qL1X80iSkGKVFCuSBfVhzUF1-N5DM7l1j1LBerhRPijh1vsWvNsOA59D_FaerxLGwXNC-HHf6K_0O85onJcc05QCkXl8HJrQX2kQ0xbcgzvxDpzndtSPW_z-AX3DoLc:1uIOVJ:HReKcY05CKELi2HQ0nWpqXSHRD8j-_uwKqWB2adSIyw','2025-06-22 09:15:49.797568'),('g5ci8exoy721a8ep99ijwzd81qqlyysg','e30:1u4Ff6:mxeK5DYv67DOCc14Qacb2CI6e0UrKLP9ZBcdRPsbZVc','2025-05-14 08:59:28.877538'),('hihwebsyuwce53046w2n11my256261kw','.eJxVj09vgjAYh7-K4axYCpTiaW5Zsh1Mlu3gsXlpX6EKhbTF6JZ99xX0ME9Nn-f3_vuJBIy-EaNDK7SKNlESLf-zCuQJzSTUEUzdx7I33uoqniLx3bp41ytsn-_ZhwYNuCZUpzyvZEloQmh4qiJLEyZBcn7gijHOGEjJSl4mZZEBV5KxiqWcHbBgAAWfmzp0TvdG4GXQ9hptaF5SQsgywm5o-yvifEHy72-gwzB8O4z2vNhBe9ZXiCYPug0cJt7d8FM9wXBeFwK2b-c61WmjnbfgexuwQqdrAz4sEezb5-L1gnL0-oxBvozWovFezyMpofmK5CtKg_qw_UG3-N5BPbl1h0rDerhRMWjp1vsGvNsOg5hD4laerQgX4AWl4rivzVfyHacszgqBScKAqiw-DnXorw3IaQvhwZ1EC84LO5rHLX7_AH03oLU:1uI3nU:YbDeZCIwFZkkvLKqeiq8AnFTHqyGaHWiaIo380W3p3E','2025-06-21 11:09:12.185167'),('jnkak2g5vk8nldfpywxjaqucziaqc4bt','.eJxVj8FuwyAMhl-lyrlNCUkJ6WndNGk7VJq2Q4_IATehSyACUrWb9u4jaQ-bhIT4vt82_k4EjKEVo0cntEq2SZYs_7Ia5CeaSagTmMam0prgdJ1OkfRufbq3CrvHe_ZfgxZ8G6tzvqllRWhGaLzqssgzJkFyfuSKMc4YSMkqXmVVWQBXkrGa5ZwdsWQAJZ-bevReWyPwMmh3TbZ0U1FCyDLBfujsFXHeIPvzNtBjHL4bRnde7KE76yskkwfdRQ4T72_4oZlgXK-PAWe7uU712mgfHATrIlbodWMgxE9E-_K-eL6gHIM-Y5RPo3NoQtDzSEroZkXiyaN6c_aoO3ztoZncukelYT3cqBi09OtDC8HvhkHMIXErL1aECwiCUnE6NOYj-0pzlhalwCxjQFWRnoYm-fkFaH-Urg:1uB64o:Cj2Gj8V9HNPCrw9ofDUmI5-6z9ukpGsetegDmBNZQag','2025-06-02 06:10:18.182117'),('mdkf024qt6jdp46oopfo997mhw6jnwdn','.eJxVj8FqwzAQRH-l6JwoshzLck5pe2ohbaGHHMVaWttKbNlINjSU_ntlJ9AUBMvOG82w30TBNDZqCuiVNWRHUrK610rQZ3QzMCdwdU9170ZvSzpb6I0GeugNtk8377-ABkIzx8qs1AXjCeNxlPk2TYQGLWUljRBSCNBaFLJIinwL0mghSpFKUWEuAHK5hAYMwfZO4ddg_YXseFZwxtiKYDe0_QVxuSC92x10GMvfbNANtGQmYNuouKuyr-c93tRF5vt2Nh_AQY0-CgaDrR2MsTPqn9BiePijz5P36MbRLhWc8WzN4ksi-vB9ZVt86aI1sk2HxsJmuKpqsDpsjg2M4XEY1GJS1-_bdSIUjCrJ1fR-Op7NK-UFTZnKAUxSZYyehpr8_AJAoo4r:1uAQSK:FNOhIBOwFnxBDnbanEVhacHgfJBLFZmxW9-20M8nQFg','2025-05-31 09:43:48.551660'),('pnmkmm5f5dy0q31azo77g8z7vk5v0l7v','.eJxVj09vgjAYh7-K4axYCpTiaW5Zsh1Mlu3gsXlpX6EKhbTF6JZ99xX0ME9Nn-f3_vuJBIy-EaNDK7SKNlESLf-zCuQJzSTUEUzdx7I33uoqniLx3bp41ytsn-_ZhwYNuCZUpzyvZEloQmh4qiJLEyZBcn7gijHOGEjJSl4mZZEBV5KxiqWcHbBgAAWfmzp0TvdG4GXQ9hptaF5SQsgywm5o-yvifEHy72-gwzB8O4z2vNhBe9ZXiCYPug0cJt7d8FM9wXBeFwK2b-c61WmjnbfgexuwQqdrAz4sEezb5-L1gnL0-oxBvozWovFezyMpofmK5CtKg_qw_UG3-N5BPbl1h0rDerhRMWjp1vsGvNsOg5hD4laerQgX4AWl4rivzVfyHacszgqBScKAqiw-DnXorw3IaQvhwZ1EC84LO5rHLX7_AH03oLU:1uI2dU:7eKqRBJlY2k_kq3ZSuMJSldmTP-nC6HVy-mV-VR1J2Y','2025-06-21 09:54:48.270175'),('sdb7knixpkvpmg60c0937khm8lppp7we','.eJxVj8FuwjAQRP_FZwiOExyHU6GnqqKtKlU9Wht7SUwTJ7INKqr673UCqHCy9s14ZveHSDiERh48Omk0WZGMzG5ZBeoL7SjoPdi6T1RvgzNVMlqSi-qTba-x3Vy8dwEN-GaMFctKlZSllMWnKvIs5QqUEDuhORecg1K8FGVaFjkIrTiveCb4DgsOUIgp1KP3prcSvwfjTmTFliWjlM4IdkPbnxCnC7Kb2UKHsfzFeNVAS0YFTBuJPZOHepzjTV3UXN-O5i1YqNFFoNGb2kKInXc89AFa2SIcoz9lMwLHmIL6imgSd3Jjlf13jezx4BzaEMy0FaNsOaf5PE1j5pvrdzHjqYsdUVt0qA0shjOVg1F-8dlA8OthkJNJXr9TISFIxmT98b5-3TwnGU_yQmKacmA6T_ZDTX7_AFnfndw:1u38cl:xnQBlwo_y1O4kF4_KdkVRBZC62EanISyKpIA3mVFz4Q','2025-05-11 07:16:27.353340');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_department`
--

DROP TABLE IF EXISTS `hr_app_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_department`
--

LOCK TABLES `hr_app_department` WRITE;
/*!40000 ALTER TABLE `hr_app_department` DISABLE KEYS */;
INSERT INTO `hr_app_department` VALUES (1,'HR'),(2,'IT'),(3,'Marketing'),(4,'Sales');
/*!40000 ALTER TABLE `hr_app_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_designation`
--

DROP TABLE IF EXISTS `hr_app_designation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_designation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `HR_App_designation_department_id_f6cc3ec5_fk_HR_App_de` (`department_id`),
  CONSTRAINT `HR_App_designation_department_id_f6cc3ec5_fk_HR_App_de` FOREIGN KEY (`department_id`) REFERENCES `hr_app_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_designation`
--

LOCK TABLES `hr_app_designation` WRITE;
/*!40000 ALTER TABLE `hr_app_designation` DISABLE KEYS */;
INSERT INTO `hr_app_designation` VALUES (1,'HR Executive',1),(2,'SD',2),(3,'Developer',2),(4,'Sales Manager',4),(38,'Web Developer',2),(40,'Full Stack Developer',2),(41,'IT Support Specialist',2),(42,'Marketing Manager',3),(43,'SEO Specialist',3),(44,'Sales Coordinator',4),(45,'Talent Acquisition Executive',1);
/*!40000 ALTER TABLE `hr_app_designation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_empleavetype`
--

DROP TABLE IF EXISTS `hr_app_empleavetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_empleavetype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_leave` int NOT NULL,
  `remaining_leave` double NOT NULL,
  `availed_leave` double NOT NULL,
  `employee_id` bigint NOT NULL,
  `leave_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HR_App_empleavetype_employee_id_leave_type_id_2115b2a4_uniq` (`employee_id`,`leave_type_id`),
  KEY `HR_App_empleavetype_leave_type_id_9c6620bf_fk_HR_App_le` (`leave_type_id`),
  CONSTRAINT `HR_App_empleavetype_employee_id_9eb38ad2_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_empleavetype_leave_type_id_9c6620bf_fk_HR_App_le` FOREIGN KEY (`leave_type_id`) REFERENCES `hr_app_leavetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_empleavetype`
--

LOCK TABLES `hr_app_empleavetype` WRITE;
/*!40000 ALTER TABLE `hr_app_empleavetype` DISABLE KEYS */;
INSERT INTO `hr_app_empleavetype` VALUES (1,13,11,2,1,21),(6,14,7,7,1,23),(7,14,14,0,2,23),(8,14,14,0,3,23),(10,12,12,0,3,25),(18,15,15,0,5,26),(25,1,1,0,1,27),(26,1,1,0,2,27),(27,1,1,0,3,27),(29,1,1,0,5,27),(36,15,15,0,1,29),(37,12,12,0,5,30),(49,1,1,0,6,27),(50,17,17,0,1,22),(51,17,17,0,2,22),(52,17,17,0,3,22),(53,17,17,0,5,22),(54,17,17,0,6,22),(55,13,13,0,1,34),(56,13,13,0,2,34),(57,13,13,0,3,34),(58,13,13,0,5,34),(59,13,13,0,6,34),(60,18,18,0,1,35),(61,18,18,0,2,35),(62,18,18,0,3,35),(63,18,18,0,5,35),(64,18,18,0,6,35),(65,18,18,0,1,38),(66,18,18,0,2,38),(67,18,18,0,3,38),(68,18,18,0,5,38),(69,18,18,0,6,38),(70,18,18,0,9,38),(71,18,18,0,11,38),(72,18,18,0,12,38),(73,15,15,0,1,39),(74,15,15,0,2,39),(75,15,15,0,3,39),(76,15,15,0,5,39),(77,15,15,0,6,39),(78,15,15,0,9,39),(79,15,15,0,11,39),(80,15,15,0,12,39),(81,15,15,0,13,39),(82,18,18,0,9,35),(83,18,18,0,11,35),(84,18,18,0,12,35),(85,18,18,0,13,35),(86,13,13,0,9,34),(87,13,13,0,11,34),(88,13,13,0,12,34),(89,13,13,0,13,34),(90,13,13,0,62,34),(91,13,13,0,63,34);
/*!40000 ALTER TABLE `hr_app_empleavetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeebankdetails`
--

DROP TABLE IF EXISTS `hr_app_employeebankdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeebankdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(100) NOT NULL,
  `bank_account_no` varchar(50) NOT NULL,
  `ifsc_code` varchar(20) NOT NULL,
  `pan_no` varchar(20) NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  CONSTRAINT `HR_App_employeebankd_employee_id_af4209d3_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeebankdetails`
--

LOCK TABLES `hr_app_employeebankdetails` WRITE;
/*!40000 ALTER TABLE `hr_app_employeebankdetails` DISABLE KEYS */;
INSERT INTO `hr_app_employeebankdetails` VALUES (1,'Axis','90988878767655','UIB00100IN','GJVPM2532K',1);
/*!40000 ALTER TABLE `hr_app_employeebankdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeebisp`
--

DROP TABLE IF EXISTS `hr_app_employeebisp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeebisp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  `permanent_address` varchar(200) DEFAULT NULL,
  `current_address` varchar(200) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  `aadhar_card` varchar(200) DEFAULT NULL,
  `date_of_join` varchar(200) DEFAULT NULL,
  `work_location` varchar(200) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `department_id` bigint DEFAULT NULL,
  `designation_id` bigint DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `version` int NOT NULL,
  `reported_to_id` bigint DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `employee_IDs` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_IDs` (`employee_IDs`),
  KEY `HR_App_employeebisp_department_id_62fe5893_fk_HR_App_de` (`department_id`),
  KEY `HR_App_employeebisp_designation_id_45f0c292_fk_HR_App_de` (`designation_id`),
  KEY `HR_App_employeebisp_reported_to_id_86562d44_fk_HR_App_em` (`reported_to_id`),
  CONSTRAINT `HR_App_employeebisp_department_id_62fe5893_fk_HR_App_de` FOREIGN KEY (`department_id`) REFERENCES `hr_app_department` (`id`),
  CONSTRAINT `HR_App_employeebisp_designation_id_45f0c292_fk_HR_App_de` FOREIGN KEY (`designation_id`) REFERENCES `hr_app_designation` (`id`),
  CONSTRAINT `HR_App_employeebisp_reported_to_id_86562d44_fk_HR_App_em` FOREIGN KEY (`reported_to_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeebisp`
--

LOCK TABLES `hr_app_employeebisp` WRITE;
/*!40000 ALTER TABLE `hr_app_employeebisp` DISABLE KEYS */;
INSERT INTO `hr_app_employeebisp` VALUES (1,'Apurv Malviya','2002-10-27','Male','Indian','patel nagar','Indore','7000243390','apurvmalviya@gmail.com','pbkdf2_sha256$1000000$W9RlRAj5qNrSvzandfBPIV$sTYCwiXgqkJwC+jfQcROBUmD8hK4l2IQucpftMObILs=','123234321232','2025-03-03','Bhopal','Administrator','profile_pics/WhatsApp_Image_2025-04-08_at_22_jWgnS1z.36.47_e116a2d4.jpg',1,1,'active','2025-05-06 11:29:30.328128',16,NULL,'2025-05-06 12:55:21.235124',NULL),(2,'Yash Anant Malviya','2005-12-12','Male','Indian','','New Market Bhopal','8839268380','yash@gmail.com','pbkdf2_sha256$1000000$v9ExF5tAl8wA4gvEKxlrVl$hWdWMyU5yxb3oVHBM0KNlc5PljL6cuCzynoRpOsIlVQ=','','2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_QcLW8YS.35.41_be8a2c01.jpg',2,3,'active','2025-05-22 09:37:16.289735',22,3,'2025-05-22 09:37:16.289741',NULL),(3,'Nischal Katara','2000-10-27','Male','Indian','','bhopal','9098787656','nischal@gmail.com','pbkdf2_sha256$1000000$ON4O3m0WDFMbCrBRTIyhVM$RUBf2tlV3MfguD2VlIXGVaJijN0D9mewyaVj8wk0WBU=','','2025-03-03','Bhopal','Manager','profile_pics/WhatsApp_Image_2025-04-16_at_17_uOjWkdJ.29.30_7aad1f50.jpg',4,4,'active','2025-05-22 09:39:44.471301',5,3,'2025-05-22 09:39:44.471304',NULL),(5,'Gaurav Singh Bhandari','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',3,43,'active','2025-05-21 09:42:26.258856',14,NULL,'2025-05-21 09:42:26.258867',NULL),(6,'Devesh','2005-09-01','male','Indian','patel nagar','bhopal','3333323243','devesh@gmail.com','pbkdf2_sha256$1000000$JyDhQaJntLzfhNaJAb7o0m$KCzJO5b5RDo/9aRpGhT1D2jIj5CAaW8ums1oJgMBtYU=','343234343212','2025-03-03','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-18_at_14.07.09_8930556b.jpg',2,3,'deleted','2025-04-21 10:29:28.911846',2,NULL,'2025-05-06 12:55:21.235124',NULL),(9,'Uday','2002-10-27','Male','Indian','','bhopal 462003','8909876777','uday@gmail.com','pbkdf2_sha256$1000000$7xNAp3TEMhWBWHCaTixxDQ$lT2iUN+eTM8kFxal744JvrSXP6kdAwRHkv3csRLqABY=','','2025-05-02','Bhopal','Employee','',2,40,'deleted','2025-05-06 09:22:58.603505',5,3,'2025-05-06 12:55:21.235124',NULL),(11,'nikhil','2005-10-29','Male','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-18_at_14_UwOU4Xa.07.09_8930556b.jpg',3,43,'active','2025-05-22 09:59:20.890960',20,3,'2025-05-22 09:59:20.890967',NULL),(12,'Imogene Gibbs',NULL,NULL,'',NULL,'Sit nemo aperiam pla',NULL,'tavevebum@gmail.com','pbkdf2_sha256$1000000$cbZUzNTkF3CQNBBexr9QhJ$Q2OGXyNtM2UIReFAau5Ye3CKNdW7m5FNrYoS36RhJnk=',NULL,'2025-04-17','Do ut ut explicabo','Employee','',3,42,'deleted','2025-05-02 12:59:53.446687',2,NULL,'2025-05-06 12:55:21.235124',NULL),(13,'Mohit',NULL,NULL,'Indian',NULL,'Banglore',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',2,41,'deleted','2025-05-14 12:29:16.065823',8,3,'2025-05-14 12:29:16.065828',NULL),(62,'Chandresh',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'chandresh@gmail.com','pbkdf2_sha256$1000000$SRhIOaz5VfJolFXNP9D16J$4N5EDWmaro8C1baz5KJtdL0vORXecUM7Ntkn8pdKzgc=',NULL,'2025-05-13','Bhopal','Employee','',2,2,'active','2025-05-13 10:09:23.658916',1,3,'2025-05-13 10:09:23.658962',NULL),(63,'Sahil',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'sahil@gmail.com','pbkdf2_sha256$1000000$lYPWx6ZXceNVPoeT3D7md3$QDhvhVUA2/qg9Md5acXiNc8WPzyEN5fvIvHrNUMbKKI=',NULL,'2025-05-13','Bhopal','Employee','',4,44,'deleted','2025-05-14 05:36:54.555885',2,3,'2025-05-14 05:36:54.555890','EMP002025001'),(64,'Devrag',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'devrag112@gmail.com','pbkdf2_sha256$1000000$GmiiGzKeMkRScGThr63rUt$E8Eaels85XB6iMzKaZ+Y73/Hw5oEgTqezj+d7vTVDl0=',NULL,'2025-05-23','Bhopal','Employee','',2,2,'active','2025-05-23 09:16:12.215144',2,3,'2025-05-23 09:16:12.215156','EMP002025002');
/*!40000 ALTER TABLE `hr_app_employeebisp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeebisphistory`
--

DROP TABLE IF EXISTS `hr_app_employeebisphistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeebisphistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  `permanent_address` varchar(200) DEFAULT NULL,
  `current_address` varchar(200) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  `aadhar_card` varchar(200) DEFAULT NULL,
  `date_of_join` varchar(200) DEFAULT NULL,
  `work_location` varchar(200) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `version` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `department_id` bigint DEFAULT NULL,
  `designation_id` bigint DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  `reported_to_id` bigint DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `employee_IDs` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_employeebisph_department_id_536f3195_fk_HR_App_de` (`department_id`),
  KEY `HR_App_employeebisph_designation_id_297b8b0f_fk_HR_App_de` (`designation_id`),
  KEY `HR_App_employeebisph_employee_id_f2487ae3_fk_HR_App_em` (`employee_id`),
  KEY `HR_App_employeebisph_reported_to_id_5382c38b_fk_HR_App_em` (`reported_to_id`),
  CONSTRAINT `HR_App_employeebisph_department_id_536f3195_fk_HR_App_de` FOREIGN KEY (`department_id`) REFERENCES `hr_app_department` (`id`),
  CONSTRAINT `HR_App_employeebisph_designation_id_297b8b0f_fk_HR_App_de` FOREIGN KEY (`designation_id`) REFERENCES `hr_app_designation` (`id`),
  CONSTRAINT `HR_App_employeebisph_employee_id_f2487ae3_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_employeebisph_reported_to_id_5382c38b_fk_HR_App_em` FOREIGN KEY (`reported_to_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeebisphistory`
--

LOCK TABLES `hr_app_employeebisphistory` WRITE;
/*!40000 ALTER TABLE `hr_app_employeebisphistory` DISABLE KEYS */;
INSERT INTO `hr_app_employeebisphistory` VALUES (49,'Mohit',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',1,'2025-05-06 11:56:19.979409',2,41,13,3,'2025-05-02 12:55:52.704748',NULL),(50,'nikhil','2002-10-27','Female','Indian',NULL,'Pune','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',4,'2025-05-06 11:58:24.445532',4,44,11,NULL,'2025-05-06 11:20:48.501511',NULL),(51,'Mohit',NULL,NULL,'Indian',NULL,'Nagpur',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',2,'2025-05-06 12:02:25.019655',2,41,13,3,'2025-05-06 11:56:20.072865',NULL),(52,'nikhil','2002-10-27','Female','Indian',NULL,'dehli','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',5,'2025-05-06 12:15:54.935044',4,44,11,NULL,'2025-05-06 11:58:24.461118',NULL),(53,'nikhil','2002-10-27','Female','Indian',NULL,'Pune','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',7,'2025-05-06 12:47:32.040675',4,44,11,NULL,'2025-05-06 12:42:51.728150',NULL),(54,'nikhil','2002-10-27','Female','Indian',NULL,'Pune','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',9,'2025-05-06 12:48:08.846920',4,44,11,NULL,'2025-05-06 12:47:46.648362',NULL),(55,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',10,'2025-05-06 12:48:26.613793',4,44,11,NULL,'2025-05-06 12:48:08.951380',NULL),(56,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',12,'2025-05-06 12:57:24.381158',4,44,11,NULL,'2025-05-06 12:52:44.255730',NULL),(57,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',14,'2025-05-06 13:03:37.077281',4,44,11,NULL,'2025-05-06 12:57:31.464050',NULL),(58,'Mohit',NULL,NULL,'Indian',NULL,'Banglore',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',3,'2025-05-07 07:27:13.854839',2,41,13,3,'2025-05-06 12:02:25.037910',NULL),(59,'Mohit',NULL,NULL,'Indian',NULL,'Banglore',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',5,'2025-05-07 07:29:57.151665',2,41,13,3,'2025-05-07 07:29:03.114501',NULL),(69,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',16,'2025-05-12 08:43:31.244981',4,44,11,NULL,'2025-05-06 13:03:42.336629',NULL),(70,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',17,'2025-05-12 08:44:49.739146',2,41,11,NULL,'2025-05-12 08:43:31.388711',NULL),(71,'Gaurav','','male','Indian','','bhopal Patel Nagar','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',3,'2025-05-13 10:07:54.643791',3,43,5,NULL,'2025-05-06 11:31:29.537890',NULL),(72,'Sahil',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'sahil@gmail.com','pbkdf2_sha256$1000000$lYPWx6ZXceNVPoeT3D7md3$QDhvhVUA2/qg9Md5acXiNc8WPzyEN5fvIvHrNUMbKKI=',NULL,'2025-05-13','Bhopal','Employee','',1,'2025-05-14 05:36:54.534525',4,44,63,3,'2025-05-13 10:44:44.092845',NULL),(73,'Gaurav','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',4,'2025-05-14 05:37:35.028043',3,43,5,NULL,'2025-05-13 10:07:54.705450',NULL),(74,'Mohit',NULL,NULL,'Indian',NULL,'Banglore',NULL,'mohit@gmail.com','pbkdf2_sha256$1000000$LbQwgYI0BcmRLD4ObulmsZ$SQMSDTi0mPGch/oDfg2LujyHnW11oVpICDeV1qYZa6A=',NULL,'2025-05-02','Bhopal','Employee','',7,'2025-05-14 12:29:16.051123',2,41,13,3,'2025-05-14 12:26:46.532504',NULL),(75,'Gaurav','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',6,'2025-05-16 12:16:43.402054',3,43,5,NULL,'2025-05-14 05:38:34.303790',NULL),(76,'Gaurav','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',6,'2025-05-16 12:17:08.677772',3,43,5,NULL,'2025-05-14 05:38:34.303790',NULL),(77,'Gaurav','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',6,'2025-05-16 12:17:17.528677',3,43,5,NULL,'2025-05-14 05:38:34.303790',NULL),(78,'Nischal','2000-10-27','Male','Indian','','bhopal','9098787656','nischal@gmail.com','pbkdf2_sha256$1000000$ON4O3m0WDFMbCrBRTIyhVM$RUBf2tlV3MfguD2VlIXGVaJijN0D9mewyaVj8wk0WBU=','','2025-03-03','Bhopal','Manager','profile_pics/WhatsApp_Image_2025-04-16_at_17_uOjWkdJ.29.30_7aad1f50.jpg',3,'2025-05-20 12:32:38.850050',4,4,3,NULL,'2025-05-02 09:21:33.331689',NULL),(79,'Nischal','2000-10-27','Male','Indian','','bhopal','9098787656','nischal@gmail.com','pbkdf2_sha256$1000000$ON4O3m0WDFMbCrBRTIyhVM$RUBf2tlV3MfguD2VlIXGVaJijN0D9mewyaVj8wk0WBU=','','2025-03-03','Bhopal','Manager','profile_pics/WhatsApp_Image_2025-04-16_at_17_uOjWkdJ.29.30_7aad1f50.jpg',3,'2025-05-20 12:32:52.120578',4,4,3,NULL,'2025-05-02 09:21:33.331689',NULL),(80,'Gaurav Singh Bhandari','','male','Indian','','Pune','','gaurav@gmail.com','pbkdf2_sha256$1000000$VwwSclmubKVM68fqYaiOJB$+sXKPpbl0WL2COt9Dvg0o6FFdDwJeVfSgEC5icICQrM=','','2025-05-01','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17.30.12_43cdf27b.jpg',7,'2025-05-20 12:33:19.939213',3,43,5,NULL,'2025-05-16 12:17:17.548434',NULL),(81,'nikhil','2002-10-27','Female','Indian',NULL,'Bhopal','7000540092','nikhil12@gmail.com','pbkdf2_sha256$1000000$oR9pF3jPG2f0CNDPvjlTIg$sNdp+gqiP9WQEYpG+H7lvdItUCXYmzidEWEbWHT+7cM=',NULL,'2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_wi1yiGs.35.41_be8a2c01.jpg',18,'2025-05-20 12:33:40.783113',3,43,11,NULL,'2025-05-12 08:44:49.753066',NULL),(82,'Yash Malviya','2005-12-12','Male','Indian','','New Market Bhopal','8839268380','yash@gmail.com','pbkdf2_sha256$1000000$v9ExF5tAl8wA4gvEKxlrVl$hWdWMyU5yxb3oVHBM0KNlc5PljL6cuCzynoRpOsIlVQ=','','2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_QcLW8YS.35.41_be8a2c01.jpg',15,'2025-05-21 09:43:31.441242',2,3,2,3,'2025-05-21 09:32:52.573019',NULL),(83,'Yash Malviya','2005-12-12','Male','Indian','','New Market Bhopal','8839268380','yash@gmail.com','pbkdf2_sha256$1000000$v9ExF5tAl8wA4gvEKxlrVl$hWdWMyU5yxb3oVHBM0KNlc5PljL6cuCzynoRpOsIlVQ=','','2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_QcLW8YS.35.41_be8a2c01.jpg',19,'2025-05-22 09:34:05.404368',2,3,2,3,'2025-05-21 09:47:44.529465',NULL),(84,'Yash Malviya','2005-12-12','Male','Indian','','New Market Bhopal','8839268380','yash@gmail.com','pbkdf2_sha256$1000000$v9ExF5tAl8wA4gvEKxlrVl$hWdWMyU5yxb3oVHBM0KNlc5PljL6cuCzynoRpOsIlVQ=','','2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_QcLW8YS.35.41_be8a2c01.jpg',19,'2025-05-22 09:34:16.972528',2,3,2,3,'2025-05-21 09:47:44.529465',NULL),(85,'Yash Anant Malviya','2005-12-12','Male','Indian','','New Market Bhopal','8839268380','yash@gmail.com','pbkdf2_sha256$1000000$v9ExF5tAl8wA4gvEKxlrVl$hWdWMyU5yxb3oVHBM0KNlc5PljL6cuCzynoRpOsIlVQ=','','2025-04-02','Bhopal','Employee','profile_pics/WhatsApp_Image_2025-04-16_at_17_QcLW8YS.35.41_be8a2c01.jpg',20,'2025-05-22 09:35:42.320381',2,3,2,3,'2025-05-22 09:34:16.984818',NULL),(86,'Nischal','2000-10-27','Male','Indian','','bhopal','9098787656','nischal@gmail.com','pbkdf2_sha256$1000000$ON4O3m0WDFMbCrBRTIyhVM$RUBf2tlV3MfguD2VlIXGVaJijN0D9mewyaVj8wk0WBU=','','2025-03-03','Bhopal','Manager','profile_pics/WhatsApp_Image_2025-04-16_at_17_uOjWkdJ.29.30_7aad1f50.jpg',4,'2025-05-22 09:39:44.463203',4,4,3,3,'2025-05-20 12:32:52.140122',NULL),(87,'Devrag',NULL,NULL,'Indian',NULL,'bhopal 462003',NULL,'devrag@gmail.com','pbkdf2_sha256$1000000$GmiiGzKeMkRScGThr63rUt$E8Eaels85XB6iMzKaZ+Y73/Hw5oEgTqezj+d7vTVDl0=',NULL,'2025-05-23','Bhopal','Employee','',1,'2025-05-23 09:16:12.103978',2,2,64,3,'2025-05-23 09:01:21.467380','EMP002025002');
/*!40000 ALTER TABLE `hr_app_employeebisphistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeechecklist`
--

DROP TABLE IF EXISTS `hr_app_employeechecklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeechecklist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `kt_tools_workflows` tinyint(1) NOT NULL,
  `kt_project_status` tinyint(1) NOT NULL,
  `kt_outstanding_tasks` tinyint(1) NOT NULL,
  `kt_contacts_relationships` tinyint(1) NOT NULL,
  `it_change_passwords` tinyint(1) NOT NULL,
  `it_revoke_access` tinyint(1) NOT NULL,
  `it_remove_from_payroll` tinyint(1) NOT NULL,
  `it_update_org_tree` tinyint(1) NOT NULL,
  `pw_resignation_letter` tinyint(1) NOT NULL,
  `pw_last_paycheck` tinyint(1) NOT NULL,
  `pw_nda_signed` tinyint(1) NOT NULL,
  `ra_laptop_charger` tinyint(1) NOT NULL,
  `ra_mouse` tinyint(1) NOT NULL,
  `ei_conduct_interview` tinyint(1) NOT NULL,
  `ad_send_announcement` tinyint(1) NOT NULL,
  `ad_host_farewell` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `resignation_id` bigint DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_employeecheck_employee_id_8b984b6f_fk_HR_App_em` (`employee_id`),
  KEY `HR_App_employeecheck_resignation_id_b0596263_fk_HR_App_re` (`resignation_id`),
  CONSTRAINT `HR_App_employeecheck_employee_id_8b984b6f_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_employeecheck_resignation_id_b0596263_fk_HR_App_re` FOREIGN KEY (`resignation_id`) REFERENCES `hr_app_resignationapplication` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeechecklist`
--

LOCK TABLES `hr_app_employeechecklist` WRITE;
/*!40000 ALTER TABLE `hr_app_employeechecklist` DISABLE KEYS */;
/*!40000 ALTER TABLE `hr_app_employeechecklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeedocument`
--

DROP TABLE IF EXISTS `hr_app_employeedocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeedocument` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `file` varchar(100) NOT NULL,
  `uploaded_at` date NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_employeedocum_employee_id_0aa432aa_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `HR_App_employeedocum_employee_id_0aa432aa_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeedocument`
--

LOCK TABLES `hr_app_employeedocument` WRITE;
/*!40000 ALTER TABLE `hr_app_employeedocument` DISABLE KEYS */;
INSERT INTO `hr_app_employeedocument` VALUES (1,'1000176690.pdf','documents/1000176690.pdf','2025-05-02',1),(11,'pdf-sample (1).pdf','documents/pdf-sample_1.pdf','2025-05-09',1);
/*!40000 ALTER TABLE `hr_app_employeedocument` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeeeducation`
--

DROP TABLE IF EXISTS `hr_app_employeeeducation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeeeducation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `institution_name` varchar(200) NOT NULL,
  `branch` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `employee_id` bigint NOT NULL,
  `priority` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_employeeeduca_employee_id_02877904_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `HR_App_employeeeduca_employee_id_02877904_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeeeducation`
--

LOCK TABLES `hr_app_employeeeducation` WRITE;
/*!40000 ALTER TABLE `hr_app_employeeeducation` DISABLE KEYS */;
INSERT INTO `hr_app_employeeeducation` VALUES (2,'Lnct','IT','2020-10-27','2024-10-27',1,NULL);
/*!40000 ALTER TABLE `hr_app_employeeeducation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeeemergencycontact`
--

DROP TABLE IF EXISTS `hr_app_employeeemergencycontact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeeemergencycontact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `relationship` varchar(50) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `priority` int NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HR_App_employeeemergency_employee_id_priority_c2dba613_uniq` (`employee_id`,`priority`),
  CONSTRAINT `HR_App_employeeemerg_employee_id_64541bcb_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeeemergencycontact`
--

LOCK TABLES `hr_app_employeeemergencycontact` WRITE;
/*!40000 ALTER TABLE `hr_app_employeeemergencycontact` DISABLE KEYS */;
INSERT INTO `hr_app_employeeemergencycontact` VALUES (1,'Nischal','Brother','8987676545',1,1),(2,'Yash','Brother','8789878978',2,1);
/*!40000 ALTER TABLE `hr_app_employeeemergencycontact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeeexperience`
--

DROP TABLE IF EXISTS `hr_app_employeeexperience`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeeexperience` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) NOT NULL,
  `position` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `employee_id` bigint NOT NULL,
  `priority` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_employeeexper_employee_id_7f0a7862_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `HR_App_employeeexper_employee_id_7f0a7862_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeeexperience`
--

LOCK TABLES `hr_app_employeeexperience` WRITE;
/*!40000 ALTER TABLE `hr_app_employeeexperience` DISABLE KEYS */;
INSERT INTO `hr_app_employeeexperience` VALUES (10,'NJ','SD','2025-04-04','2025-05-02',13,1),(11,'fads','aadf','2025-04-10','2025-05-01',13,2),(54,'BISP','SD','2025-05-02','2025-05-04',1,1),(55,'TCS','wf','2025-05-02','2025-05-05',1,2);
/*!40000 ALTER TABLE `hr_app_employeeexperience` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_employeepersonaldetails`
--

DROP TABLE IF EXISTS `hr_app_employeepersonaldetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_employeepersonaldetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `passport` varchar(50) DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  `Tell_number` varchar(20) DEFAULT NULL,
  `religion` varchar(100) DEFAULT NULL,
  `marital_status` varchar(50) DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  CONSTRAINT `HR_App_employeeperso_employee_id_676c7c55_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_employeepersonaldetails`
--

LOCK TABLES `hr_app_employeepersonaldetails` WRITE;
/*!40000 ALTER TABLE `hr_app_employeepersonaldetails` DISABLE KEYS */;
INSERT INTO `hr_app_employeepersonaldetails` VALUES (1,'Visa','909878765645','7000243390','Hindu','Single',1),(2,'Visa','121232123212','7898909867','Hindu','Single',2);
/*!40000 ALTER TABLE `hr_app_employeepersonaldetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_exitdocument`
--

DROP TABLE IF EXISTS `hr_app_exitdocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_exitdocument` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `document` varchar(100) NOT NULL,
  `upload_date` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `resignation_id` bigint DEFAULT NULL,
  `uploaded_by_id` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_exitdocument_employee_id_a153fc7d_fk_HR_App_em` (`employee_id`),
  KEY `HR_App_exitdocument_resignation_id_ccd2e046_fk_HR_App_re` (`resignation_id`),
  KEY `HR_App_exitdocument_uploaded_by_id_b6b42bd1_fk_auth_user_id` (`uploaded_by_id`),
  CONSTRAINT `HR_App_exitdocument_employee_id_a153fc7d_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_exitdocument_resignation_id_ccd2e046_fk_HR_App_re` FOREIGN KEY (`resignation_id`) REFERENCES `hr_app_resignationapplication` (`id`),
  CONSTRAINT `HR_App_exitdocument_uploaded_by_id_b6b42bd1_fk_auth_user_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_exitdocument`
--

LOCK TABLES `hr_app_exitdocument` WRITE;
/*!40000 ALTER TABLE `hr_app_exitdocument` DISABLE KEYS */;
/*!40000 ALTER TABLE `hr_app_exitdocument` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_exitemail`
--

DROP TABLE IF EXISTS `hr_app_exitemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_exitemail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_email` varchar(254) NOT NULL,
  `to_email` varchar(254) NOT NULL,
  `cc` varchar(254) DEFAULT NULL,
  `bcc` varchar(254) DEFAULT NULL,
  `subject` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `sent_at` datetime(6) NOT NULL,
  `employee_id` bigint DEFAULT NULL,
  `resignation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_exitemail_employee_id_0f622e10_fk_HR_App_employeebisp_id` (`employee_id`),
  KEY `HR_App_exitemail_resignation_id_afe478a6_fk_HR_App_re` (`resignation_id`),
  CONSTRAINT `HR_App_exitemail_employee_id_0f622e10_fk_HR_App_employeebisp_id` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_exitemail_resignation_id_afe478a6_fk_HR_App_re` FOREIGN KEY (`resignation_id`) REFERENCES `hr_app_resignationapplication` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_exitemail`
--

LOCK TABLES `hr_app_exitemail` WRITE;
/*!40000 ALTER TABLE `hr_app_exitemail` DISABLE KEYS */;
/*!40000 ALTER TABLE `hr_app_exitemail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_handbookacknowledgement`
--

DROP TABLE IF EXISTS `hr_app_handbookacknowledgement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_handbookacknowledgement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `acknowledged_at` datetime(6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `employee_id` bigint NOT NULL,
  `pdf_id` bigint NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HR_App_handbookacknowledgement_pdf_id_employee_id_c2c90f70_uniq` (`pdf_id`,`employee_id`),
  KEY `HR_App_handbookackno_employee_id_e57b7ccb_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `HR_App_handbookackno_employee_id_e57b7ccb_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_handbookackno_pdf_id_58a7d27b_fk_HR_App_ha` FOREIGN KEY (`pdf_id`) REFERENCES `hr_app_handbookpdf` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_handbookacknowledgement`
--

LOCK TABLES `hr_app_handbookacknowledgement` WRITE;
/*!40000 ALTER TABLE `hr_app_handbookacknowledgement` DISABLE KEYS */;
INSERT INTO `hr_app_handbookacknowledgement` VALUES (1,NULL,'Not Acknowledge',1,1,'2025-04-25 11:04:52.489634'),(2,NULL,'Not Acknowledge',2,1,'2025-05-01 07:09:03.868029'),(3,NULL,'Not Acknowledge',3,1,'2025-04-25 11:04:52.489634'),(5,NULL,'Acknowledge',2,2,'2025-05-01 10:33:45.361270'),(6,NULL,'Acknowledge',3,4,'2025-05-01 10:41:48.140909'),(7,NULL,'Acknowledge',1,6,'2025-05-01 11:09:19.201937'),(8,NULL,'Acknowledge',5,6,'2025-05-01 11:10:16.180774'),(9,NULL,'Acknowledge',3,6,'2025-05-01 12:16:19.043734'),(10,NULL,'Acknowledge',1,7,'2025-05-01 12:52:01.231549'),(11,NULL,'Acknowledge',1,8,'2025-05-03 09:29:50.339924'),(12,NULL,'Acknowledge',2,8,'2025-05-06 07:45:05.442761'),(13,NULL,'Acknowledge',1,10,'2025-05-08 11:04:44.015666'),(14,NULL,'Acknowledge',1,11,'2025-05-09 08:51:25.032946'),(15,NULL,'Acknowledge',2,11,'2025-05-14 06:37:40.539428');
/*!40000 ALTER TABLE `hr_app_handbookacknowledgement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_handbookpdf`
--

DROP TABLE IF EXISTS `hr_app_handbookpdf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_handbookpdf` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_handbookpdf`
--

LOCK TABLES `hr_app_handbookpdf` WRITE;
/*!40000 ALTER TABLE `hr_app_handbookpdf` DISABLE KEYS */;
INSERT INTO `hr_app_handbookpdf` VALUES (1,'handbooks/pdf-sample.pdf','2025-04-09 14:06:15.315714',0,'2025-04-25 11:04:52.539225'),(2,'handbooks/1000176690.pdf','2025-05-01 10:25:25.807633',0,'2025-05-01 10:25:25.807672'),(3,'handbooks/1000176690_fJ7x1vr.pdf','2025-05-01 10:37:38.778048',0,'2025-05-01 10:37:38.778081'),(4,'handbooks/1000176690_4H9QE5h.pdf','2025-05-01 10:41:20.032204',0,'2025-05-01 10:41:20.032281'),(5,'handbooks/1000176690_GyA2dRk.pdf','2025-05-01 10:50:16.186073',0,'2025-05-01 10:50:16.186111'),(6,'handbooks/pdf-sample_820L27E.pdf','2025-05-01 10:53:32.671541',0,'2025-05-01 10:53:32.671563'),(7,'handbooks/1000176690_1KEKOqm.pdf','2025-05-01 12:51:39.602726',0,'2025-05-01 12:51:39.602792'),(8,'handbooks/Employee_Handbook_2024_1.pdf','2025-05-03 09:29:16.326729',0,'2025-05-03 09:29:16.326784'),(10,'handbooks/Employee_Handbook_2024_1_MII9RCn.pdf','2025-05-08 11:04:28.674376',0,'2025-05-08 11:04:28.674415'),(11,'handbooks/Employee_Handbook_2024_1_TgHmcMy.pdf','2025-05-08 11:13:53.608440',1,'2025-05-08 11:13:53.608485');
/*!40000 ALTER TABLE `hr_app_handbookpdf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_holiday`
--

DROP TABLE IF EXISTS `hr_app_holiday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_holiday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `day` varchar(15) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_holiday`
--

LOCK TABLES `hr_app_holiday` WRITE;
/*!40000 ALTER TABLE `hr_app_holiday` DISABLE KEYS */;
INSERT INTO `hr_app_holiday` VALUES (7,'Diwali','Saturday','2025-11-15'),(8,'Friday','Friday','2025-05-16'),(9,'Hoil','Thursday','2025-03-13');
/*!40000 ALTER TABLE `hr_app_holiday` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_learningvideo`
--

DROP TABLE IF EXISTS `hr_app_learningvideo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_learningvideo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `section` varchar(50) NOT NULL,
  `video` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_learningvideo`
--

LOCK TABLES `hr_app_learningvideo` WRITE;
/*!40000 ALTER TABLE `hr_app_learningvideo` DISABLE KEYS */;
/*!40000 ALTER TABLE `hr_app_learningvideo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_leave`
--

DROP TABLE IF EXISTS `hr_app_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_leave` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `apply_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` longtext NOT NULL,
  `compensatory_off` tinyint(1) NOT NULL,
  `compensatory_reason` longtext,
  `is_half_day` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `attachment` varchar(100) DEFAULT NULL,
  `leave_days` double NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  `leave_type_id` bigint NOT NULL,
  `reject_date` datetime(6) DEFAULT NULL,
  `reject_reason` longtext,
  `half_day_type_name` varchar(250) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_leave_approved_by_id_292ba3bf_fk_HR_App_employeebisp_id` (`approved_by_id`),
  KEY `HR_App_leave_employee_id_1afd2cae_fk_HR_App_employeebisp_id` (`employee_id`),
  KEY `HR_App_leave_leave_type_id_d2b7c85b_fk_HR_App_leavetype_id` (`leave_type_id`),
  CONSTRAINT `HR_App_leave_approved_by_id_292ba3bf_fk_HR_App_employeebisp_id` FOREIGN KEY (`approved_by_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_leave_employee_id_1afd2cae_fk_HR_App_employeebisp_id` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `HR_App_leave_leave_type_id_d2b7c85b_fk_HR_App_leavetype_id` FOREIGN KEY (`leave_type_id`) REFERENCES `hr_app_leavetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_leave`
--

LOCK TABLES `hr_app_leave` WRITE;
/*!40000 ALTER TABLE `hr_app_leave` DISABLE KEYS */;
INSERT INTO `hr_app_leave` VALUES (85,'2025-04-24','2025-04-24','2025-04-25','I am going to Pune for some personal work',0,'',0,'Approved','',2,1,2,34,'2025-04-24 07:11:48.087210',NULL,'','2025-04-24 07:11:48.086707','2025-04-25 08:23:34.269175'),(86,'2025-04-24','2025-04-24','2025-04-29','I am suffering from fever',0,'',0,'Rejected','',6,1,6,34,'2025-04-24 12:24:04.597000','NO','','2025-04-24 07:12:39.096773','2025-04-24 12:24:04.597242'),(87,'2025-04-24','2025-04-24','2025-04-30','I have some personal work',0,'',0,'Withdrawn','',7,1,5,35,'2025-04-24 07:13:29.945695',NULL,'','2025-04-24 07:13:29.945518','2025-04-24 12:25:36.863360'),(88,'2025-04-25','2025-04-24','2025-04-25','I am going to pune for some work',0,'',1,'Approved','',0.5,1,1,35,'2025-04-24 08:08:13.018582',NULL,'Second Half on Friday (2025-04-25)','2025-04-24 08:08:13.018359','2025-04-24 12:22:21.682371'),(89,'2025-04-25','2025-04-24','2025-04-26','I have some work',0,'',0,'Withdrawn','',2,1,1,34,'2025-04-24 09:37:38.468671',NULL,'','2025-04-24 09:37:38.467524','2025-04-24 12:24:29.222175'),(90,'2025-04-26','2025-04-24','2025-04-26','I have some work',0,'',1,'Withdrawn','',0.5,1,5,35,'2025-04-24 09:38:39.752412',NULL,'First Half on Saturday (2025-04-26)','2025-04-24 09:38:39.752022','2025-04-24 12:25:31.583921'),(91,'2025-04-25','2025-04-24','2025-04-25','I want second half form bank work',0,'',1,'Approved','',0.5,1,2,34,'2025-04-24 11:16:39.735962',NULL,'Second Half on Friday (2025-04-25)','2025-04-24 11:16:39.735395','2025-04-24 12:22:21.682371'),(92,'2025-04-25','2025-04-24','2025-04-25','I am going to indore',0,'',0,'Rejected','',1,1,2,35,'2025-04-24 12:34:40.179195','Project is on deadtime','','2025-04-24 11:35:15.576035','2025-04-24 12:34:40.179409'),(93,'2025-04-26','2025-04-25','2025-04-26','I have some urgent work',0,'',1,'Approved','',0.5,1,2,35,'2025-04-25 06:06:24.442395',NULL,'Second Half on Saturday (2025-04-26)','2025-04-25 06:06:24.441970','2025-04-25 08:21:50.730117'),(94,'2025-04-26','2025-04-25','2025-04-26','I have some work',0,'',1,'Approved','',0.5,1,1,35,'2025-04-25 08:24:24.714618',NULL,'First Half on Saturday (2025-04-26)','2025-04-25 08:24:24.714261','2025-04-25 08:24:31.591212'),(95,'2025-04-26','2025-04-25','2025-04-26','I am suffering from common cold',0,'',1,'Rejected','',0.5,1,2,35,'2025-04-26 10:23:00.232534','Project is on deadline','Second Half on Saturday (2025-04-26)','2025-04-25 08:25:45.943192','2025-04-26 10:23:00.232970'),(96,'2025-04-26','2025-04-25','2025-04-26','I have some urgent work',0,'',0,'Approved','',1,1,5,35,'2025-04-25 11:16:48.499464',NULL,'','2025-04-25 11:16:48.499061','2025-04-26 07:06:17.816367'),(97,'2025-04-28','2025-04-26','2025-04-28','I have some urgent work on monday',0,'',1,'Approved','',0.5,1,6,34,'2025-04-26 10:20:56.924196',NULL,'Second Half on Monday (2025-04-28)','2025-04-26 10:20:56.922337','2025-04-26 10:22:37.486970'),(98,'2025-04-28','2025-04-26','2025-04-28','I am suffering from fever',0,'',0,'Pending','',1,NULL,6,34,'2025-04-26 10:40:43.361445',NULL,'','2025-04-26 10:40:43.360863','2025-04-26 10:40:43.361620'),(100,'2025-05-02','2025-05-01','2025-05-02','I have some urgent work in Noida',0,'',1,'Approved','leave_attachments/Screenshot_2025-04-11_112816.png',0.5,1,2,34,'2025-05-01 06:48:04.506144',NULL,'First Half on Friday (2025-05-02)','2025-05-01 06:48:04.505995','2025-05-01 06:49:35.845737'),(101,'2025-05-02','2025-05-01','2025-05-02','I have work',0,'',1,'Pending','',0.5,NULL,2,34,'2025-05-01 08:18:48.916788',NULL,'Second Half on Friday (2025-05-02)','2025-05-01 08:18:48.916073','2025-05-01 08:18:48.916982'),(102,'2025-05-09','2025-05-01','2025-05-09','i have some work',0,'',0,'Pending','',1,NULL,3,34,'2025-05-01 11:25:00.441764',NULL,'','2025-05-01 11:25:00.441454','2025-05-01 11:25:00.441841'),(103,'2025-05-17','2025-05-01','2025-05-17','i have some work',0,'',0,'Pending','',1,NULL,2,35,'2025-05-01 11:28:10.058482',NULL,'','2025-05-01 11:28:10.058250','2025-05-01 11:28:10.058553'),(104,'2025-05-03','2025-05-03','2025-05-03','I am traveling to Agra to attend my brother’s wedding.',0,'',0,'Withdrawn','',1,NULL,3,35,'2025-05-03 09:27:28.775813',NULL,'','2025-05-03 09:27:28.775622','2025-05-03 09:27:48.657137'),(105,'2025-05-05','2025-05-05','2025-05-05','I have some urgent work',0,'',0,'Pending','',1,NULL,9,38,'2025-05-05 07:28:52.979901',NULL,'','2025-05-05 07:28:52.979641','2025-05-05 07:28:52.980024'),(106,'2025-05-06','2025-05-06','2025-05-07','Tuesday full day and wednesday Half day',0,'',1,'Approved','',1.5,1,2,34,'2025-05-06 07:42:55.590684',NULL,'First Half on Wednesday (2025-05-07)','2025-05-06 07:42:55.590199','2025-05-06 07:44:19.753697'),(107,'2025-05-10','2025-05-09','2025-05-10','I have some urgent work tommorrow',0,'',1,'Pending','',0.5,NULL,1,29,'2025-05-09 09:07:54.969167',NULL,'Second Half on Saturday (2025-05-10)','2025-05-09 09:07:54.968598','2025-05-09 09:07:54.969285'),(108,'2025-05-14','2025-05-14','2025-05-15','hare krishna temple visit',0,'',1,'Pending','',1,NULL,3,34,'2025-05-14 11:29:03.840750',NULL,'First Half on Wednesday (2025-05-14), First Half on Thursday (2025-05-15)','2025-05-14 11:29:03.840403','2025-05-14 11:29:03.840842'),(109,'2025-05-19','2025-05-15','2025-05-21','Holiday leave',0,'',0,'Approved','',3,1,1,34,'2025-05-15 10:07:36.913708',NULL,'','2025-05-15 10:07:36.912945','2025-05-23 09:29:11.999142'),(113,'2025-05-16','2025-05-16','2025-05-16','emergency',0,'',0,'Approved','',0,1,1,34,'2025-05-16 10:11:36.228944',NULL,'','2025-05-16 10:11:36.228142','2025-05-23 09:28:33.314545'),(114,'2025-05-21','2025-05-20','2025-05-21','ef',0,'',0,'Approved','',1,1,11,35,'2025-05-20 10:30:34.968557',NULL,'','2025-05-20 10:30:34.968287','2025-05-23 09:27:45.544915'),(115,'2025-05-23','2025-05-23','2025-05-23','urgent work',0,'',0,'Pending','',1,NULL,1,34,'2025-05-23 09:31:49.707315',NULL,'','2025-05-23 09:31:49.707030','2025-05-23 09:31:49.707381'),(116,'2025-05-23','2025-05-23','2025-05-23','urgent work',0,'',0,'Pending','',1,NULL,1,38,'2025-05-23 09:33:12.110063',NULL,'','2025-05-23 09:33:12.109875','2025-05-23 09:33:12.110120'),(117,'2025-05-23','2025-05-23','2025-05-23','urgent work',0,'',0,'Pending','',1,NULL,1,38,'2025-05-23 09:34:15.377930',NULL,'','2025-05-23 09:34:15.377616','2025-05-23 09:34:15.378010');
/*!40000 ALTER TABLE `hr_app_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_leavetype`
--

DROP TABLE IF EXISTS `hr_app_leavetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_leavetype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `accrual` tinyint(1) NOT NULL,
  `effective_after` int unsigned DEFAULT NULL,
  `effective_from` varchar(3) NOT NULL,
  `status` varchar(10) NOT NULL,
  `leave_time` int unsigned DEFAULT NULL,
  `leave_time_unit` varchar(10) NOT NULL,
  `leave_type` varchar(20) NOT NULL,
  `count_weekends_as_leave` tinyint(1) NOT NULL,
  `count_holidays_as_leave` tinyint(1) NOT NULL,
  `leave_frequency` varchar(10) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `marital_status` varchar(10) DEFAULT NULL,
  `department_id` bigint DEFAULT NULL,
  `effective_after_value` varchar(10) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `version` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `HR_App_leavetype_department_id_210fcbb4_fk_HR_App_department_id` (`department_id`),
  CONSTRAINT `HR_App_leavetype_department_id_210fcbb4_fk_HR_App_department_id` FOREIGN KEY (`department_id`) REFERENCES `hr_app_department` (`id`),
  CONSTRAINT `hr_app_leavetype_chk_1` CHECK ((`effective_after` >= 0)),
  CONSTRAINT `hr_app_leavetype_chk_2` CHECK ((`leave_time` >= 0)),
  CONSTRAINT `hr_app_leavetype_chk_3` CHECK ((`version` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_leavetype`
--

LOCK TABLES `hr_app_leavetype` WRITE;
/*!40000 ALTER TABLE `hr_app_leavetype` DISABLE KEYS */;
INSERT INTO `hr_app_leavetype` VALUES (18,'MEDI','MM',1,NULL,'DOJ','inactive',18,'DAYS','Paid',1,0,'YEARLY','male','single',3,'Year',0,'2025-04-22 07:46:49.664975',2),(20,'Maternity 2','MMJ',1,NULL,'DOJ','inactive',15,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-04-22 07:46:47.391022',2),(21,'HLL','HL',1,1,'DOJ','inactive',13,'DAYS','Paid',1,0,'YEARLY','male','single',1,'day',1,'2025-04-22 08:21:04.822951',4),(22,'Privliage','PL',1,NULL,'DOJ','inactive',17,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-04-22 08:21:08.043434',7),(23,'Project leave','POL',1,NULL,'DOJ','inactive',14,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-04-22 07:46:52.013114',2),(25,'ppl 3','p01',1,NULL,'DOJ','inactive',12,'DAYS','Paid',1,0,'YEARLY','male','single',4,'Year',0,'2025-04-22 08:21:11.196492',8),(26,'Festive ','FL',1,1,'DOJ','inactive',15,'DAYS','Paid',1,0,'YEARLY','male','single',3,'Year',0,'2025-04-22 07:46:56.849812',6),(27,'Spring','SP',1,NULL,'DOJ','inactive',1,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-04-22 08:21:14.104925',6),(29,'Medical Leave','ML',1,NULL,'DOJ','inactive',15,'DAYS','Paid',1,0,'YEARLY','male','single',1,'Day',0,'2025-05-23 09:24:26.008673',11),(30,'Gaurav','GA',1,NULL,'DOJ','inactive',12,'DAYS','Paid',1,0,'YEARLY','male','single',3,'year',1,'2025-04-22 08:47:37.094315',5),(34,'Sick','SL',1,2,'DOJ','active',13,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Day',0,'2025-05-15 10:07:56.066589',7),(35,'Casual','CS',1,NULL,'DOJ','active',18,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-05-06 09:58:52.249102',7),(38,'Preparation','pre',1,NULL,'DOJ','active',18,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Year',0,'2025-05-02 12:28:04.595165',3),(39,'Paternity Leave','PT11',1,NULL,'DOJ','active',15,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,NULL,'Day',0,'2025-05-06 09:56:24.501087',1);
/*!40000 ALTER TABLE `hr_app_leavetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_leavetypehistory`
--

DROP TABLE IF EXISTS `hr_app_leavetypehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_leavetypehistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `accrual` tinyint(1) NOT NULL,
  `effective_after` int unsigned DEFAULT NULL,
  `effective_after_value` varchar(10) NOT NULL,
  `effective_from` varchar(3) NOT NULL,
  `status` varchar(10) NOT NULL,
  `leave_time` int unsigned DEFAULT NULL,
  `leave_time_unit` varchar(10) NOT NULL,
  `leave_type_field` varchar(20) NOT NULL,
  `count_weekends_as_leave` tinyint(1) NOT NULL,
  `count_holidays_as_leave` tinyint(1) NOT NULL,
  `leave_frequency` varchar(10) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `marital_status` varchar(10) DEFAULT NULL,
  `version` int unsigned NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `department_id` bigint DEFAULT NULL,
  `leave_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_leavetypehist_department_id_ef52e7e2_fk_HR_App_de` (`department_id`),
  KEY `HR_App_leavetypehist_leave_type_id_3f40771a_fk_HR_App_le` (`leave_type_id`),
  CONSTRAINT `HR_App_leavetypehist_department_id_ef52e7e2_fk_HR_App_de` FOREIGN KEY (`department_id`) REFERENCES `hr_app_department` (`id`),
  CONSTRAINT `HR_App_leavetypehist_leave_type_id_3f40771a_fk_HR_App_le` FOREIGN KEY (`leave_type_id`) REFERENCES `hr_app_leavetype` (`id`),
  CONSTRAINT `hr_app_leavetypehistory_chk_1` CHECK ((`effective_after` >= 0)),
  CONSTRAINT `hr_app_leavetypehistory_chk_2` CHECK ((`leave_time` >= 0)),
  CONSTRAINT `hr_app_leavetypehistory_chk_3` CHECK ((`version` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_leavetypehistory`
--

LOCK TABLES `hr_app_leavetypehistory` WRITE;
/*!40000 ALTER TABLE `hr_app_leavetypehistory` DISABLE KEYS */;
INSERT INTO `hr_app_leavetypehistory` VALUES (3,'Apurv','AP',1,1,'Day','DOJ','active',15,'DAYS','Paid',1,0,'YEARLY','male','single',4,'2025-04-22 07:48:03.921900',1,29),(5,'Spring','SP',1,12,'Year','DOJ','inactive',1,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,3,'2025-04-22 07:47:02.184149',NULL,27),(6,'Privliage','PL',1,NULL,'Year','DOJ','inactive',17,'DAYS','Paid',1,0,'YEARLY','male','single',4,'2025-04-22 07:46:45.010830',1,22),(7,'Sick','SL',1,NULL,'Year','DOJ','active',13,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,1,'2025-04-22 08:11:16.237794',NULL,34),(8,'Apurv','AP',1,NULL,'Day','DOJ','active',15,'DAYS','Paid',1,0,'YEARLY','male','single',8,'2025-04-23 10:15:08.665446',1,29),(9,'Preparation','pre',1,NULL,'Year','DOJ','active',18,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,1,'2025-05-02 12:23:53.235130',NULL,38),(10,'Casual','CS',1,NULL,'Year','DOJ','inactive',20,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,5,'2025-05-06 09:57:12.944425',NULL,35),(11,'Sick','SL',1,2,'Day','DOJ','active',13,'DAYS','Paid',1,0,'YEARLY',NULL,NULL,3,'2025-04-23 06:23:12.886076',NULL,34),(12,'Sick','SL',1,2,'Day','DOJ','active',13,'DAYS','Paid',1,1,'YEARLY',NULL,NULL,5,'2025-05-15 10:07:08.274117',NULL,34);
/*!40000 ALTER TABLE `hr_app_leavetypehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_app_resignationapplication`
--

DROP TABLE IF EXISTS `hr_app_resignationapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_app_resignationapplication` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `resignation_apply_date` date NOT NULL,
  `last_working_date` date NOT NULL,
  `reason` longtext,
  `selected_elsewhere` tinyint(1) NOT NULL,
  `bond_period_over` tinyint(1) NOT NULL,
  `advance_salary_taken` tinyint(1) NOT NULL,
  `dues_pending` tinyint(1) NOT NULL,
  `submitted_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `hr_approved` tinyint(1) DEFAULT NULL,
  `manager_approved` tinyint(1) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HR_App_resignationap_employee_id_2ce87f70_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `HR_App_resignationap_employee_id_2ce87f70_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_app_resignationapplication`
--

LOCK TABLES `hr_app_resignationapplication` WRITE;
/*!40000 ALTER TABLE `hr_app_resignationapplication` DISABLE KEYS */;
/*!40000 ALTER TABLE `hr_app_resignationapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_project`
--

DROP TABLE IF EXISTS `project_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_name` varchar(200) NOT NULL,
  `client_name` varchar(200) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `rate_status` varchar(20) NOT NULL,
  `rate_currency` varchar(10) NOT NULL,
  `rate_amount` decimal(10,2) DEFAULT NULL,
  `priority` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `upload_file` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `admin_id` bigint DEFAULT NULL,
  `leader_id` bigint DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `version` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Project_project_admin_id_bd688694_fk_HR_App_employeebisp_id` (`admin_id`),
  KEY `Project_project_leader_id_73e94e77_fk_HR_App_employeebisp_id` (`leader_id`),
  CONSTRAINT `Project_project_admin_id_bd688694_fk_HR_App_employeebisp_id` FOREIGN KEY (`admin_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_project_leader_id_73e94e77_fk_HR_App_employeebisp_id` FOREIGN KEY (`leader_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_project`
--

LOCK TABLES `project_project` WRITE;
/*!40000 ALTER TABLE `project_project` DISABLE KEYS */;
INSERT INTO `project_project` VALUES (1,'BISP Infonent','BISP','2025-04-12','2025-04-13','Billable','Rs',1200.00,'Low','Complete within given timeslot on time\r\n','','2025-04-11 10:46:42.930833',1,1,'Inactive','2025-05-01 09:34:19.796341',8),(2,'Django','Inhouse','2025-04-13','2025-05-12','Billable','Rs',1800.00,'Low','hare krsna','project_files/Screenshot_2025-04-09_211824.png','2025-04-11 11:00:10.765851',3,3,'Inactive','2025-05-01 11:19:48.590882',6),(3,'Employee 23','Inhouse','2025-04-13','2025-05-26','Billable','USD',1200.00,'High','New Project','','2025-04-11 11:57:38.352040',1,1,'Inactive','2025-05-01 09:43:21.634872',4),(4,'Employee Model 2','Inhouse','2025-04-15','2025-04-20','Billable','Rs',500.00,'Low','yes','','2025-04-14 11:39:57.897300',1,1,'Inactive','2025-05-01 09:59:59.301441',2),(5,'EMART','Infosys','2025-04-15','2025-06-15','Billable','USD',50000.00,'High','important','','2025-04-14 12:14:20.833185',3,1,'Inactive','2025-05-01 11:18:31.365795',3),(6,'Demo of Python Project','Inhouse','2025-04-01','2025-04-30','Non Billable','Rs',0.00,'Low','It is inhouse project of BISP','','2025-04-15 08:54:44.970619',1,3,'Inactive','2025-05-01 09:27:41.788753',5),(7,'React','Inhouse','2025-04-11','2025-04-28','Non Billable','Rs',1222.00,'Low','ef','','2025-04-18 11:29:20.910539',1,3,'Inactive','2025-05-01 09:28:21.890274',3),(8,'HR_Portal','Inhouse','2025-04-18','2025-04-30','Non Billable','Rs',0.00,'Low','Inhouse project','','2025-04-18 11:39:07.060489',1,3,'Inactive','2025-05-01 11:16:59.308257',2),(9,'Djano 2','BISP','2025-04-18','2025-04-20','Non Billable','Rs',122.00,'Low','n','','2025-04-18 11:41:27.524833',3,1,'Inactive','2025-05-01 11:14:55.544605',2),(10,'BISP 3','Infosys','2025-04-18','2025-04-30','Non Billable','Rs',23.00,'Low','3','','2025-04-18 11:42:36.707323',3,1,'Inactive','2025-05-01 11:07:23.939812',2),(11,'MM','BISP','2025-04-23','2025-04-27','Non Billable','Rs',1200.00,'Low','s','','2025-04-22 13:20:32.492170',1,1,'Inactive','2025-05-01 09:33:48.481967',3),(12,'Google map clone','Inhouse','2025-04-25','2025-05-20','Non Billable','Rs',50000.00,'Low','Complete before deadline','','2025-04-24 11:20:20.932177',3,1,'Inactive','2025-05-01 11:05:15.712928',4),(13,'CRM','Inhouse','2025-05-03','2025-05-13','Non Billable','Rs',0.00,'Low','Completed within deadline','','2025-05-01 08:14:15.253495',1,1,'Inactive','2025-05-01 09:28:33.374953',2),(14,'CRM','Inhouse','2025-05-02','2025-05-12','Non Billable','Rs',0.00,'Low','Complete within 2 months','','2025-05-01 11:01:10.308347',1,3,'Inactive','2025-05-01 11:01:56.588072',2),(15,'CVC','Inhouse','2025-05-03','2025-05-18','Non Billable','Rs',0.00,'Low','C','','2025-05-01 11:11:36.031087',1,1,'Inactive','2025-05-01 11:12:23.096832',2),(16,'CVS','Inhouse','2025-05-10','2025-05-22','Non Billable','Rs',0.00,'Low','v','','2025-05-01 11:17:30.644096',1,1,'Inactive','2025-05-01 11:20:23.932313',2),(17,'HR_Portal','BISP','2025-05-10','2025-05-20','Non Billable','Rs',0.00,'Low','It is Inhouse project','','2025-05-01 11:27:19.216387',3,1,'active','2025-05-01 11:27:19.216408',1),(18,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','','2025-05-06 07:32:28.853973',1,1,'active','2025-05-22 09:43:21.537382',16);
/*!40000 ALTER TABLE `project_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_project_team_members`
--

DROP TABLE IF EXISTS `project_project_team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_project_team_members` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_id` bigint NOT NULL,
  `employeebisp_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Project_project_team_mem_project_id_employeebisp__1f3c3b3e_uniq` (`project_id`,`employeebisp_id`),
  KEY `Project_project_team_employeebisp_id_ed52d4ed_fk_HR_App_em` (`employeebisp_id`),
  CONSTRAINT `Project_project_team_employeebisp_id_ed52d4ed_fk_HR_App_em` FOREIGN KEY (`employeebisp_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_project_team_project_id_be26c890_fk_Project_p` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_project_team_members`
--

LOCK TABLES `project_project_team_members` WRITE;
/*!40000 ALTER TABLE `project_project_team_members` DISABLE KEYS */;
INSERT INTO `project_project_team_members` VALUES (1,1,2),(30,1,5),(5,2,2),(23,2,5),(24,2,6),(9,3,2),(31,3,5),(34,3,6),(10,4,1),(11,4,2),(12,4,3),(14,5,2),(25,5,5),(26,5,6),(16,6,2),(27,7,2),(28,7,5),(29,7,6),(18,8,2),(19,8,5),(20,9,2),(21,9,6),(22,10,2),(32,11,2),(33,11,6),(35,12,2),(37,13,2),(38,14,2),(39,15,5),(40,16,2),(41,17,2),(42,17,5),(45,18,5),(46,18,11);
/*!40000 ALTER TABLE `project_project_team_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_projecthistory`
--

DROP TABLE IF EXISTS `project_projecthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_projecthistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_name` varchar(200) NOT NULL,
  `client_name` varchar(200) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `rate_status` varchar(20) NOT NULL,
  `rate_currency` varchar(10) NOT NULL,
  `rate_amount` decimal(10,2) DEFAULT NULL,
  `priority` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `upload_file` varchar(100) DEFAULT NULL,
  `version` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `admin_id` bigint DEFAULT NULL,
  `leader_id` bigint DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Project_projecthisto_admin_id_73e03c74_fk_HR_App_em` (`admin_id`),
  KEY `Project_projecthisto_leader_id_c2e4fb18_fk_HR_App_em` (`leader_id`),
  KEY `Project_projecthistory_project_id_6eae5841_fk_Project_project_id` (`project_id`),
  CONSTRAINT `Project_projecthisto_admin_id_73e03c74_fk_HR_App_em` FOREIGN KEY (`admin_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_projecthisto_leader_id_c2e4fb18_fk_HR_App_em` FOREIGN KEY (`leader_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_projecthistory_project_id_6eae5841_fk_Project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_projecthistory`
--

LOCK TABLES `project_projecthistory` WRITE;
/*!40000 ALTER TABLE `project_projecthistory` DISABLE KEYS */;
INSERT INTO `project_projecthistory` VALUES (58,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',5655.00,'High','It\'s a project of one year implementation of netsuit','',8,'2025-05-21 12:35:01.334320',1,1,18,'2025-05-21 12:24:27.756228'),(59,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',8000.00,'High','It\'s a project of one year implementation of netsuit','',9,'2025-05-21 12:35:28.546913',1,1,18,'2025-05-21 12:35:01.345495'),(60,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',9000.00,'High','It\'s a project of one year implementation of netsuit','',10,'2025-05-21 12:36:21.576239',1,1,18,'2025-05-21 12:35:28.557878'),(61,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',9098.00,'High','It\'s a project of one year implementation of netsuit','',11,'2025-05-21 12:41:49.405434',1,1,18,'2025-05-21 12:36:21.581117'),(62,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Non Billable','Rs',NULL,'High','It\'s a project of one year implementation of netsuit','',12,'2025-05-21 13:01:42.832076',1,1,18,'2025-05-21 12:41:49.417069'),(63,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','',13,'2025-05-22 09:36:33.470063',1,1,18,'2025-05-21 13:01:42.864924'),(64,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','',13,'2025-05-22 09:36:37.272160',1,1,18,'2025-05-21 13:01:42.864924'),(65,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','',14,'2025-05-22 09:42:34.936397',1,1,18,'2025-05-22 09:36:37.280543'),(66,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','',14,'2025-05-22 09:42:37.910969',1,1,18,'2025-05-22 09:36:37.280543'),(67,'CH Furniture Projects','CLassic Home','2025-01-01','2026-01-01','Billable','Rs',900000.00,'High','It\'s a project of one year implementation of netsuit','',15,'2025-05-22 09:43:21.527351',1,1,18,'2025-05-22 09:42:37.922933');
/*!40000 ALTER TABLE `project_projecthistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_projecthistory_team_members`
--

DROP TABLE IF EXISTS `project_projecthistory_team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_projecthistory_team_members` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `projecthistory_id` bigint NOT NULL,
  `employeebisp_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Project_projecthistory_t_projecthistory_id_employ_525bd66a_uniq` (`projecthistory_id`,`employeebisp_id`),
  KEY `Project_projecthisto_employeebisp_id_105b9c3a_fk_HR_App_em` (`employeebisp_id`),
  CONSTRAINT `Project_projecthisto_employeebisp_id_105b9c3a_fk_HR_App_em` FOREIGN KEY (`employeebisp_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_projecthisto_projecthistory_id_6859597b_fk_Project_p` FOREIGN KEY (`projecthistory_id`) REFERENCES `project_projecthistory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_projecthistory_team_members`
--

LOCK TABLES `project_projecthistory_team_members` WRITE;
/*!40000 ALTER TABLE `project_projecthistory_team_members` DISABLE KEYS */;
INSERT INTO `project_projecthistory_team_members` VALUES (1,62,2),(2,62,5),(3,63,2),(4,63,5),(5,64,2),(6,64,5),(8,65,5),(7,65,11),(10,66,5),(9,66,11),(12,67,5),(11,67,11),(13,67,62);
/*!40000 ALTER TABLE `project_projecthistory_team_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_task`
--

DROP TABLE IF EXISTS `project_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_title` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `description` longtext,
  `created_at` datetime(6) NOT NULL,
  `assigned_to_id` bigint DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `version` int NOT NULL,
  `status_field` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Project_task_assigned_to_id_93dd5d60_fk_HR_App_employeebisp_id` (`assigned_to_id`),
  KEY `Project_task_project_id_e4da143e_fk_Project_project_id` (`project_id`),
  CONSTRAINT `Project_task_assigned_to_id_93dd5d60_fk_HR_App_employeebisp_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_task_project_id_e4da143e_fk_Project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_task`
--

LOCK TABLES `project_task` WRITE;
/*!40000 ALTER TABLE `project_task` DISABLE KEYS */;
INSERT INTO `project_task` VALUES (1,'Add Employees','2025-04-12','2025-04-14','Completed','Low','Complete on time','2025-04-15 11:45:43.090125',2,1,'2025-04-26 08:10:12.949236',19,'active'),(2,'Add Leave','2025-04-15','2025-04-17','Claimed Completed','Low','yes','2025-04-24 12:13:48.018120',2,1,'2025-04-24 12:13:48.018345',4,'active'),(3,'Add task','2025-04-15','2025-04-18','Completed','Low','yes','2025-05-01 06:58:55.740614',6,1,'2025-05-01 06:58:55.740728',5,'active'),(4,'Add Project','2025-04-20','2025-04-23','Inprogress','Low','yes','2025-04-24 09:55:37.933818',2,1,'2025-04-24 09:55:37.933966',2,'active'),(5,'Add Timesheet','2025-04-15','2025-04-17','Completed','High','yes','2025-04-16 09:40:18.972688',3,3,'2025-04-22 11:27:07.349411',1,'active'),(6,'Add Product','2025-04-15','2025-04-20','Completed','High','complete within timeslot','2025-04-26 05:37:13.265608',6,5,'2025-04-26 05:37:13.266052',10,'active'),(7,'Development of HR','2025-04-15','2025-04-20','Inprogress','Low','Development is given to Yash ','2025-04-24 09:56:09.775586',2,6,'2025-04-24 09:56:09.775728',5,'active'),(8,'Design Task 23','2025-04-15','2025-04-20','Completed','Low','Design is given to devesh','2025-04-15 08:57:20.185081',2,6,'2025-04-22 13:14:48.223136',5,'active'),(40,'Add Employee 123','2025-04-23','2025-04-26','Claimed Completed','Low','e','2025-04-24 12:26:09.464916',5,5,'2025-04-24 12:26:09.465113',6,'active'),(41,'Demo','2025-04-23','2025-04-27','Completed','Low','ssc','2025-05-01 08:03:39.484012',5,3,'2025-05-01 08:03:39.484307',4,'active'),(42,'dfs','2025-04-23','2025-04-29','Pending','Low','dsf','2025-04-23 06:16:16.968604',5,2,'2025-04-23 06:16:16.968681',1,'active'),(43,'sfa','2025-04-23','2025-04-25','Pending','Low','saas','2025-04-23 06:17:49.698940',5,3,'2025-04-23 06:17:49.699015',1,'active'),(44,'HandleTimesheet','2025-04-24','2025-04-27','Inprogress','Low','Complete on Time','2025-04-24 06:44:40.869013',2,8,'2025-04-24 06:44:40.869228',2,'active'),(45,'Learning video','2025-04-26','2025-04-28','Pending','Low','Complete within given timeslot','2025-04-26 10:39:27.177433',6,6,'2025-04-26 10:39:27.177508',1,'active'),(46,'Add report','2025-05-02','2025-05-10','Claimed Completed','Low','It is urgent','2025-05-01 08:19:40.505817',2,1,'2025-05-01 08:19:40.505894',3,'active'),(47,'Add Profile','2025-05-02','2025-05-06','Pending','Low','It is urgent','2025-05-01 08:04:41.199697',5,2,'2025-05-01 08:04:41.199753',1,'active'),(48,'Add exit system','2025-05-03','2025-05-04','Pending','Low','It is urgent','2025-05-01 08:06:52.436053',5,2,'2025-05-01 08:16:43.957848',3,'active'),(49,'Add Employees','2025-05-10','2025-05-21','Completed','High','Completed within time','2025-05-09 09:33:36.246759',2,17,'2025-05-21 12:43:20.831098',13,'active'),(50,'Information gathering','2025-01-01','2026-01-01','Pending','High','Yash is given the task of information gathering','2025-05-06 07:34:06.052191',2,18,'2025-05-07 10:59:12.117766',2,'active');
/*!40000 ALTER TABLE `project_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_taskhistory`
--

DROP TABLE IF EXISTS `project_taskhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_taskhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_title` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `priority` varchar(10) NOT NULL,
  `description` longtext,
  `version` int NOT NULL,
  `status` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `assigned_to_id` bigint DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  `status_field` varchar(20) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Project_taskhistory_assigned_to_id_98ea79d8_fk_HR_App_em` (`assigned_to_id`),
  KEY `Project_taskhistory_project_id_28b53060_fk_Project_project_id` (`project_id`),
  KEY `Project_taskhistory_task_id_e2349f82_fk_Project_task_id` (`task_id`),
  CONSTRAINT `Project_taskhistory_assigned_to_id_98ea79d8_fk_HR_App_em` FOREIGN KEY (`assigned_to_id`) REFERENCES `hr_app_employeebisp` (`id`),
  CONSTRAINT `Project_taskhistory_project_id_28b53060_fk_Project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`),
  CONSTRAINT `Project_taskhistory_task_id_e2349f82_fk_Project_task_id` FOREIGN KEY (`task_id`) REFERENCES `project_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_taskhistory`
--

LOCK TABLES `project_taskhistory` WRITE;
/*!40000 ALTER TABLE `project_taskhistory` DISABLE KEYS */;
INSERT INTO `project_taskhistory` VALUES (46,'Add Employees','2025-05-10','2025-05-21','Low','Completed within time',3,'Pending','2025-05-02 06:59:07.015964',2,17,49,'active',NULL),(47,'Information gathering','2025-01-01','2026-01-01','Low','Yash is given the task of information gathering',1,'Pending','2025-05-07 10:59:12.105144',2,18,50,'active','2025-05-06 07:34:06.052226'),(48,'Add Employees','2025-05-10','2025-05-21','Low','Completed within time',4,'Claimed Completed','2025-05-07 11:02:47.308112',2,17,49,'active','2025-05-02 06:59:07.033245'),(49,'Add Employees','2025-05-10','2025-05-21','High','Completed within time',11,'Completed','2025-05-21 12:42:50.015947',2,17,49,'active','2025-05-09 09:33:36.246937'),(50,'Add Employees','2025-05-10','2025-05-21','Medium','Completed within time',12,'Completed','2025-05-21 12:43:20.822162',2,17,49,'active','2025-05-21 12:42:50.028376');
/*!40000 ALTER TABLE `project_taskhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timesheet_imagetaskrecord`
--

DROP TABLE IF EXISTS `timesheet_imagetaskrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timesheet_imagetaskrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `employee_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Timesheet_imagetaskr_employee_id_a663f4a3_fk_HR_App_em` (`employee_id`),
  CONSTRAINT `Timesheet_imagetaskr_employee_id_a663f4a3_fk_HR_App_em` FOREIGN KEY (`employee_id`) REFERENCES `hr_app_employeebisp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timesheet_imagetaskrecord`
--

LOCK TABLES `timesheet_imagetaskrecord` WRITE;
/*!40000 ALTER TABLE `timesheet_imagetaskrecord` DISABLE KEYS */;
INSERT INTO `timesheet_imagetaskrecord` VALUES (1,'timesheet_files/WhatsApp_Image_2025-04-16_at_17.29.30_7aad1f50.jpg','2025-04-21','2025-04-27',1),(2,'timesheet_files/Screenshot_2025-04-11_112816_vAecryt.png','2025-04-28','2025-05-04',1),(3,'timesheet_files/Screenshot_2025-04-11_112816_Fnd9sfB.png','2025-04-28','2025-05-04',2),(4,'timesheet_files/Screenshot_2025-04-12_114454.png','2025-04-28','2025-05-04',2),(5,'timesheet_files/Screenshot_2025-04-12_114454_BBbHhEu.png','2025-05-05','2025-05-11',2),(6,'timesheet_files/pdf-sample_1.pdf','2025-05-05','2025-05-11',2);
/*!40000 ALTER TABLE `timesheet_imagetaskrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timesheet_taskrecord`
--

DROP TABLE IF EXISTS `timesheet_taskrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timesheet_taskrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `record_name` varchar(255) NOT NULL,
  `attachment` varchar(100) DEFAULT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Timesheet_taskrecord_task_id_c295af9a_fk_Project_task_id` (`task_id`),
  CONSTRAINT `Timesheet_taskrecord_task_id_c295af9a_fk_Project_task_id` FOREIGN KEY (`task_id`) REFERENCES `project_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=692 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timesheet_taskrecord`
--

LOCK TABLES `timesheet_taskrecord` WRITE;
/*!40000 ALTER TABLE `timesheet_taskrecord` DISABLE KEYS */;
INSERT INTO `timesheet_taskrecord` VALUES (595,'2025-04-14','11:00:00.000000','20:00:00.000000','completed','',3),(596,'2025-04-15','11:00:00.000000','20:00:00.000000','completed','',3),(597,'2025-04-16','11:00:00.000000','20:00:00.000000','completed','',3),(598,'2025-04-17','11:00:00.000000','20:00:00.000000','completed','',3),(599,'2025-04-18','11:00:00.000000','20:00:00.000000','completed','',3),(600,'2025-04-19','11:00:00.000000','20:00:00.000000','completed','',3),(601,'2025-04-14','11:00:00.000000','20:00:00.000000','o','',7),(602,'2025-04-15','11:00:00.000000','20:00:00.000000','a','',7),(603,'2025-04-16','11:00:00.000000','20:00:00.000000','a','',7),(604,'2025-04-17','11:00:00.000000','20:00:00.000000','a','',7),(605,'2025-04-18','11:00:00.000000','20:00:00.000000','a','',7),(606,'2025-04-19','11:00:00.000000','20:00:00.000000','a','',7),(607,'2025-04-14','11:00:00.000000','20:00:00.000000','a','',3),(608,'2025-04-15','11:00:00.000000','20:00:00.000000','a','',3),(609,'2025-04-16','11:00:00.000000','20:00:00.000000','a','',3),(610,'2025-04-17','11:00:00.000000','20:00:00.000000','a','',3),(611,'2025-04-18','11:00:00.000000','20:00:00.000000','a','',3),(612,'2025-04-19','11:00:00.000000','20:00:00.000000','a','',3),(613,'2025-04-20','11:00:00.000000','20:00:00.000000','a','',3),(614,'2025-04-14','11:00:00.000000','20:00:00.000000','v','',3),(615,'2025-04-15','11:00:00.000000','20:00:00.000000','v','',3),(616,'2025-04-16','11:00:00.000000','20:00:00.000000','v','',3),(617,'2025-04-17','11:00:00.000000','20:00:00.000000','v','',3),(618,'2025-04-18','11:00:00.000000','20:00:00.000000','v','',3),(619,'2025-04-19','11:00:00.000000','20:00:00.000000','v','',3),(620,'2025-04-20','11:00:00.000000','20:00:00.000000','v','',3),(621,'2025-04-14','11:00:00.000000','20:00:00.000000','d','',3),(622,'2025-04-15','11:00:00.000000','20:00:00.000000','d','',3),(623,'2025-04-16','11:00:00.000000','20:00:00.000000','d','',3),(624,'2025-04-17','11:00:00.000000','20:00:00.000000','d','',3),(625,'2025-04-18','11:00:00.000000','20:00:00.000000','d','',3),(626,'2025-04-19','11:00:00.000000','20:00:00.000000','d','',3),(627,'2025-04-20','11:00:00.000000','20:00:00.000000','d','',7),(628,'2025-04-14','11:00:00.000000','20:00:00.000000','c','',3),(629,'2025-04-15','11:00:00.000000','20:00:00.000000','c','',4),(630,'2025-04-16','11:00:00.000000','20:00:00.000000','c','',4),(631,'2025-04-17','11:00:00.000000','20:00:00.000000','c','',4),(632,'2025-04-18','11:00:00.000000','20:00:00.000000','c','',4),(633,'2025-04-19','11:00:00.000000','20:00:00.000000','c','',7),(634,'2025-04-20','11:00:00.000000','20:00:00.000000','c','',7),(635,'2025-04-07','11:00:00.000000','20:00:00.000000','w','',3),(636,'2025-04-08','11:00:00.000000','20:00:00.000000','w','',3),(637,'2025-04-09','11:00:00.000000','20:00:00.000000','w','',3),(638,'2025-04-10','11:00:00.000000','20:00:00.000000','w','',4),(639,'2025-04-11','11:00:00.000000','20:00:00.000000','w','',4),(640,'2025-04-12','11:00:00.000000','20:00:00.000000','w','',4),(641,'2025-04-13','11:00:00.000000','20:00:00.000000','w','',4),(642,'2025-04-21','11:00:00.000000','20:00:00.000000','Done','',7),(643,'2025-04-22','11:00:00.000000','20:00:00.000000','Done','',7),(644,'2025-04-23','11:00:00.000000','20:00:00.000000','Done','',7),(645,'2025-04-24','11:00:00.000000','20:00:00.000000','Done','',7),(646,'2025-04-25','11:00:00.000000','20:00:00.000000','Done','',3),(647,'2025-04-26','11:00:00.000000','20:00:00.000000','Done','',7),(648,'2025-04-21','11:00:00.000000','20:00:00.000000','Done','',1),(649,'2025-04-21','11:00:00.000000','20:00:00.000000','von','',2),(650,'2025-04-26','11:00:00.000000','20:00:00.000000','done','',1),(651,'2025-04-26','11:00:00.000000','20:00:00.000000','Doen','',2),(652,'2025-04-26','11:00:00.000000','20:00:00.000000','completed within timeslot\r\n','',44),(653,'2025-04-21','11:00:00.000000','20:00:00.000000','Complete within given timeslot','',2),(654,'2025-04-21','11:00:00.000000','20:00:00.000000','Please give some more time','',2),(655,'2025-04-21','11:00:00.000000','20:00:00.000000','Please give some more time','',2),(656,'2025-04-21','11:00:00.000000','20:00:00.000000','o','',4),(657,'2025-04-21','11:00:00.000000','20:00:00.000000','o','',4),(658,'2025-04-21','11:00:00.000000','20:00:00.000000','n','',2),(659,'2025-04-21','11:00:00.000000','20:00:00.000000','n','',2),(660,'2025-04-26','11:00:00.000000','20:00:00.000000','completed within timeslot','',1),(661,'2025-04-28','11:00:00.000000','20:00:00.000000','Completed within  timeslot','',1),(662,'2025-04-29','11:00:00.000000','20:00:00.000000','Completwd within timeslot','',1),(663,'2025-04-30','11:00:00.000000','20:00:00.000000','Completed','',6),(664,'2025-04-30','11:00:00.000000','20:00:00.000000','I am unable to complete ','',1),(665,'2025-05-01','11:00:00.000000','20:00:00.000000','Completed within timeslot and uploaded on net','',1),(666,'2025-05-06','11:00:00.000000','20:00:00.000000','I was given the task of information gathering','',50),(667,'2025-05-05','11:00:00.000000','20:00:00.000000','task given on this day','',50),(668,'2025-05-06','11:00:00.000000','20:00:00.000000','started analysing the task','',50),(669,'2025-05-07','11:00:00.000000','20:00:00.000000','Scheduling the task','',50),(670,'2025-05-08','11:00:00.000000','20:00:00.000000','Working on task','',50),(671,'2025-05-09','11:00:00.000000','20:00:00.000000','Error found in the task','',50),(672,'2025-05-10','11:00:00.000000','20:00:00.000000','Under resolve','',50),(673,'2025-05-05','11:00:00.000000','20:00:00.000000','Completed within deadline','',40),(674,'2025-05-06','11:00:00.000000','20:00:00.000000','Completed within deadline','',43),(675,'2025-05-05','11:00:00.000000','20:00:00.000000','Monday','',40),(676,'2025-05-08','11:00:00.000000','20:00:00.000000','Testing','',1),(677,'2025-05-05','11:00:00.000000','20:00:00.000000','jnkjn','',1),(678,'2025-05-09','11:00:00.000000','20:00:00.000000','Completed within deadline','',1),(679,'2025-05-05','16:25:00.000000','17:26:00.000000','f','',40),(680,'2025-04-28','11:00:00.000000','20:00:00.000000','modified','',50),(681,'2025-04-29','11:00:00.000000','20:00:00.000000','gr','timesheet_files/mysql-installer-web-community-8.0.41.0.msi',50),(682,'2025-04-29','11:00:00.000000','20:00:00.000000','gr','timesheet_files/mysql-installer-web-community-8_thJUMey.0.41.0.msi',50),(683,'2025-04-29','11:00:00.000000','20:00:00.000000','gr','timesheet_files/mysql-installer-web-community-8_ehSyHfU.0.41.0.msi',50),(684,'2025-04-30','11:00:00.000000','20:00:00.000000','asc','',50),(685,'2025-04-30','11:00:00.000000','20:00:00.000000','asc','',50),(686,'2025-04-30','11:00:00.000000','20:00:00.000000','asc','',50),(687,'2025-04-30','11:00:00.000000','20:00:00.000000','asc','',50),(688,'2025-04-30','11:00:00.000000','20:00:00.000000','4regh','timesheet_files/Employee_Handbook_2024_1.pdf',50),(689,'2025-05-01','11:00:00.000000','20:00:00.000000','kl','timesheet_files/mysql-installer-web-community-8_9OTKQH5.0.41.0.msi',50),(690,'2025-05-12','11:00:00.000000','20:00:00.000000','ge','',50),(691,'2025-05-14','11:00:00.000000','20:00:00.000000','Completed within deadline','',50);
/*!40000 ALTER TABLE `timesheet_taskrecord` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-23 17:34:54
