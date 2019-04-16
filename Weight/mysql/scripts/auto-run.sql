--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` varchar(14) DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),

USE weight;

INSERT INTO `transactions` (`id`, `datetime`, `direction`, `truck`, `containers`, `bruto`, `truckTara`, `neto`, `produce`) VALUES 
(10,'2019010101000','in','A10000','2002,2001,2000',5123,1200,3923,'oranges'),
(11,'2019010101100','out','A10000','2005,2004,2003',5124,1200,3924,'oranges'),
(12,'2019010101200','in','A10002','2007,2006,2005',5125,1200,3925,'pears'),
(13,'2019010101300','out','A10002','2010,2009,2008',5126,1200,3926,'pears'),
(14,'2019010101400','out','A10002','2012,2011,2010',5127,1200,3927,'pears'),
(15,'2019010101500','out','A10002','2014,2013,2012',5128,1200,3928,'lemons'),
(16,'2019010101600','in','A10005','2017,2016,2015',5129,1200,3929,'oranges'),
(17,'2019010101700','out','A10005','2022,2021,2020',5130,1200,3930,'oranges'),
(18,'2019010101800','in','A10007','2025,2024,2023',5131,1300,3831,'pears'),
(19,'2019010101900','out','A10007','2027,2026,2025',5132,1300,3832,'pears'),
(20,'2019010102000',null,'A10009','2030,2029,2028',5133,1300,3833,'pears'),
(21,'2019010102100',null,'A10010','2032,2031,2030',5134,1300,3834,'lemons'),
(22,'2019010102200','in','A10011','2034,2033,2032',5135,1300,3835,'oranges'),
(23,'2019010102300','out','A10011','2037,2036,2035',5136,1300,3836,'oranges'),
(24,'2019010102400','in',null,'2040,2039,2038',5137,1300,3837,'pears'),
(25,'2019010102500','out',null,'2043,2042,2041',5138,1300,3838,'pears'),
(26,'2019010102600','in','A10015','2046,2045,2044',5139,1300,3839,'pears'),
(27,'2019010102700','in','A10016','2049,2048,2047',5140,1300,3840,'lemons'),
(28,'2019010102800','out','A10016','2053,2052,2051',5141,1300,3841,'oranges');


INSERT INTO `containers_registered` (`container_id`, `weight`, `unit`) VALUES 
('C-35434',296,'kg'),
('C-73281',273,'kg'),
('C-35537',292,'kg'),
('K-8263',666,'lbs'),
('K-5269',666,'lbs'),
('K-7943',644,'lbs');

