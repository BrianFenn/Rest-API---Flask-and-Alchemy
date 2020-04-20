from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#@app.route('/', methods=['GET'])
#def get():
#   return jsonify({ 'msg': 'Hello World'})

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQL Alchemy (our database)
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True) #auto-increment will be done automatically
  name = db.Column(db.String(100), unique=True) #create a string with limit of 100 characters & be unique, (meaning no two products can have the same name)
  description = db.Column(db.String(200)) # 200 characters limit
  price = db.Column(db.Float) # We'll use a float for price
  qty = db.Column(db.Integer) # Qauntity will be an integer

# Our Constructor
  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
# this is where we'll use Marshmallow by passing in ma.Schema, and 
class ProductSchema(ma.Schema): 
  class Meta: #this is the fields were allowing to show from our Product Schema
    fields = ('id', 'name', 'description', 'price', 'qty') # we'll go ahead and show everything (including the id)


# Initialize Our Schema
product_schema = ProductSchema() # pass in an object of script=True, or else, we'll get a warning message 
products_schema = ProductSchema(many=True) # this will handle our call for products, (not just calling a single product)


 # Create a Product
@app.route('/product', methods=['POST'])
def add_product(): # attach our fields below using requests (bringing in our data that is passed in from postman)
 name = request.json['name'] #since it will be json data
 description = request.json['description']
 price = request.json['price']
 qty = request.json['qty']

 new_product = Product(name, description, price, qty) #creating a new product with our Product Class, this is data coming from Postman (or Client)

 db.session.add(new_product)
 db.session.commit() # to save the new_product variable (our new product information) to the database

 return product_schema.jsonify(new_product) # to return our new_product variable (our product information) to the client, remember it will need to be sent iin json to the client

# Get All Products
@app.route('/product', methods=['GET']) # Same route as Create a Product
def get_products(): # create a function to get all of our products 
  all_products = Product.query.all() # create a variable to our moodel (or our class), which will have a method on it called query, then we want to get all, this will get all our products
  result = products_schema.dump(all_products) # Now, get our result for products(since there is more than one product) so we'll use products_schema where many=True, and use the dump method to return the data
                                              # of our variable all_products
  return jsonify(result) # Now return our list in json using jsonify data (note: instructor advised result.data would not work, per video, so only use result object, which is our call keyword to return our result 
                          #(which result keyword is an object in a(our) dictionary)

# Get a Single Product
@app.route('/product/<id>', methods=['GET']) #this time use the route above, but since we need a specific product, use "/" to enter a new directory path with < > brackets with the id inside it
def get_product(id): # instead of get_products and pass our id into the function
  product = Product.query.get(id) # just product instead of products, and we "query" with a call "get" on the "(id)"
  # result = product_schema.dump() # we don't need this because we are not dealing with an array, we are only dealing with a single product
  # return jsonify(result) can be combined below:

  return product_schema.jsonify(product) # and combine our product_schema call to return product_schema.jsonfiy(product), since we are not using an array if for multiple products

# Update a Product

@app.route('/product/<id>', methods=['PUT']) # we need to know which ID to update, so /<id> will be the route in our product directory, and we'll use 'PUT' since we are using an Update (not POST)
def update_product(id): # define our function as update_product() and pass in our id which will be pulled from Postman
  product =  Product.query.get(id) # we need to first, fetch our product (that we'll update) so, we'll create a variable and set it equal to our class Product. which has a propeerty query (or property query object)
             # that has a method called .get and pass in our id that the user enters in Postman 
#since we'll need to get all of our fields from the body of the request, we'll keep all of this data, like we used to Create a Product
  name = request.json['name'] # since it will be json data
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

 # Now we need to construct a new product to submit to the database
  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

#we don't need to add, like we did for a new product, so we can remove the code below (from our create product, b/c we just copied the create product function to save time)
 #new_product = Product(name, description, price, qty) //#creating a new product with our Product Class, this is data coming from Postman (or Client)

 # db.session.add(new_product) #we don't need to add a new product since we are just updating, so we don't need this either.
  db.session.commit() #we still need this to commit the change to update our product

# Since we are not creating a new product, we can use the script return product_schema.jsonify(product) b/c we already have our product, and we're just going to update it 
 #return product_schema.jsonify(new_product) # to return our new_product variable (our product information) to the client, remember it will need to be sent iin json to the client
  return product_schema.jsonify(product) #since we already have our product we use product, not calling a new_product   

# Now we need to Our final CRUDE Function DELETE

@app.route('/product/<id>', methods=['DELETE']) #this time use the route above, but since we need a specific product, use "/" to enter a new directory path with < > brackets with the id inside it
def delete_product(id): # create our delete function name and pass in our id that the user will enter in Postman
  product = Product.query.get(id) # we still will need to query our product, (to know what product we need to delete)
  
  db.session.delete(product) # We call our db.session delete funciton with the product we plan to delete
  db.session.commit() # we need to commit this change to our database (or else it won't happen)
  return product_schema.jsonify(product) # now we can view in the Postman terminal the product that we are deleting, # and combine our product_schema call to return product_schema.jsonfiy(product), since we are not using an array if for multiple products


# Run Server

if __name__== '__main__':
  app.run(debug=True)


  #we're done, we could of done this app without SQLAlchemy, by using Flask Restful, but it is much too much harder, and unnecessary.  
  # You could build a front-end to this app though.

  #Source:
  # Travery, B. (2019, Jan 7). "Rest api with flask & sql alchemy." Traversy Media. Retrieved from https://www.youtube.com/watch?v=PTZiDnuC86g&feature=youtu.be