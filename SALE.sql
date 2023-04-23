CREATE TABLE `SALE` (
  `SALE_ID` int NOT NULL,
  `USER_EMAIL` varchar(30) NOT NULL,
  `SELLER_NAME` varchar(100) NOT NULL,
  `CAR_ID` int DEFAULT NULL,
  `RATING` int DEFAULT NULL
) ;

INSERT INTO `SALE` (`SALE_ID`, `USER_EMAIL`, `SELLER_NAME`, `CAR_ID`, `RATING`) VALUES
(1, 'sample@user.com', 'Seif', 195976890, 4),
(2, 'dummy@example.com', 'احمد', 196576395, 2),
(3, 'tinker@yahoo.com', 'tamer', 196722888, 4),
(4, 'memo@gmail.com', 'Mahmoud El Wrdany', 196715613, 5);
