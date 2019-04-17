
USE weight;

INSERT INTO `transactions` (`id`, `datetime`, `direction`, `truck`, `containers`, `bruto`, `truckTara`, `neto`, `produce`) VALUES 
(10,now() - interval 1 day,'in','A10000','2002,2001,2000',5123,1200,3923,'oranges'),
(11,now() - interval 1 day,'out','A10000','2005,2004,2003',5124,1200,3924,'oranges'),
(12,now() - interval 2 day,'in','A10002','2007,2006,2005',5125,1200,3925,'pears'),
(13,now() - interval 2 day,'out','A10002','2010,2009,2008',5126,1200,3926,'pears'),
(14,now() - interval 2 day,'out','A10002','2012,2011,2010',5127,1200,3927,'pears'),
(15,now() - interval 3 day,'out','A10002','2014,2013,2012',5128,1200,3928,'lemons'),
(16,now() - interval 3 day,'in','A10005','2017,2016,2015',5129,1200,3929,'oranges'),
(17,now() - interval 4 day,'out','A10005','2022,2021,2020',5130,1200,3930,'oranges'),
(18,now() - interval 4 day,'in','A10007','2025,2024,2023',5131,1300,3831,'pears'),
(19,now() - interval 5 day,'out','A10007','2027,2026,2025',5132,1300,3832,'pears'),
(20,now() - interval 6 day,null,'A10009','2030,2029,2028',5133,1300,3833,'pears'),
(21,now() - interval 7 day,null,'A10010','2032,2031,2030',5134,1300,3834,'lemons'),
(22,now() - interval 15 day,'in','A10011','2034,2033,2032',5135,1300,3835,'oranges'),
(23,now() - interval 16 day,'out','A10011','2037,2036,2035',5136,1300,3836,'oranges'),
(24,now() - interval 18 day,'in',null,'2040,2039,2038',5137,1300,3837,'pears'),
(25,now() - interval 21 day,'out',null,'2043,2042,2041',5138,1300,3838,'pears'),
(26,now() - interval 22 day,'in','A10015','2046,2045,2044',5139,1300,3839,'pears'),
(27,now() - interval 27 day,'in','A10016','2049,2048,2047',5140,1300,3840,'lemons'),
(28,now() - interval 40 day,'out','A10016','2053,2052,2051',5141,1300,3841,'oranges');


INSERT INTO `containers_registered` (`container_id`, `weight`, `unit`) VALUES 
('C-35434',296,'kg'),
('C-73281',273,'kg'),
('C-35537',292,'kg'),
('K-8263',666,'lbs'),
('K-5269',666,'lbs'),
('K-7943',644,'lbs');

