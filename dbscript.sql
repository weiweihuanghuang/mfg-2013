drop table glyph;
drop table glyphoutline;
drop table glyphparam;
drop table master;
drop table globalparam;
drop table localparam;
drop table groupparam;

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
    groupname VARCHAR(10),
    startp INT,
    doubledash INT,
    tripledash INT,
    leftp   INT,
    rightp  INT,
    downp   INT,
    upp     INT,
    dir     varchar(30),
    leftp2   INT,
    rightp2  INT,
    downp2   INT,
    upp2     INT,
    dir2     varchar(30),
    superright float,
    superleft float,
    tension INT, 
    tensionand varchar(10),
    cycle     INT,
    penshifted varchar(30), 
    pointshifted varchar(30),
    superness INT, 
    penwidth float,
    xHeight  float,
    cardinal VARCHAR(10),
    overx VARCHAR(1), 
    overbase VARCHAR(1),  
    overcap VARCHAR(1), 
    stemcutter float,
    stemshift float,
    inktrap_l float,
    inktrap_r float,   
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,id,glyphName)
);
CREATE TABLE groupparam (
    groupname varchar(10), 
    startp INT,
    doubledash INT,
    tripledash INT,
    leftp   INT,
    rightp  INT,
    downp   INT,
    upp     INT,
    dir     varchar(30),
    leftp2   INT,
    rightp2  INT,
    downp2   INT,
    upp2     INT,
    dir2     float,
    superright float,
    superleft float,
    tension INT, 
    tensionand varchar(10),
    cycle     INT,
    penshifted varchar(30), 
    pointshifted varchar(30),
    superness INT, 
    penwidth float,
    xHeight  float,
    cardinal VARCHAR(10),
    overx VARCHAR(1), 
    overbase VARCHAR(1),  
    overcap VARCHAR(1), 
    stemcutter float,
    stemshift float,
    inktrap_l float,
    inktrap_r float,   
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (idmaster,groupname)
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
    maxstemcut float default 0.0,
    over      float default 0,
    primary key (idglobal)
);
CREATE TABLE localparam (
    idlocal INT ,
    px        float default 0.1,
    mean      float default 5.0,
    des       float default 2.0,
    ascl       float default 0.8,
    cap       float default 0.8,
    width  float default 1,
    xheight   float default 1,
    capital   float default 1,
    ascender   integer default 1,
    descender  integer default 1,
    inktrap    integer default 10,
    stemcut   integer default 20,
    skeleton  float default 0.0,
    superness float default 1.0,
    primary key (idlocal)
);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My First Metapolator Font", "GaramondSansA.ufo","GaramondSansB.ufo",1);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My second Metapolator Font", "Aeriel-Regular.ufo","Aeriel-Regular.ufo",2);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("combined Garamond and Aeriel", "GaramondSans.ufo","Aeriel-Regular.ufo",2);
insert into globalparam (idglobal,metapolation,superness,penwidth,unitwidth,xHeight,fontsize,ht,maxstemcut,over) Values (1, 0.5,1,1,1.0,1.0,12,10,0,0);
insert into globalparam (idglobal,metapolation,superness,penwidth,unitwidth,xHeight,fontsize,ht,maxstemcut,over) Values (2, 0.5,1,700,1.0,1.0,15,8,0,0);
insert into localparam (idlocal) values (1);
insert into localparam (idlocal) values (2);
insert into localparam (idlocal) values (3);
insert into localparam (idlocal) values (4);
insert into localparam (idlocal) values (5);
insert into localparam (idlocal) values (6);
insert into localparam (idlocal) values (7);
insert into localparam (idlocal) values (8);
insert into localparam (idlocal) values (9);
insert into localparam (idlocal) values (10);
