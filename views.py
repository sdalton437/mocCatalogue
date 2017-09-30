from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Sport, Item, User

from flask import session as login_session
import random
import string


from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from functools import wraps

app = Flask(__name__)

# Declare the client_id
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "MOC Catalogue"
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                                  digits) for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)

# login function


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            'connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'
    'border-radius: 150px;-webkit-border-radius:'
    '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# logout function


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/'
           'revoke?token=%s') % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Return all sport in JSON format


@app.route('/JSON')
def menuJSON():
    categories = session.query(Sport).all()
    return jsonify(Categories=[i.serialize for i in categories])

# Return all items in specific sport in JSON format


@app.route('/catalog/<int:sport_id>/items/JSON')
def showSportJSON(sport_id):
    sport = session.query(Sport).filter_by(id=sport_id).one()
    items = session.query(Item).filter_by(sport_id=sport.id).all()
    return jsonify(SportItems=[i.serialize for i in items])

# Return specific sport in JSON format


@app.route('/catalog/<int:sport_id>/<int:item_id>/JSON')
def showItemJSON(sport_id, item_id):
    showItem = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=showItem.serialize)

# Main Menu


@app.route('/')
def menu():
    categories = session.query(Sport).all()
    Login_session = login_session
    return render_template("mainMenu.html",
                           categories=categories, login_session=Login_session)

# Sport Main Menu


@app.route('/catalog/<int:sport_id>/items/')
def showSport(sport_id):
    sport = session.query(Sport).filter_by(id=sport_id).one()
    items = session.query(Item).filter_by(sport_id=sport.id).all()
    Login_session = login_session
    if 'username' not in login_session:
        return render_template('publicshowSport.html', item=sport, items=items,
                               login_session=Login_session)
    else:
        return render_template('showSport.html', item=sport, items=items)

# Item Main Menu


@app.route('/catalog/<int:sport_id>/<int:item_id>/')
def showItem(sport_id, item_id):
    showItem = session.query(Item).filter_by(id=item_id).one()
    Login_session = login_session
    if ('username' not in login_session or
            showItem.user_id != login_session['user_id']):
        return render_template('publicshowItem.html', item=showItem,
                               login_session=Login_session)
    else:
        return render_template('showItem.html', item=showItem)

# Edit Item


@app.route('/catalog/<int:sport_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(sport_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    creator = getUserID(editedItem.user_id)
    if ('username' not in login_session or
            editedItem.user_id != login_session['user_id']):
        return ("<script>function myFunction(){alert"
                "('You are not authorized to edit this item."
                " Please login as owner to edit item.');}"
                "</script><body onload='myFunction()''>")

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        session.add(editedItem)
        session.commit()
        flash("Item Edited!")
        return redirect(url_for('showItem', item_id=item_id,
                                sport_id=sport_id, item=editedItem))
    else:
        return render_template('editItem.html', sport_id=sport_id,
                               item_id=item_id, item=editedItem)

# Delete Item


@app.route('/catalog/<int:sport_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(sport_id, item_id):
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if ('username' not in login_session or
            deletedItem.user_id != login_session['user_id']):
        return ("<script>function myFunction() "
                "{alert('You are not authorized to delete this item. "
                "Please login as owner to edit item.');}</script><body "
                "onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Item Deleted!")
        return redirect(url_for('showSport', sport_id=sport_id))
    else:
        return render_template('deleteItem.html', sport_id=sport_id,
                               item_id=item_id, item=deletedItem)

# Create Item


@app.route('/catalog/<int:sport_id>/create', methods=['GET', 'POST'])
@login_required
def createItem(sport_id):

    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       picture=request.form['picture'],
                       sport_id=sport_id, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('Item Created!')
        return redirect(url_for('showSport', sport_id=sport_id))
    else:
        return render_template('createItem.html', sport_id=sport_id)

# Create User


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get User ID


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
