drop view vglyphoutline;
drop view vglyphoutlines;
drop view vgls;
drop view vglgroup;
create  view vglyphoutline as select v.id,v.glyphName,v.PointNr,v.x,v.y,v.contrp,p.PointName, ifnull(p.groupname,'') groupn, v.idmaster from glyphoutline v left join glyphparam p  on v.id=p.id and v.glyphName=p.glyphName and v.idmaster=p.idmaster;
create view vglyphoutlines as select v.id,p.idmaster,p.glyphName,PointNr,PointName,startp,doubledash,tripledash,leftp,rightp,downp,upp,dir,leftp2,rightp2,downp2,upp2,dir2,superright,superleft,tension,tensionand,cycle,penshifted,pointshifted,superness,penwidth,xHeight,cardinal,overx,overbase,overcap,stemcutter,stemshift,inktrap_l,inktrap_r from glyphoutline v left join glyphparam p on v.id=p.id and p.PointName>'' and v.glyphName=p.glyphName and v.idmaster=p.idmaster;
create view vgls as select v.id,p.idmaster,p.glyphName,PointNr,PointName,
ifnull(p.startp     ,(select g.startp      from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) startp     ,
ifnull(p.doubledash ,(select g.doubledash  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) doubledash ,
ifnull(p.tripledash ,(select g.tripledash  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) tripledash ,
ifnull(p.leftp      ,(select g.leftp       from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) leftp      ,
ifnull(p.rightp     ,(select g.rightp      from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) rightp     ,
ifnull(p.downp      ,(select g.downp       from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) downp      ,
ifnull(p.upp        ,(select g.upp         from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) upp        ,
ifnull(p.dir        ,(select g.dir         from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) dir        ,
ifnull(p.leftp2     ,(select g.leftp2      from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) leftp2     ,
ifnull(p.rightp2    ,(select g.rightp2     from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) rightp2    ,
ifnull(p.downp2     ,(select g.downp2      from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) downp2     ,
ifnull(p.upp2       ,(select g.upp2        from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) upp2       ,
ifnull(p.dir2       ,(select g.dir2        from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) dir2       ,
ifnull(p.superright ,(select g.superright  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) superright ,
ifnull(p.superleft  ,(select g.superleft   from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) superleft  ,
ifnull(p.tension    ,(select g.tension     from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) tension    ,
ifnull(p.tensionand ,(select g.tensionand  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) tensionand ,
ifnull(p.cycle      ,(select g.cycle       from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) cycle      ,
ifnull(p.penshifted ,(select g.penshifted  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) penshifted ,
ifnull(p.pointshifted ,(select g.pointshifted  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) pointshifted ,
ifnull(p.superness  ,(select g.superness   from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) superness  ,
ifnull(p.penwidth   ,(select g.penwidth    from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) penwidth   ,
ifnull(p.xHeight    ,(select g.xHeight     from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) xHeight    ,
ifnull(p.cardinal   ,(select g.cardinal    from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) cardinal   ,
ifnull(p.overx      ,(select g.overx       from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) overx      ,
ifnull(p.overbase   ,(select g.overbase    from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) overbase   ,
ifnull(p.overcap    ,(select g.overcap     from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) overcap    ,
ifnull(p.stemcutter ,(select g.stemcutter  from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) stemcutter ,
ifnull(p.stemshift  ,(select g.stemshift   from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) stemshift  ,
ifnull(p.inktrap_l  ,(select g.inktrap_l   from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) inktrap_l  ,
ifnull(p.inktrap_r  ,(select g.inktrap_r   from groupparam g where g.idmaster=v.idmaster and g.groupname=p.groupname)) inktrap_r  
from glyphoutline v left join glyphparam p on v.id=p.id and p.PointName>'' and v.glyphName=p.glyphName and v.idmaster=p.idmaster order by p.PointName;
create view vglgroup as select v.id,v.idmaster,v.glyphName,v.groupname,
p.startp,p.doubledash,p.tripledash,p.leftp,p.rightp,p.downp,p.upp,p.dir,p.leftp2,p.rightp2,p.downp2,p.upp2,p.dir2,p.superright,p.superleft,p.tension,p.tensionand,p.cycle,p.penshifted,p.pointshifted,p.superness,p.penwidth,p.xHeight,p.cardinal,p.overx,p.overbase,p.overcap,p.stemcutter,p.stemshift,p.inktrap_l,p.inktrap_r from glyphparam v , groupparam p where  p.groupname>'' and v.groupname=p.groupname and v.idmaster=p.idmaster;

