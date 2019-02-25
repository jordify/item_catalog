from flask import (
    Flask, redirect, render_template, request, url_for, flash, jsonify, g
)

from models import User, Category, Item
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/')
@app.route('/catalog/')
def index():
  """Show all of the categories and the last 10 items created."""
  session = DBSession()
  categories = session.query(Category)
  items = session.query(Item).order_by(desc(Item.time_created)).limit(10).all()
  return render_template('index.html', categories=categories, items=items)

@app.route('/newItem/', methods=['GET', 'POST'])
def newItem():
  """Allow logged-in users to make a new item"""
  if request.method=='POST':
    session = DBSession()
    category_id = createNewCategory(request.form['category'])
    newItem = Item(
        name=request.form['name'],
        description=request.form['description'],
        category_id=category_id
    )
    session.add(newItem)
    session.commit()
    flash('New item, %s, created!' % (newItem.name,))
    return redirect(url_for('index'))
  else:
    return render_template('newItem.html')

@app.route('/catalog/<string:categoryName>', methods=['GET'])
def categoryListing(categoryName):
  if request.method=='GET':
    session = DBSession()
    category = session.query(Category).filter_by(name=categoryName).one()
    items = session.query(Item).filter_by(category_id=category.id).order_by(desc(Item.time_created)).all()
    return render_template('category.html', category=category, items=items)
  else:
    return redirect(url_for('index'))

@app.route('/catalog/<string:categoryName>/<string:itemName>', methods=['GET'])
def itemListing(itemName, categoryName):
  if request.method=='GET':
    session = DBSession()
    item = session.query(Item).filter_by(name=itemName).one()
    return render_template('item.html', item=item)
  else:
    return redirect(url_for('index'))


@app.route('/catalog/<string:categoryName>/<string:itemName>/edit', methods=['GET', 'POST'])
def editItem(itemName, categoryName):
  """Allow logged-in users to edit an existing item"""
  session = DBSession()
  categories = session.query(Category)
  editItem = session.query(Item).filter_by(name=itemName).one()
  if request.method=='GET':
    return render_template('editItem.html', categories=categories, item=editItem)
  elif request.method=='POST':
    if request.form['name']:
      editItem.name = request.form['name']
    if request.form['description']:
      editItem.description = request.form['description']
    if request.form.get('categoryName'):
      category = session.query(Category).filter_by(name=request.form['categoryName']).one()
      editItem.category_id = category.id
    session.add(editItem)
    session.commit()
    flash('Item, %s, edited!' % (editItem.name,))
    return redirect(url_for('itemListing', categoryName=editItem.category.name, itemName=editItem.name))
  else:
    return redirect(url_for('index'))


@app.route('/catalog/<string:categoryName>/<string:itemName>/delete', methods=['GET', 'POST'])
def deleteItem(itemName, categoryName):
  """Deletes an item. Logged in users only!"""
  session = DBSession()
  deleteItem = session.query(Item).filter_by(name=itemName).one()
  if request.method=='POST':
    session.delete(deleteItem)
    session.commit()
    flash('Item, %s, deleted!' % (deleteItem.name,))
    return redirect(url_for('index'))
  else:
    return render_template('deleteItem.html', item=deleteItem)


@app.route('/catalog/<string:categoryName>/delete', methods=['GET', 'POST'])
def deleteCategory(categoryName):
  """Deletes a category. Should check for items in category or happen
  automatically. Logged in users only!"""
  session = DBSession()
  deleteCategory = session.query(Category).filter_by(name=categoryName).one()
  if request.method=='POST':
    session.delete(deleteCategory)
    session.commit()
    flash('Category, %s, deleted!' % (deleteCategory.name,))
    return redirect(url_for('index'))
  else:
    return render_template('deleteCategory.html', category=deleteCategory)


def createNewCategory(categoryName):
  """Check if categoryName exists, create a new category if not.
  Returns category ID"""
  session = DBSession()
  category = session.query(Category).filter_by(name=categoryName).limit(1).all()
  if not category:
    category = Category(name=categoryName)
    session.add(category)
    session.commit()
    return category.id
  else:
    return category[0].id


if __name__=='__main__':
  app.debug = True
  app.secret_key = 'debug'
  app.run(host='0.0.0.0', port=5000)
