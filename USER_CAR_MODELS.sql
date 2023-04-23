CREATE TABLE `USER_CAR_MODELS` (
  `EMAIL` varchar(30) NOT NULL,
  `CAR_MODEL` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `USER_CAR_MODELS` (`EMAIL`, `CAR_MODEL`) VALUES
('john.doe@example.com', 'X6'),
('sample@user.com', 'Civic'),
('sample@user.com', 'Corolla');
