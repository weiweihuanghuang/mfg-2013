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
    primary key (id,glyphName)
);
CREATE TABLE glyphparam (
    id INT ,
    glyphName VARCHAR(3),
    PointName VARCHAR(5),
    startp integer default 0,
    superness integer , 
    penwidth float,
    xHeight  float,
    cardinal VARCHAR(10), 
    idmaster INT,
    vdate    TIMESTAMP default now(),
    primary key (id,glyphName)
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
    Interpolation float,
    superness float,
    penwidth  float,
    unitwidth float,
    xHeight   float,
    primary key (idglobal)
);
insert into master (FontName,FontNameA,FontNameB,idglobal) Values ("My First Metapolator Font", "","",1);
insert into globalparam (idglobal,Interpolation,superness,penwidth,unitwidth,xHeight) Values (1, 0.5,1,1,1.0,1.0);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (1,'A','p1',20,0);
insert into glyphoutline (id,Glyphname,PointNr,x,y) Values (2,'A','p2',139,0);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (3,'A','p3',257,295);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (4,'A','p4',665,295);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (5,'A','p5',778,0);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (6,'A','p6',896,0);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (7,'A','p7',537,930);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (8,'A','p8',385,930);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (9,'A','p9',303,405);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (10,'A','p10',461,819);
insert into glyphoutline (id,GlyphName,PointNr,x,y) Values (11,'A','p11',618,405);

