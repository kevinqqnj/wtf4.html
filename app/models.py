# -*- coding: utf-8 -*-
# 17197602@qq.com

from datetime import datetime, timedelta
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager
import requests, os, re, random, time, sys, traceback
from bs4 import BeautifulSoup

from threading import Thread
def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		threads.append(thr)
		thr.start()
	return wrapper

threads = []	# 多线程池，用来 join	
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.0 Chrome/30.0.1599.101 Safari/537.36'}

class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), primary_key=True, nullable=False)

    @staticmethod
    def clear_A():
        for a in Alembic.query.all():
            print a.version_num
            db.session.delete(a)
        db.session.commit()
        print '======== data in Table: Alembic cleared!'


class Bbs(db.Model):
    __tablename__ = 'bbs' #ָ������
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    page = db.Column(db.Integer)
    floor = db.Column(db.String, unique=True)
    master = db.Column(db.String)
    original = db.Column(db.String)
    reply = db.Column(db.String)
    comments = db.Column(db.String)
    lz_reply = db.Column(db.Boolean)
    test = db.Column(db.Boolean)
    test2 = db.Column(db.Boolean)
    test3 = db.Column(db.Boolean)


class Ty556242(db.Model):
    __tablename__ = 'ty556242'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, unique=True)
    floors = db.Column(db.String)
    last_update = db.Column(db.DateTime())
    lz_update = db.Column(db.DateTime())
    type = 'develop'	# db.Column(db.String)
    author = u'66端午88'	#
    title = u'房地产投资依然无忧，逆向思维让你找到真实'

    articleId = __tablename__[2:]

    def to_json(self):
        json_log = self.__dict__.copy()
        last_access = json_log['last_update']
        floors = (json_log['floors'].replace('datetime.datetime', 'datetime') )    # 数据库日期，建议用 float: time.time()
        # floors = img_url_convert(floors0)
        # if floors0<>floors : print floors
        json_log['last_update'] = str(last_access)[:19]
        json_log['lz_update'] = str(last_access)[:19]
        floors_dic = eval(floors)
        for k, v in floors_dic.items():
            floors_dic[k]['master'] = img_url_convert(v['master'])
            floors_dic[k]['original'] = img_url_convert(v['original'])
            floors_dic[k]['reply'] = img_url_convert(v['reply'])
        json_log['floorsJSON'] = floors_dic	#.sort(key = lambda x:x["time"])    # string to JSON object
#        json_log['floorsJSON'] = sorted(raw.iteritems(), key=lambda d:d[0], reverse = False) 	# 对字典按键（key）排序，再dict
        json_log.pop('floors')      # 不需要重复返回 floors (string)
        json_log.pop('_sa_instance_state')
        return json_log

    @staticmethod
    def fetch_new_articles():
        AUTHOR = u'66端午88'
        Article = Ty556242
        articleId = '556242'
        type = 'develop'
        urlsession = requests.Session()
        lastpost = Article.query.order_by(Article.page.desc()).first()
        if lastpost: # and lastpost.page>1: #如果已经有数据
            previous_page = lastpost.page
            # db.session.delete(lastpost)	# 清空最后一page
            # db.session.commit()
            print '====== current last page:', previous_page
            # print '====== now last page is:', Ty556242.query.order_by(Ty556242.page.desc()).first().page
            url = 'http://bbs.tianya.cn/post-%s-%s-1.shtml'% (type, articleId)  # #ty_vip_look[21035714]'
            r = urlsession.get(url, headers=user_agent)
            soup = BeautifulSoup(r.text, "html.parser")
            maxpage = int( soup.select('div.atl-pages > form > a')[-2].text )
            print 'start to fetch bbs from page %d to %d ...' % (previous_page, maxpage)

            for pg in range(previous_page, maxpage+1):
                page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
                if page_content == 'nok':
                    return 'nok'
                if page_content:
                    [page, floors, last_update, lz_update] = page_content
                    # print pg, lz_update
                    if floors<>'{}':
                        p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update )
                        if page==previous_page:
                            db.session.query(Article).filter(Article.page==page).update({
                                Article.floors: floors,
                                Article.last_update: last_update,
                                Article.lz_update: lz_update
                            })
                            print '====== previous last page updated!'
                        else: db.session.add(p)
                        db.session.commit()
                        print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
                else: print '======= No update. Author not found in this page:', pg
            print '====================== Done'
            return 'ok'
        else:
            print "============ empty table, will add first page..."
            # for pg in range(1, 2):
            pg = 1
            page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
            if page_content=='nok': return 'nok'
            [page, floors, last_update, lz_update] = page_content
            print pg, lz_update
            if floors <> '{}':
                p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update)
                db.session.add(p)
                db.session.commit()
                print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
            print '====================== Done'
            return 'ok'

class Ty5439941(db.Model):
    __tablename__ = 'ty5439941'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, unique=True)
    floors = db.Column(db.String)
    last_update = db.Column(db.DateTime())
    lz_update = db.Column(db.DateTime())
    type = 'free'	# db.Column(db.String)
    author = u'无名寒士'	# 
    title = u'宝钗比黛玉大八岁！重解红楼全部诗词！血泪文字逐段解释！所有谜团完整公开！'

    articleId = __tablename__[2:]
    def to_json(self):
        json_log = self.__dict__.copy()
        last_access = json_log['last_update']
        floors = json_log['floors'].replace('datetime.datetime', 'datetime')    # 数据库日期，建议用 float: time.time()
        # print last_access
        json_log['last_update'] = str(last_access )[:19]
        floors_dic = eval(floors)
        for k, v in floors_dic.items():
            floors_dic[k]['master'] = img_url_convert(v['master'])
            floors_dic[k]['original'] = img_url_convert(v['original'])
            floors_dic[k]['reply'] = img_url_convert(v['reply'])
        json_log['floorsJSON'] = floors_dic	#.sort(key = lambda x:x["time"])    # string to JSON object
        json_log.pop('floors')      # 不需要重复返回 floors (string)
        json_log.pop('_sa_instance_state')
        return json_log

    @staticmethod
    def fetch_new_articles():
        AUTHOR = u'无名寒士'
        Article = Ty5439941
        articleId = '5439941'
        type = 'free'
        urlsession = requests.Session()
        lastpost = Article.query.order_by(Article.page.desc()).first()
        if lastpost: # and lastpost.page>1: #如果已经有数据
            previous_page = lastpost.page
            # db.session.delete(lastpost)	# 清空最后一page
            # db.session.commit()
            print '====== current last page:', previous_page
            # print '====== now last page is:', Ty556242.query.order_by(Ty556242.page.desc()).first().page
            url = 'http://bbs.tianya.cn/post-%s-%s-1.shtml'% (type, articleId)  # #ty_vip_look[21035714]'
            r = urlsession.get(url, headers=user_agent)
            soup = BeautifulSoup(r.text, "html.parser")
            maxpage = int( soup.select('div.atl-pages > form > a')[-2].text )
            print 'start to fetch bbs from page %d to %d ...' % (previous_page, maxpage)

            for pg in range(previous_page, maxpage+1):
                page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
                if page_content == 'nok':
                    return 'nok'
                if page_content:
                    [page, floors, last_update, lz_update] = page_content
                    # print pg, lz_update
                    if floors<>'{}':
                        p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update )
                        if page==previous_page:
                            db.session.query(Article).filter(Article.page==page).update({
                                Article.floors: floors,
                                Article.last_update: last_update,
                                Article.lz_update: lz_update
                            })
                            print '====== previous last page updated!'
                        else: db.session.add(p)
                        db.session.commit()
                        print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
                else: print '======= No update. Author not found in this page:', pg
            print '====================== Done'
            return 'ok'
        else:
            print "============ empty table, will add first page..."
            # for pg in range(1, 2):
            pg = 1
            page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
            if page_content=='nok': return 'nok'
            [page, floors, last_update, lz_update] = page_content
            print pg, lz_update
            if floors <> '{}':
                p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update)
                db.session.add(p)
                db.session.commit()
                print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
            print '====================== Done'
            return 'ok'

class Ty1309480(db.Model):
    __tablename__ = 'ty1309480'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, unique=True)
    floors = db.Column(db.String)
    last_update = db.Column(db.DateTime())
    lz_update = db.Column(db.DateTime())
    type = 'develop'	# db.Column(db.String)
    author = u'第三元'	#
    title = u'2013~2017的大框架'

    articleId = __tablename__[2:]

    def to_json(self):
        json_log = self.__dict__.copy()
        last_access = json_log['last_update']
        floors = json_log['floors'].replace('datetime.datetime', 'datetime')    # 数据库日期，建议用 float: time.time()
        # print last_access
        json_log['last_update'] = str(last_access )[:19]
        floors_dic = eval(floors)
        for k, v in floors_dic.items():
            floors_dic[k]['master'] = img_url_convert(v['master'])
            floors_dic[k]['original'] = img_url_convert(v['original'])
            floors_dic[k]['reply'] = img_url_convert(v['reply'])
        json_log['floorsJSON'] = floors_dic	#.sort(key = lambda x:x["time"])    # string to JSON object
        json_log.pop('floors')      # 不需要重复返回 floors (string)
        json_log.pop('_sa_instance_state')
        return json_log


    @staticmethod
    def fetch_new_articles():
        AUTHOR = u'第三元'
        Article = Ty1309480
        articleId = '1309480'
        type = 'develop'
        urlsession = requests.Session()
        lastpost = Article.query.order_by(Article.page.desc()).first()
        if lastpost: # and lastpost.page>1: #如果已经有数据
            previous_page = lastpost.page
            # db.session.delete(lastpost)	# 清空最后一page
            # db.session.commit()
            print '====== current last page:', previous_page
            # print '====== now last page is:', Ty556242.query.order_by(Ty556242.page.desc()).first().page
            url = 'http://bbs.tianya.cn/post-%s-%s-1.shtml'% (type, articleId)  # #ty_vip_look[21035714]'
            r = urlsession.get(url, headers=user_agent)
            soup = BeautifulSoup(r.text, "html.parser")
            maxpage = int( soup.select('div.atl-pages > form > a')[-2].text )
            print 'start to fetch bbs from page %d to %d ...' % (previous_page, maxpage)

            for pg in range(previous_page, maxpage+1):
                page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
                if page_content == 'nok':
                    return 'nok'
                if page_content:
                    [page, floors, last_update, lz_update] = page_content
                    # print pg, lz_update
                    if floors<>'{}':
                        p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update )
                        if page==previous_page:
                            db.session.query(Article).filter(Article.page==page).update({
                                Article.floors: floors,
                                Article.last_update: last_update,
                                Article.lz_update: lz_update
                            })
                            print '====== previous last page updated!'
                        else: db.session.add(p)
                        db.session.commit()
                        print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
                else: print '======= No update. Author not found in this page:', pg
            print '====================== Done'
            return 'ok'
        else:
            print "============ empty table, will add first page..."
            # for pg in range(1, 2):
            pg = 1
            page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
            if page_content=='nok': return 'nok'
            [page, floors, last_update, lz_update] = page_content
            print pg, lz_update
            if floors <> '{}':
                p = Article(page=page, floors=floors, last_update=last_update, lz_update=lz_update)
                db.session.add(p)
                db.session.commit()
                print '====== now last page is:', Article.query.order_by(Article.page.desc()).first().page
            print '====================== Done'
            return 'ok'

class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String)
    host = db.Column(db.String)
    referer = db.Column(db.String)
    user_agent = db.Column(db.String)
    last_access = db.Column(db.DateTime())
    name = db.Column(db.String)
    email = db.Column(db.String)
    comment = db.Column(db.String)
    ip_location = db.Column(db.String)
    last_update = db.Column(db.DateTime())


    def to_json(self):
        json_log = self.__dict__.copy()
        last_access = json_log['last_access']
        # print last_access
        json_log['last_access'] = str(last_access)[:19]
        json_log.pop('_sa_instance_state')
        return json_log

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        self.followed.append(Follow(followed=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


db.event.listen(Comment.body, 'set', Comment.on_changed_body)

#@async
def bbs_search2(page, urlsession, AUTHOR, articleId, type):
    DEBUG = False
    url = 'http://bbs.tianya.cn/post-%s-%s-%d.shtml'% (type, articleId, page)  # #ty_vip_look[21035714]'
    print '============= Page:', page
    r = urlsession.get(url, headers=user_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    eles = soup.select('div.atl-item')
    try:
        floors = {}
        if page==1:
            floor = {}
            timestamp = soup.select('div.atl-info')[0].select('span')[1].text.strip()[-19:] # <span>时间：2011-01-29 22:31:00 </span>
            timestamp = datetime.strptime(timestamp, u"%Y-%m-%d %H:%M:%S") + timedelta(hours=-8)
            floor['timestamp'] = timestamp
            master = soup.select('div.bbs-content')[0].text.strip().replace(u'      ', '<br/>')
            floor['master'] = master
            floor['original'] = ''
            floor['reply'] = ''
            floor['comments'] = {}
            floor['lz_reply'] = False
            floors[0] = floor
            print 0, timestamp, '0 floor'

        for i in eles :
            if i['_host'] == AUTHOR:
                floor = {}
                replyid = i['replyid']
                original, reply, master, lz_reply = ('', '', '', False)
                #			timestamp = i['js_restime']
                timestamp = datetime.strptime( i['js_restime'], "%Y-%m-%d %H:%M:%S")+ timedelta(hours=-8) # 中国时区转换为UTC
                lz_update=timestamp
                #content = i.select('div.bbs-content')[0]
                content_raw = str(i.select('div.bbs-content')[0])[25:-6].strip().decode('utf8')
                content = i.select('div.bbs-content')[0].text.strip()
                floor_id = int( i.select('div.atl-reply > span')[0].text[:-1] ) # 多少楼
                if DEBUG: print eles.index(i), timestamp, floor_id, 'floor'
                rawstr = u"(.*)(<br/?>　　[-]{15,99}<br/?>)(.*)"		# 匹配 <br/>　　-------------<br/>
                rawstr2 = u"(.*)(<br/?>　　[—]{15,99}<br/?>)(.*)"		# 匹配: u'<br/>　　—————————————————<br/>'
                match_obj = re.search(rawstr, content_raw)
                match_obj2 = re.search(rawstr2, content_raw)
                if match_obj and (content[0]=='@' or  content[:3]==u'作者：' ) :	# 回帖
                    original = match_obj.group(1)
                    splitline = match_obj.group(2)
                    reply = match_obj.group(3)
                    if DEBUG: print u'【原帖】', original
                elif match_obj2 and (content[0]=='@' or  content[:3]==u'作者：' ) :	# 回帖
                    original = match_obj2.group(1)
                    splitline = match_obj2.group(2)
                    reply = match_obj2.group(3)
                    if DEBUG: print u'【原帖】', original
                else:
                    if DEBUG: print u'[M]', content
                    master = content_raw.replace(u'<br/>　　<br/>　　', '<br/>')#.replace(u'　　 ', '<br/>')
                floor['timestamp']=timestamp
                floor['master']=master
                floor['original']=original
                floor['reply']=reply
                floor['comments']= {}
                cmt_ele = i.select('div.ir-list > ul > li')
                commentlist = []
                cmt_id = 0
                for cc in cmt_ele:
                    tt = cc['_replytime']
                    if cc['_username'] == AUTHOR:
                        lz_reply = True
                        lz_update = datetime.strptime( tt, "%Y-%m-%d %H:%M:%S")+ timedelta(hours=-8)
                    #						commentlist.append( cc['_username'] + '>>>>'+ cc['_replytime'] + '>>>>' + cc.select('span.ir-content')[0].text)
                    author = cc['_username']
                    comment = cc.select('span.ir-content')[0].text
                    floor['comments'][cmt_id] = {'timestamp': tt, 'author': author, 'comment': comment}
                    cmt_id += 1
                    if DEBUG: print '[CMT]', cmt_id, author

                try: cmt_page = int( soup.select('div.atl-item')[1].select('span.ir-pageNums > a')[-1]['page'] )	# 评论页数
                except: cmt_page = 0

                for ccc in range(2, cmt_page+1):
                    if DEBUG: print u'有多页评论', cmt_page
                    url = 'http://bbs.tianya.cn/api?method=bbs.api.getCommentList&params.item=%s&params.articleId=%s&params.replyId=%s&params.pageNum=%d' % (type, articleId, replyid, ccc)
                    resp = urlsession.get(url, headers=user_agent).text
                    if eval(resp)['success'] == '1':
                        for cccc in eval(resp)['data']:
                            #							commentlist.append(cccc['author_name'].decode('utf8') + '>>>>' + cccc['comment_time'] + '>>>>' + cccc['content'].decode('utf8'))
                            tt = cccc['comment_time']
                            author = cccc['author_name'].decode('utf8')
                            comment = cccc['content'].decode('utf8')
                            floor['comments'][cmt_id] = {'timestamp': tt, 'author': author, 'comment': comment}
                            cmt_id += 1
                            if DEBUG: print '[CMT]', cmt_id, author

                floor['lz_reply']=lz_reply
                floors[floor_id] = floor

        last_update = datetime.utcnow()
        #		print [page, floors, last_update, lz_update]
        if floors<>{}:
            return [page, str(floors), last_update, lz_update]
        else: return []

    except:
        print traceback.print_exc()
        return 'nok'

def img_url_convert(article):
    url_prefix = '<img src="http://www.beihaiw.com/pic.php?url='
    regx = u'(.*)(<img original=")(http://.*)" src="(http://static.*)"/>(.*)'
    match_obj = re.search(regx, article)
    if match_obj :	# 回帖
    #			print p.master
    #			url = match_obj.group(3)
    #			print 'url:', url
        new_url = '%s%s">' % (url_prefix, match_obj.group(3))
    #			print new_url
        return match_obj.group(1) + new_url + match_obj.group(5)
    else: return article

