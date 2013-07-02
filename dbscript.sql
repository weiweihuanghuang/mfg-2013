drop table glyph;
drop table glyphoutline;
drop table glyphparam;
drop table master;
drop table globalparam;

CREATE TABLE glyph (
    idglyph INT AUTO_INCREMENT,
    glyphName varchar(3),
    width integer,
    unicode TEXT,
    primary key (idglyph)
);
CREATE TABLE glyphoutline (
    id INT ,
    glyphName VARCHAR(3),
    PointNr VARCHAR(4),
    x integer,
    y integer, 
    contrp integer default 0,
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,id,glyphName)
);
CREATE TABLE glyphparam (
    id INT ,
    glyphName VARCHAR(3),
    PointName VARCHAR(5),
    startp INT,
    leftp   INT,
    rightp  INT,
    downp   INT,
    upp     INT,
    superqr INT,
    superleft INT,
    tension INT, 
    tensionend varchar(10),
    cycle     INT,
    penshiftedx varchar(7),
    penshiftedy varchar(7), 
    pointshiftx varchar(7),
    pointshifty varchar(7),
    superness INT, 
    penwidth float,
    xHeight  float,
    cardinal VARCHAR(10), 
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,id,glyphName)
);
CREATE TABLE master (
    idmaster INT AUTO_INCREMENT,
    FontName TEXT,
    FontNameA varchar(30),
    FontNameB varchar(30),
    idglobal INT, 
    vdate    TIMESTAMP default now(),
    primary key (idmaster)
);
CREATE TABLE globalparam (
    idglobal INT ,
    metapolation float,
    superness float,
    penwidth  float,
    unitwidth float,
    xHeight   float,
    tension   integer,
    fontsize  integer default 12,
    ht        integer default 10,
    primary key (idglobal)
);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My First Metapolator Font", "GaramondSans.ufo","GaramondSans.ufo",1);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My second Metapolator Font", "Aeriel-Regular.ufo","Aeriel-Regular.ufo",2);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("combined Garamond and Aeriel", "GaramondSans.ufo","Aeriel-Regular.ufo",2);
insert into globalparam (idglobal,metapolation,superness,penwidth,unitwidth,xHeight,fontsize,ht) Values (1, 0.5,1,1,1.0,1.0,12,10);
insert into globalparam (idglobal,metapolation,superness,penwidth,unitwidth,xHeight,fontsize,ht) Values (2, 0.5,1,700,1.0,1.0,15,8);

