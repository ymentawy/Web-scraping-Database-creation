CREATE TABLE `USER_CAR_MAKES` (
  `EMAIL` varchar(30) NOT NULL,
  `CAR_MAKE` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `USER_CAR_MAKES` (`EMAIL`, `CAR_MAKE`) VALUES
('john.doe@example.com', 'BMW'),
('sample@user.com', 'Honda'),
('sample@user.com', 'Toyota');
