import os
from flask_migrate import Migrate
from flask import session
from app import create_app, db
from app.models import User, Series, Movie, Category, UserMovie
from app.main.forms import SearchBarForm
from app.scripts.scan import Main
from flask_wtf.csrf import CsrfProtect
from config import Config

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
	return dict(db=db, user=User, series=Series, movie=Movie, category = Category, main = Main, usermovie=UserMovie)

@app.context_processor
def inject_forms():
    try:
        cur_user = User.query.filter_by(id=session['current_user']).first()
    except:
        cur_user = None
    return dict(sbform=SearchBarForm(), current_user=cur_user)


if __name__=='__main__':
    with app.app_context():
        Config.Save()
        db.create_all()
        if not Category.query.all():
            for cat in Category.data:
                db.session.add(Category(name=cat))
            db.session.commit()
        if not User.query.all():
            db.session.add(User(username='default', enabled=True))
            db.session.commit()
        app.run(host='0.0.0.0', debug=True)

