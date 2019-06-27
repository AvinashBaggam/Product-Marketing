from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import User, Product, Review, connect_to_db
from product_Marketing import get_chart_data, format_reviews_to_dicts
import json

app = Flask(__name__)


app.secret_key = "ProductMarketing"


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def display_homepage():
    

    return render_template("homepage.html")


@app.route('/search')
def search_products():
    

    search_query = request.args.get('query')

    
    products = Product.find_products(search_query)

    return render_template("product_listing.html",
                           query=search_query,
                           products=products)


@app.route('/product-scores/<asin>.json')
def product_reviews_data(asin):
    

    product = Product.query.get(asin)
    score_list = product.get_scores()

   
    data_dict = get_chart_data(score_list)

    return jsonify(data_dict)


@app.route('/search-review/<asin>.json')
def search_reviews(asin):
    

    search_query = request.args.get('query')

    
    reviews = Review.find_reviews(asin, search_query)

    user_id = None

    if "user" in session:
        user_id = session["user"]["id"]

    
    review_dict_list = format_reviews_to_dicts(reviews, user_id)

    return jsonify(review_dict_list[:10])


@app.route('/product/<asin>')
def display_product_profile(asin):
    

    product = Product.query.get(asin)

    favorite_reviews = None
    is_favorite = None

    if "user" in session:
        user_id = session["user"]["id"]
        user = User.query.get(user_id)

        
        favorite_reviews = user.get_favorite_review_ids()
        is_favorite = user.is_favorite_product(asin)

    return render_template("product_details.html",
                           product=product,
                           pos_words=json.dumps(product.pos_words),
                           neg_words=json.dumps(product.neg_words),
                           is_favorite=is_favorite,
                           favorite_reviews=favorite_reviews)



@app.route('/user/<user_id>')
def display_user_profile(user_id):
    

    user_id = int(user_id)
    user = User.query.get(user_id)

    favorite_products = user.favorite_products.all()

    for pr in favorite_products:

        
        pr.favorited_reviews = user.get_favorite_reviews_for_product(pr.asin)

    return render_template("user_page.html",
                           user=user,
                           favorite_products=favorite_products)


@app.route('/favorite-product', methods=['POST'])
def favorite_product():
    

    asin = request.form.get('asin')
    user_id = session['user']['id']

    user = User.query.get(user_id)

    
    favorite_status = user.update_favorite_product(asin)

  
    if favorite_status == "Unfavorited":
        user.remove_favorite_reviews(asin)

    return favorite_status


@app.route('/favorite-review', methods=['POST'])
def favorite_review():
    
    review_id = request.form.get('reviewID')
    asin = request.form.get('asin')
    user_id = session['user']['id']

    user = User.query.get(user_id)

    
    favorite_status = user.update_favorite_review(review_id)

    
    if favorite_status == "Favorited":
        user.add_favorite_product_from_review(asin)

    return favorite_status




@app.route('/register', methods=["GET"])
def display_registration():
    """Display register form"""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_registration():
    """Process a new user's' registration form"""

    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).count() != 0:
        message = "That email already exists. Please login or register for a new account"
    else:
        User.register_user(name, email, password)
        message = "Welcome to Product Genius"

    flash(message)

    return redirect("/login")


@app.route('/login', methods=["GET"])
def display_login():
    """Display login form"""

    return render_template('login_form.html')


@app.route('/login', methods=["POST"])
def log_in():
    """Log user in"""

    email = request.form.get('email')
    password = request.form.get('password')

  
    user_query = User.query.filter_by(email=email)

   
    if user_query.count() == 0:
        flash("No account exists for that email")
        return redirect("/")

    user = user_query.one()

   
    if user.password == password:

        
        session['user'] = {"id": user.user_id,
                           "name": user.name}

        flash("Logged in as {}".format(user.name))
        return redirect("/")

    else:
        flash("Incorrect password")
        return redirect("/login")


@app.route('/logout')
def log_out():
    """Log user out"""

    
    del session['user']

    return redirect("/")





if __name__ == "__main__":

    
    app.debug = True

    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.run(port=5000, host='0.0.0.0')
