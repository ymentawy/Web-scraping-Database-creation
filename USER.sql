CREATE TABLE `USER` (
  `EMAIL` varchar(50) NOT NULL,
  `USERNAME` varchar(30) NOT NULL,
  `GENDER` char(1) NOT NULL,
  `DOB` date NOT NULL,
  `USER_PHONE` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `USER` (`EMAIL`, `USERNAME`, `GENDER`, `DOB`, `USER_PHONE`) VALUES
('dummy@example.com', 'dummy', 'F', '1999-07-08', '01158426874'),
('john.doe@example.com', 'JohnDoe', 'M', '1990-01-01', '01123456789'),
('m7mad@yahoo.com', 'm7mad', 'M', '1987-06-24', '01236547895'),
('memo@gmail.com', 'memo', 'F', '1998-09-23', '01245698745'),
('sample@user.com', 'uname', 'M', '2000-08-25', '01114886846'),
('sample111@example.com', 'sample111', 'F', '2004-05-05', '01254789635'),
('tinker@yahoo.com', 'tee', 'F', '1987-06-27', '01547863254');
