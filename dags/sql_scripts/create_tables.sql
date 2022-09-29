CREATE TABLE IF NOT EXISTS integrated.listing
(
	listid int not null,
	sellerid int not null,
	eventid int not null,
	dateid smallint not null,
	numtickets smallint not null,
	priceperticket decimal(8,2) not null,
	totalprice decimal(8,2) not null,
	listtime timestamp not null
);

CREATE TABLE IF NOT EXISTS integrated.date
(
	dateid smallint not null,
	caldate date not null,
	day character(3) not null,
	week smallint not null,
	month character(5) not null,
	qtr character(5) not null,
	year smallint not null,
	holiday boolean not null default 0
);

CREATE TABLE IF NOT EXISTS integrated.sales
(
	salesid int not null,
	listid int not null,
	sellerid int not null,
	buyerid int not null,
	eventid int not null,
	dateid smallint not null,
	qtysold smallint not null,
	pricepaid decimal(8,2) not null,
	commission decimal(8,2) not null,
	saletime varchar(20) not null
);

CREATE TABLE integrated.users
(
	userid integer not null,
	username char(8),
	firstname varchar(30),
	lastname varchar(30),
	city varchar(30),
	state char(2),
	email varchar(100),
	phone char(14),
	likesports varchar(5),
	liketheatre varchar(5),
	likeconcerts varchar(5),
	likejazz varchar(5),
	likeclassical varchar(5),
	likeopera varchar(5),
	likerock varchar(5),
	likevegas varchar(5),
	likebroadway varchar(5),
	likemusicals varchar(5)
);

CREATE TABLE integrated.venue
(
	venueid smallint not null,
	venuename varchar(100),
	venuecity varchar(30),
	venuestate char(2),
	venueseats integer
);

CREATE TABLE integrated.category
(
	catid smallint not null,
	catgroup varchar(10),
	catname varchar(10),
	catdesc varchar(50)
);

CREATE TABLE integrated.event(
	eventid integer not null,
	venueid smallint not null,
	catid smallint not null,
	dateid smallint not null,
	eventname varchar(200),
	starttime timestamp
);