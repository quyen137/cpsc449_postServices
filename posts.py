import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

# load all of the *sql files in the queries/ directory into a single module
queries = pugsql.module('queries/')

# go into posts.cfg to get DATABASE_URL
queries.connect(app.config['DATABASE_URL'])

# we first init database 
@app.cli.command('init')
def init_db():
    with app.app_context():
        # we will create a connection first
        db = queries._engine.raw_connection()
        # we will select the database that we will use
        with app.open_resource('userdata.sql',mode='r') as f:
            # read from that database
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to POSTS microservices</h1>
    <p> You can select /create To create post</p>
    <p> You can select /delete/<int:id> To delete post</p>
    <p> You can select /retrieve/<int:id> To retrieve all posts</p>
    <p> You can select /mostrecent To retrieve most recent posts</p> 
    <p> You can select /community/mostrecent To retrieve specific community posts</p> '''

# show all posts
@app.route('/api/mostrecent', methods=['GET'])
def all_posts():
    # go into database and take out all posts
    all_posts = queries.all_posts()
    return list(all_posts)

# since you cant go directly to create it will be reroute
@app.route('/api/create',methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        return print_insert(request.args)
    elif request.method == 'POST':
        return create_post(request.data)

# create posts
def create_post(userPost):
    # validation check to make sure all field are being input into database
    required_fields = ['article', 'username', 'community']
    # if some field are empty throw exception
    if not all([field in userPost for field in required_fields]):
        raise exceptions.ParseError()
    try:
        userPost['id'] = queries.create_post(**userPost)
    except Exception as e:
        #show error code that item already exist
        return {'error':str(e)}, status.HTTP_409_CONFLICT 
    # return create successfull and location being stored
    return userPost, status.HTTP_201_CREATED, {
        'Location' : f'/retrieve/{userPost["id"]}'
    }

# printout inserted data
def print_insert(query_parameter):
    id = query_parameter.get('id')
    username = query_parameter.get('username')
    community = query_parameter.get('community')
    query = "SELECT * FROM userdata WHERE"
    to_filter = []
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if community:
        query += ' community=? AND'
        to_filter.append(community)
    if not (id or username or community):
        raise exceptions.NotFound()
    query = query[:-4] + ';'
    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))

# 
@app.route('/api/retrieve/<int:id>',methods=['GET','DELETE'])
# retrieve and delete a specific post
def retrieve_post(id):
    if request.method == 'GET':
        post = queries.post_by_id(id=id)
        if post:
            return post
        else:
            raise exceptions.NotFound()
    if request.method == 'DELETE':
        if post:
            return status.HTTP_204_NO_CONTENT
    else:
        raise exceptions.NotFound()

# # delete a specifc post
# def delete_post(id):
#     post = queries.post_by_id(id=id)
#     if post:
#         post.pop(id)
#         return status.HTTP_204_NO_CONTENT
#     else:
#         raise exceptions.NotFound()

