import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# from pprint import pprint
import json,itertools

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin

from flask_admin.contrib import sqla
from flask_admin.actions import action

# Create application
app = Flask(__name__)


# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///common.db'
app.config['SQLALCHEMY_ECHO'] = True

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'common.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    ADMIN='admin@qq.com',
    PASSWORD='123'
))
db = SQLAlchemy(app)
def get_db(db_name= app.config['DATABASE']):
    """Connects to the specific database."""
    rv = sqlite3.connect(db_name)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('sql/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()




def create_user(dbname):
    """Initializes the user db"""
    db = get_db(session['db_name'])
    with app.open_resource('sql/label.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def write_back_label():
    user_db = get_db(session['db_name'])
    sql = 'select * from image'
    cur = user_db.execute(sql)
    res =  dictfetchall(cur)
    user_db.close()

    db = get_db()
    for items in res:
        sql = 'update image set status = "{0}" where id = "{1}"'.format(items['status'],items['image_id'])
        db.execute(sql)
        db.commit()
        print sql


def init_user():
    db = get_db()
    sql = 'select class_id, class_name, name from tasks,datasets, class where tasks.dataset_id = datasets.id and tasks.class_id = class.id and tasks.user_name ="{0}"'.format(session['username'])
    cur = db.execute(sql)
    task = dictfetchall(cur)
    print "task"
    print task
    image_list ={}
    for k in task:
        sql = 'select * from image where class_id = {0}'.format(k['class_id'])
        cur = db.execute(sql)
        image = dictfetchall(cur)
        image_list[k['class_id']] = image
    print image_list

    db.close()

    user_db = get_db(session['db_name'])
    print task
    for k in task:
        sql = 'insert or ignore into tasks (tasks_id, dataset_name, name, status) values({0},"{1}","{2}","0/{3}")'.format(k['class_id'],k['name'].encode('utf-8'),k['class_name'].encode('utf-8'),len(image_list[k['class_id']]))
        print sql
        user_db.execute(sql)

        for image in image_list[k['class_id']]:
            print image
            sql = 'insert or ignore into image (image_id, tasks_id,image_path,status) values({0},{1},"{2}","{3}")'.format(image['id'],image['class_id'],image['image_path'].encode('utf-8'),image['status'].encode('utf-8'))
            user_db.execute(sql)

    user_db.commit()
    user_db.close()




# @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables. common.db"""
#     # init_db()
#     db.create_all()
#     user = Users("lcy4869@qq.com","123")
#     db.session.add(user)
#     db.session.commit()
#     print('Initialized the database.')


@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if session.get('admin'):
            return redirect('/admin');
        else:
            return render_template('tasks.html')

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

from tree import tree
import re
@app.route('/Task')
def getTask():
    """from common.db get tasks"""
    db = get_db()
    sql = 'select * from tasks where user_name ="{0}"'.format(session['username'])
    cur = db.execute(sql)
    task_list = dictfetchall(cur)
    db.close()

    user_db = get_db(session['db_name'])
    result = []
    for item in task_list:
        """update the task status!!!"""
        sql = 'select count(*) from image where tasks_id="{0}" and status <> "unlabelled"'.format(item['class_id'])
        cur = user_db.execute(sql)
        label_num = cur.fetchall()[0][0]

        sql = 'select count(*) from image where tasks_id="{0}"'.format(item['class_id'])
        cur = user_db.execute(sql)
        total_num = cur.fetchall()[0][0]
        status = str(label_num)+"/"+str(total_num)

        sql = 'update tasks set status = "{0}" where tasks_id = "{1}"'.format(status,item['class_id'])
        cur = user_db.execute(sql)
        user_db.commit()

        """"get the task """
        sql = 'select * from tasks where tasks_id ="{0}"'.format(item['class_id'])
        cur = user_db.execute(sql)
        tmp = dictfetchall(cur)

        result = result + tmp
    # print result
    tree(result)
    user_db.close()
    json_results = json.dumps(tree(result))
    print "Asd"
    print json_results

    p = re.compile(r'(\"tags\":) \"(\d+\/\d+)\"}')
    print p.findall(json_results)
    print p.sub(r'\1 ["\2"]}', json_results)

    return p.sub(r'\1 ["\2"]}', json_results)
    return json_results

@app.route('/Insert',methods=['POST'])
def updateLabel():
    if request.method == 'POST':
        label = request.get_json()['label']
        for i in range(len(label)):
            db = get_db(session['db_name'])
            sql = 'update image set status = "{0}" where image_id = "{1}"'.format(label[i]['status'],label[i]['id'])
            db.execute(sql)
            db.commit()
    return 'yes'

@app.route('/getImagePath',methods=['GET'])
def getImagePath():
    id = request.args.get('id')
    begin = request.args.get('index')
    num = request.args.get('num')

    db = get_db(session['db_name'])
    sql = 'select * from image where tasks_id ={0} limit {1},{2}'.format(id,begin,num)
    cur = db.execute(sql)
    image = dictfetchall(cur)

    db.close()
    print image
    return json.dumps(image)



@app.route('/Image')
def getImage():
    id = request.args.get('id')
    name = request.args.get('name')
    db = get_db(session['db_name'])

    sql = 'select count(*) from image where tasks_id = {0}'.format(id)
    cur = db.execute(sql)
    image_num = cur.fetchall()[0][0]
    print image_num
    return render_template('hehe.html',id=id,total=image_num,category = name)



@app.route('/login', methods=['POST'])
def login():
    error = None
    username = request.form['username']
    pwd = request.form['password']
    db = get_db()
    sql = 'select count(*) from users where name="{0}" and pwd="{1}"'.format(username,pwd)
    cur = db.execute(sql)
    correct = cur.fetchall()[0][0]

    if request.method == 'POST':
        if username == app.config['ADMIN'] and pwd == app.config['PASSWORD'] :
            session['logged_in'] = True
            session['admin'] = True
            return redirect(url_for('show_entries'))

        else:
            if correct == 1:
                session['db_name'] = os.path.join(app.root_path, "db/"+username)
                session['logged_in'] = True
                session['username'] = username
                print session['db_name']
                # if not os.path.exists(session['db_name']):
                create_user(session['db_name'])
                init_user()
                return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout',methods=['POST','GET'])
def logout():
    if session.get('db_name'):
        write_back_label()
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('db_name', None)
    session.pop('admin', None)
    session.pop('dataset_id', None)

    return redirect(url_for('show_entries'))


# Flask views
@app.route('/admin')
def index():
    session['dataset_id'] = ""
    print "asd"+session['dataset_id']
    if not session.get('admin'):
        return redirect(url_for('logout'))
    else:
        return redirect('/admin/users/')

# Create models
class Users(db.Model):
    __tablename__ = 'users'
    def __init__(self, name="", pwd=""):
        self.name = name
        self.pwd = pwd
    name = db.Column(db.String(100),primary_key=True)
    pwd = db.Column(db.String(100))


    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return '%s - %s' % (self.name, self.pwd)

class Datasets(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    data_path = db.Column(db.String(100))

    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.name

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer,primary_key=True)
    dataset_id = db.Column(db.Integer,db.ForeignKey('datasets.id'))
    class_name = db.Column(db.String(100))
    def __init__(self, dataset_id="", class_name=""):
            self.dataset_id = dataset_id
            self.class_name = class_name
    dataset = db.relationship('Datasets',
                           backref=db.backref('class', cascade="all, delete-orphan"),
                           lazy='joined')
    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.class_name

class Image(db.Model):
    __tablename__ = 'image'
    def __init__(self, dataset_id="",class_id="", image_path="",status=""):
            self.dataset_id = dataset_id
            self.class_id = class_id
            self.status = status
            self.image_path = image_path

    id = db.Column(db.Integer,primary_key=True)
    dataset_id = db.Column(db.Integer,db.ForeignKey('datasets.id'))
    class_id = db.Column(db.Integer,db.ForeignKey('class.id'))

    classes = db.relationship('Class',
                           backref=db.backref('image', cascade="all, delete-orphan"),
                           lazy='joined')
    dataset = db.relationship('Datasets',
                           backref=db.backref('image', cascade="all, delete-orphan"),
                           lazy='joined')
    image_path = db.Column(db.String(100))
    status = db.Column(db.String(100))


    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.image_path

class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer,primary_key=True)
    dataset_id = db.Column(db.Integer,db.ForeignKey('datasets.id'))
    class_id = db.Column(db.Integer,db.ForeignKey('class.id'),unique=True)
    user_name = db.Column(db.String(100))
    # accept = db.Column(db.String(100))
    classes = db.relationship('Class',
                           backref=db.backref('tasks', cascade="all, delete-orphan"),
                           lazy='joined')
    dataset = db.relationship('Datasets',
                           backref=db.backref('tasks', cascade="all, delete-orphan"),
                           lazy='joined')
    # user = db.relationship('Users',
    #                       backref=db.backref('tasks', cascade="all, delete-orphan"),
    #                       lazy='primaryjoin')
    def __unicode__(self):
        return '%s - %s' % (self.user_name, self.accept)

@app.route('/batch',methods=['GET'])
def batch():
    id = request.args.get('username')
    print id
    db = get_db()
    for item in session['json']:
        print item
        sql = 'insert or ignore into tasks (dataset_id, class_id,user_name, accept) values({0},{1},"{2}","{3}")'.format(item[1],item[0],id,"none")
        print sql
        cur = db.execute(sql)
    db.commit()
    db.close()
    return redirect('/admin/tasks/')

from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from flask.ext.admin.contrib.sqla.view import ModelView, func
from flask import Markup

class usersView(sqla.ModelView):
    column_display_pk = True
    form_columns = ['name', 'pwd']
    def is_visible(self):
        if not session.get('dataset_id'):
            return True
        else:
            if session['dataset_id'] == "":
                return True
            else:
                return False
from sqlalchemy import and_

def new_dataset(model):
    """Initializes the dataset."""
    # print model.data_path
    dataset_id = model.id
    dataset_path = model.data_path
    for root, dirs, files in os.walk(dataset_path):
        first = 1
        for image in files:
            if image.find(".jpg") > 0:
                if image.find("thumb") > 0:
                    continue
                classname = root.split('/')[-1]
                if first == 1:
                    new = Class(model.id,classname)
                    db.session.add(new)
                    first = 0
                this_class = Class.query.filter(and_(Class.class_name == classname,Class.dataset_id == dataset_id)).first()
                print dataset_id
                img = Image(dataset_id,this_class.id,os.path.join(root,image),"unlabelled")
                db.session.add(img)
                db.session.commit()

                # print

class datasetsView(sqla.ModelView):
    column_display_pk = True
    form_columns = ['name','data_path']
    def is_visible(self):
        if not session.get('dataset_id'):
            return True
        else:
            if session['dataset_id'] == "":
                return True
            else:
                return False
    def _dataset_id_formatter(view, context, model, name):
        return Markup(
            "<a href='%s'>%s</a>" % (
                '/dataset?dataset_id='+str(model.id)+'&dataset_name='+str(model.name),
                model.id
            )
        )

    column_formatters = {
        'id': _dataset_id_formatter
    }
    def after_model_change(self,form, model, is_created):
        print model.id
        print model.data_path
        if is_created:
            new_dataset(model)
            print "asdasdasd"


@app.route('/dataset',methods = ['GET','POST'])
def dataset():
    if not request.args.get('dataset_id'):
        session['dataset_id'] = ""
    else:
        session['dataset_id'] = request.args.get('dataset_id')
        # session['dataset_name'] = request.args.get('dataset_name')
        admin.name = request.args.get('dataset_name')

    return redirect('/admin/class/')


class tasksView(sqla.ModelView):
    can_export = True

    def get_query(self):
        if session['dataset_id'] == "":
            return self.session.query(self.model)
        else:
            return self.session.query(self.model).filter(self.model.dataset_id==session['dataset_id'])

    def get_count_query(self):
        if session['dataset_id'] == "":
            return self.session.query(func.count('*')).select_from(self.model)
        else:
            return self.session.query(func.count('*')).filter(self.model.dataset_id==session['dataset_id'])


    column_display_pk = True

    column_filters = [
        FilterEqual(Tasks.user_name, 'User_name'),
        FilterEqual(Tasks.dataset_id, 'Dataset_id')
    ]
    form_columns = ['dataset_id', 'class_id','user_name']


class classView(sqla.ModelView):
    def get_query(self):
        return self.session.query(self.model).filter(self.model.dataset_id==session['dataset_id'])

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.dataset_id==session['dataset_id'])


    def is_visible(self):
        if session['dataset_id'] == "":
            return False
        else:
            return True

    column_display_pk = True
    form_columns = ['id', 'dataset_id','class_name']
    @action('assign', 'Assign', 'Are you sure you want to assign selected classes?')
    def action_assign(self, ids):
        try:
            query = Class.query.filter(Class.id.in_(ids))
            l = []
            for task in query.all():
                l.append((task.id, task.dataset_id))
            session['json'] = l

            # return render_template('batch.html')
            return '<script src="../../../static/js/label.js">prompt();</script>'
            # return '<script >var name=prompt("input a username","lcy4869@qq.com");window.location = "/batch?username="+name;</script>'

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to approve users. %(error)s', error=str(ex)), 'error')
from flask_admin import form
class imageView(sqla.ModelView):
    can_export = True

    def get_query(self):
        return self.session.query(self.model).filter(self.model.dataset_id==session['dataset_id'])

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.dataset_id==session['dataset_id'])

    def is_visible(self):
        if not session.get('dataset_id'):
            return False
        else:
            if session['dataset_id'] == "":
                return False
            else:
                return True
    column_display_pk = True
    form_columns = ['dataset_id','class_id','image_path']
    column_filters = [
        FilterEqual(Image.class_id, 'class_id'),
    ]
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''
        # print url_for('static',filename = form.thumbgen_filename(model.image_path))
        path = '../../'+form.thumbgen_filename(model.image_path)
        return Markup('<img src="%s">' % path)

    column_formatters = {
        'image_path': _list_thumbnail
    }


from flask_admin import BaseView, expose
class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/logout')
    def is_visible(self):
        if session['dataset_id'] == "":
            return True
        else:
            return False
class backView(BaseView):
    @expose('/')
    def index(self):
        admin.name = "Admin"
        session['dataset_id'] = ""
        return redirect('/admin/users/')
    def is_visible(self):
        if session['dataset_id'] == "":
            return False
        else:
            return True

admin = admin.Admin(app, name='Admin',index_view=admin.AdminIndexView(
        name=' ',
        url='/admin'
            ),template_mode='bootstrap3')
# Create admin
admin.add_view(usersView(Users, db.session))
admin.add_view(datasetsView(Datasets, db.session))
admin.add_view(classView(Class, db.session))
admin.add_view(imageView(Image, db.session))
admin.add_view(tasksView(Tasks, db.session))

admin.add_view(backView(name='Back',menu_class_name="alert-success"))
admin.add_view(MyView(name='Logout', menu_class_name="alert-success"))


if __name__ == '__main__':
    # Start app
    app.run(debug=True)
