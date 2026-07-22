CREATE TABLE `users_ex3_8220210_2024_2025` (
  `username` varchar(45) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `users_ex3_8220210_2024_2025` (`username`,`firstname`,`lastname`,`email`,`password`) VALUES ('demo-user-1','Demo','User One','demo-user-1','demo-pass-1');
INSERT INTO `users_ex3_8220210_2024_2025` (`username`,`firstname`,`lastname`,`email`,`password`) VALUES ('demo-user-2','Demo','User Two','demo-user-2','demo-pass-2');
INSERT INTO `users_ex3_8220210_2024_2025` (`username`,`firstname`,`lastname`,`email`,`password`) VALUES ('demo-user-3','Demo','User Three','demo-user-3','demo-pass-3');
