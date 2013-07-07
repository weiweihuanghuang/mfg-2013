drop view vglyphoutline;
drop view vglyphoutlines;
create  view vglyphoutline as select v.id,v.glyphName,v.PointNr,v.x,v.y,v.contrp,p.PointName, v.idmaster from glyphoutline v left join glyphparam p  on v.id=p.id and v.glyphName=p.glyphName and v.idmaster=p.idmaster;
create view vglyphoutlines as select v.id,p.idmaster,p.glyphName,PointNr,PointName,startp,leftp,rightp,downp,upp,superqr,superleft,tension,tensionend,cycle,penshiftedx,penshiftedy,pointshiftx,pointshifty,superness,penwidth,xHeight,cardinal from glyphoutline v left join glyphparam p on v.id=p.id and p.PointName>'' and v.glyphName=p.glyphName and v.idmaster=p.idmaster;
