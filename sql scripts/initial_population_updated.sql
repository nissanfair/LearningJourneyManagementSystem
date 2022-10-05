DROP DATABASE IF EXISTS `ljms`;
CREATE DATABASE IF NOT EXISTS `ljms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ljms`;



CREATE TABLE `role` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(20) NOT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `staff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `staff_fname` varchar(50) NOT NULL,
  `staff_lname` varchar(50) NOT NULL,
  `dept` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `role` int DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `role` (`role`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`role`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `course` (
  `course_id` varchar(20) NOT NULL,
  `course_name` varchar(50) NOT NULL,
  `course_desc` varchar(255) DEFAULT NULL,
  `course_status` varchar(15) DEFAULT NULL,
  `course_type` varchar(10) DEFAULT NULL,
  `course_category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `registration` (
  `reg_id` int NOT NULL AUTO_INCREMENT,
  `reg_status` varchar(20) NOT NULL,
  `completion_status` varchar(20) NOT NULL,
  `course_id` varchar(20) DEFAULT NULL,
  `staff_id` int DEFAULT NULL,
  PRIMARY KEY (`reg_id`),
  KEY `course_id` (`course_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `registration_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `registration_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `jobrole` (
`jobrole_id` int NOT NULL AUTO_INCREMENT,
`jobrole_name` varchar(255) NOT NULL,
PRIMARY KEY (`jobrole_id`),
KEY `jobrole_name` (`jobrole_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE `skill` (
`skill_id` int NOT NULL auto_increment,
`skill_name` varchar(255) NOT NULL,
`skill_desc` varchar(255) DEFAULT NULL,
PRIMARY KEY (`skill_id`),
KEY `skill_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE `learningjourney` (
`lj_id` int NOT NULL,
`lj_name` varchar(40) NOT NULL,
PRIMARY KEY (`lj_id`),
KEY `lj_name` (`lj_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `roleskill` (
`rsid` int NOT NULL AUTO_INCREMENT,
`jobrole_id` int NOT NULL,
`skill_id` int NOT NULL,
PRIMARY KEY (`rsid`),
CONSTRAINT `roleskills_ibfk` FOREIGN KEY (`jobrole_id`) REFERENCES `jobrole` (`jobrole_id`),
CONSTRAINT `roleskills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`skill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `courseskill` (
`csid` int NOT NULL,
`course_id` varchar(20) NOT NULL,
`skill_id` int NOT NULL,
PRIMARY KEY (`csid`),
CONSTRAINT `courseskills_ibfk` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
CONSTRAINT `courseskills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`skill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `learningjourneycourse` (
`ljc_id` int NOT NULL,
`lj_id` int NOT NULL,
`course_id` varchar(20) NOT NULL,
PRIMARY KEY (`ljc_id`),
CONSTRAINT `learningjourneycourse_ibfk` FOREIGN KEY (`lj_id`) REFERENCES `learningjourney` (`lj_id`),
CONSTRAINT `learningjourneycourse_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

INSERT INTO `Role` (`Role_ID`, `Role_Name`) VALUES
(1, 'Admin');

INSERT INTO `Staff` (`Staff_ID`, `Staff_FName`, `Staff_LName`, `Dept`, `Email`, `Role`) VALUES
(1, 'Apple', 'Tan', 'HR', 'apple.tan.hr@spm.com', 1);

INSERT INTO `Course` (`Course_ID`, `Course_Name`, `Course_Desc`, `Course_Status`, `Course_Type`, `Course_Category`) VALUES
('IS111', 'Introduction to Programming', 'Introductory Python module', 'Active', 'Internal', 'Technical');

INSERT INTO `Registration` (`Reg_ID`, `Course_ID`, `Staff_ID`, `Reg_Status`, `Completion_Status`) VALUES
(1, 'IS111', 1, 'Registered', 'Completed');

INSERT INTO `jobrole` (`jobrole_id`, `jobrole_name`) VALUES
(1, 'Data Analyst');

INSERT INTO `skill` (`skill_id`, `skill_name`, `skill_desc`) VALUES
(1, 'Data structures', 'Ability to use data structures such as lists, dictionaries, sets, and tuples to store and manipulate data');

INSERT INTO `learningjourney` (`lj_id`, `lj_name`) VALUES
(1, 'LJ to be swe');

INSERT INTO `roleskill` (`rsid`, `jobrole_id`,`skill_id`) VALUES
(1, 1, 1);

INSERT INTO `courseskill` (`csid`, `course_id`,`skill_id`) VALUES
(1, 'IS111', 1);

INSERT INTO `learningjourneycourse` (`ljc_id`, `lj_id`,`course_id`) VALUES
(1, 1, 'IS111');



SELECT * from staff;
SELECT * from Role;
SELECT * from course;
SELECT * from registration;
SELECT * from jobrole;
SELECT * from learningjourney;
SELECT * from skill;
SELECT * from roleskill;
SELECT * from courseskill;
SELECT * from learningjourneycourse;



