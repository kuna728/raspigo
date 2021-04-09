import os, sys
from .. import db
from ..models import Movie, Series, Category, Seasons, UserMovie, UserSeries
from googlesearch import search
from datetime import datetime
from .scrap import GetInfo
from .googleImg import DownloadImg
from flask import current_app



def Main():
    log = []
    log.append(Insert('m'))
    log.append(Insert('s'))
    return log


def Insert(contentType):
    added = []; deleted = []
    app_dir = os.getcwd()
    if contentType=='m':
        Handler = Movie
        os.chdir(current_app.config['MEDIA_FOLDER']+'/movies')
    elif contentType=='s':
        Handler = Series
        os.chdir(current_app.config['MEDIA_FOLDER']+'/series')
    else:
        raise AttributeError('Allowed args: "s", "m"')
    ls = os.listdir()
    for con in ls:
        if(not Handler.query.filter_by(title=con).first() and con!='example'):
            links = [search(con+ 'imdb'), search(con+' filmweb')]
            single_links = []
            for link in links:
                if type(link) is list:
                    single_links.append(link[0])
                else:
                    single_links.append(next(link))
            infos = GetInfo(fwlink=single_links[1], imdblink=single_links[0])
            cn = Handler(title=con, added=datetime.now(), IMDBmark=infos[0],FWlink=single_links[1], IMDBlink=single_links[0], FWmark=infos[1], year=infos[3], description=infos[4])
            if type(infos[2]) is list:
                for x in infos[2]:
                    cat = Category.query.filter_by(name=x).first()
                    if cat:
                        cn.cats.append(cat)
            else:
                cat = Category.query.filter_by(name=infos[2]).first()
                if cat:
                    cn.cats.append(cat)
            db.session.add(cn)
            added.append(con)
            if contentType=='s':
                seriesId = Series.query.filter_by(title=con).first().id
                os.chdir(con)
                iterator = 1
                for el in os.listdir():
                    if os.path.isdir(el):
                        season = Seasons(series_id=seriesId, season=iterator, episodes=len(os.listdir(el)))
                        iterator +=1    
                        db.session.add(season)
                os.chdir('..')
                

    for con in Handler.query.all():
        if not con.title in ls:
            deleted.append(con.title)
            Handler.query.filter_by(id=con.id).delete()
        if Handler==Movie:
            UserMovie.query.filter_by(movie_id=con.id).delete()
        else:
            UserSeries.query.filter_by(seasons_id=con.id).delete() 
    db.session.commit()
    if len(added):
        constTag = (' serial' if contentType=='s' else ' film')
        DownloadImg(tags=added, constTag=constTag, dir=os.getcwd())
    
    os.chdir(app_dir)

    return added, deleted



if __name__=="__main__":
    Main()



    