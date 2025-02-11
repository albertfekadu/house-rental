import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv  # Import load_dotenv
from sqlalchemy import or_, and_

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# Use an absolute path for the database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'house_rental.db')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'static/uploads'  # Create a folder named 'uploads' in the 'static' directory
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Configure pagination
LISTINGS_PER_PAGE = 6

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HouseListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact = db.Column(db.String(100))
    images = db.relationship('Image', backref='house_listing', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('house_listing.id'), nullable=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('house_listing.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    listings = HouseListing.query.paginate(page=page, per_page=LISTINGS_PER_PAGE)
    return render_template('index.html', listings=listings)

@app.route("/admin_dashboard", methods=['GET'])
@login_required
def admin_dashboard():
    if not current_user.is_authenticated:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('login'))

    # Fetch necessary data for the dashboard
    active_listings = HouseListing.query.count()
    revenue = db.session.query(db.func.sum(HouseListing.price)).scalar() or 0.0
    search_trends = []  # Assuming you have a model to track search trends

    return render_template('admin_dashboard.html', 
                           active_listings=active_listings, 
                           revenue=revenue, 
                           search_trends=search_trends)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '', type=str)
    sort_by = request.args.get('sort_by', 'newest', type=str)  # Default: newest first
    page = request.args.get('page', 1, type=int)

    filters = []

    if query:
        search_filter = "%{}%".format(query)
        filters.append(or_(
            HouseListing.title.like(search_filter),
            HouseListing.location.like(search_filter),
            HouseListing.amenities.like(search_filter),
            HouseListing.contact.like(search_filter)
        ))

    listings_query = HouseListing.query

    if filters:
        listings_query = listings_query.filter(and_(*filters))

    # Sorting logic
    if sort_by == "low_price":
        listings_query = listings_query.order_by(HouseListing.price.asc())  # Sort by price ascending
    elif sort_by == "high_price":
        listings_query = listings_query.order_by(HouseListing.price.desc())  # Sort by price descending
    elif sort_by == "newest":
        listings_query = listings_query.order_by(HouseListing.id.desc())  # Sort by most recent (assuming ID increases over time)

    listings = listings_query.paginate(page=page, per_page=LISTINGS_PER_PAGE)
    
    return render_template('search.html', listings=listings, query=query, sort_by=sort_by)

@app.route('/listing/<int:id>')
def listing(id):
    house = HouseListing.query.get_or_404(id)
    return render_template('listing.html', house=house)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        location = request.form.get('location')
        number_of_rooms = request.form.get('number_of_rooms')
        amenities = request.form.get('amenities')
        contact = request.form.get('contact')

        # Handle image upload
        images = request.files.getlist('images')
        image_urls = []

        for file in images:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_urls.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            price = float(price)
            number_of_rooms = int(number_of_rooms)
        except ValueError:
            flash("Invalid price or number of rooms", 'error')
            return render_template('add_listing.html')

        new_listing = HouseListing(
            title=title,
            price=price,
            location=location,
            number_of_rooms=number_of_rooms,
            amenities=amenities,
            contact=contact,
            user_id=current_user.id,
        )

        for image_url in image_urls:
            image = Image(filename=image_url, house_listing=new_listing)
            db.session.add(image)

        db.session.add(new_listing)
        db.session.commit()
        flash('New listing added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_listing.html')

@app.route('/add_to_wishlist/<int:listing_id>')
@login_required
def add_to_wishlist(listing_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if not wishlist_item:
        wishlist_item = Wishlist(user_id=current_user.id, listing_id=listing_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Added to wishlist!', 'success')
    else:
        flash('Already in wishlist!', 'info')
    return redirect(url_for('home'))

@app.route('/remove_from_wishlist/<int:listing_id>')
@login_required
def remove_from_wishlist(listing_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Removed from wishlist!', 'success')
    return redirect(url_for('wishlist'))

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    listings = [HouseListing.query.get(item.listing_id) for item in wishlist_items]
    return render_template('wishlist.html', listings=listings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

