from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
from utils import create_salt, add_salt, check_passwd, seconds_to_human_time
from upvote import upvote, _upvote, get_upvoted

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zz:zz@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
CORS(app)
db = SQLAlchemy(app)

def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(20), unique=True, nullable=False)
    passwd = db.Column(db.String(70), unique=True, nullable=False)
    salt = db.Column(db.String(10), nullable=False)


@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify('Hello World from Flask!')


@app.route('/validateUser', methods=['POST'])
def validateUser():
    username = request.form.get('username')
    password = request.form.get('password')
    user = db.session.query(User).filter_by(uname=username).first()
    if not user:
        return jsonify({'msg': 'username error!'})
    is_valid_user = check_passwd(user, password)
    if is_valid_user is False:
        return jsonify({'msg': 'password error!'})
    return jsonify({'msg': 'success!'})

@app.route('/work', methods=['POST'])
def work():
    link = request.form.get('link')
    counts = request.form.get('counts')
    voted = get_upvoted(link)
    seconds = int(counts) - int(voted)
    msg = '完成投票需要时间：' + seconds_to_human_time(seconds)
    upvote(link, int(counts))
    return jsonify({'msg': msg})

@celery.task
def worker(link, counts):
    _upvote(link, counts)

# db.create_all()
# passwd = '4a60bf7d4bc1e485744cf7e8d0860524752fca1ce42331be7c439fd23043f151'
# salt = create_salt()
# passwd = add_salt(passwd, salt)
# zz = User(uname='zz', passwd=passwd, salt=salt)
# db.session.add(zz)
# db.session.commit()


if __name__ == '__main__':
    app.run()
