
drop table users;
create table users
	(id integer not null,
	 user_name varchar(100) not null unique,
	 e_mail varchar(255) not null,
	 nickname varchar(100) not null,
	 password varchar(8) not null,
	 type varchar(8) not null,
	 created_on date,
	 primary key (id));

DROP TABLE p_categories;
CREATE TABLE `p_categories` (
  `Id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `category_name` (`category_name`)
);

DROP TABLE products;
CREATE TABLE `products` (
  `Id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_on` date DEFAULT NULL,
  product_image varchar(100),
  `want_count` INTEGER NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `product_name` (`product_name`)
);

DROP TABLE classification; 
CREATE TABLE `classification` (
  `Id` int(11) NOT NULL,
  `product_Id` int(11) NOT NULL,
  `category_Id` int(11) NOT NULL,
  PRIMARY KEY (`Id`)
);

DROP TABLE shopper;
CREATE TABLE `shopper` (
  `user_Id` int(11) NOT NULL,
  `category_Id` int(11) NOT NULL,
  `product_Id` int(11) NOT NULL
);


DROP TABLE user_products;
CREATE TABLE `user_products` (
  `Id` int(11) NOT NULL,
  `User_Id` int(11) NOT NULL,
  `product_Id` int(11) NOT NULL,
  `Comments` varchar(255),
  `Price` int(11),
  `Quantity` int(4),
  `Want` varchar(3) NOT NULL DEFAULT 'No'
);


