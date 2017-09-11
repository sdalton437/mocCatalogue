from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Sport, Item 

from flask import session as login_session
import random, string


from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app=Flask(__name__)

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')

def menu():
	categories = session.query(Sport).all()
	return render_template("mainMenu.html",categories=categories)

@app.route('/catalog/<sport_id>/items/')
	
def showSport(sport_id):
	sport = session.query(Sport).filter_by(id=sport_id).one()
	items = session.query(Item).filter_by(sport_id = sport.id).all()
	return render_template('showSport.html',item= sport, items = items)

@app.route('/catalog/<sport_id>/<item_id>/')

def showItem(sport_id, item_id):
	showItem = session.query(Item).filter_by(id = item_id, sport_id=sport_id).one()
	return render_template('showItem.html',item = showItem)


@app.route('/catalog/<int:sport_id>/<int:item_id>/edit', methods=['GET','POST'])

def editItem(sport_id,item_id):
    editedItem = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
        	editedItem.description = request.form['description']
    	session.add(editedItem)
    	session.commit()
    	flash("Item Edited!")
    	return redirect(url_for('showItem',sport_id=sport_id,item_id=item_id))
    else:
        return render_template('editItem.html', sport_id = sport_id, item_id = item_id,item= editedItem)

@app.route('/catalog/<sport_id>/<item_id>/delete',methods=['GET','POST'])

def deleteItem(sport_id,item_id):
	deletedItem = session.query(Item).filter_by(id = item_id).one()

	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Item Deleted!")
		return redirect(url_for('showItems', sport_id=sport_id))
	else:
		return render_template('deleteItem.html',sport_id=sport_id,item_id=item_id,item = deletedItem)

@app.route('/catalog/<int:sport_id>/create',methods=['GET','POST'])
def createItem(sport_id):
	if request.method == 'POST':
		newItem = Item(name = request.form['name'],description=request.form['description'], sport_id=sport_id)
		session.add(newItem)
		session.commit()
		flash('Item Created!')
		return redirect(url_for('showSport', sport_id=sport_id))
	else:
		return render_template('createItem.html',sport_id=sport_id)





if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)