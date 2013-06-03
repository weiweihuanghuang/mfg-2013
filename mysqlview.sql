drop view vglyphoutline;
create  view vglyphoutline as select v.id,v.glyphName,v.PointNr,v.x,v.y,v.contrp,p.PointName from glyphoutline v left join glyphparam p  on v.id=p.id and v.glyphName=p.glyphName;


