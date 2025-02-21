# House Rental Web Application

## 1. Project Overview

This House Rental web application allows users to post, search, and manage house listings for rent. Features include user registration, authentication, listing creation, advanced search (with filters for price and location), wishlist management, comparison of listings, and an admin dashboard for approving or rejecting listings.

## 2. How to Set Up and Run the Project

### 2.1 Installation Instructions

#### 2.1.1. **Install Python 3**
You need python 3 to run this project.

#### 2.1.2. **Create and Activate a Virtual Environment**

- On macOS/Linux:
```
python3 -m venv houserentalenv
source houserentalenv/bin/activate
```

- On Windows:
```
python -m venv houserentalenv
houserentalenv\Scripts\activate
```

#### 2.1.3. **Install Dependencies**
```
pip install -r requirements.txt
```
This installs Flask, Flask-SQLAlchemy and other required packages.

#### 2.1.4. **Set Up Environment**
- The project uses sqlite database file found in the project folder. This is specified in the application code and doesn't need any further setup.
- For file uploads the project saves uploaded files in the /static/uploads folder.

#### 2.1.5. **Initialize the Database**
- The database tables are created on first run if they don’t exist.
- Ensure that `house_rental.db` is accessible (or that your custom DB is configured).

#### 2.1.6. **Run the Application**
```
python app.py
```
By default, the app runs in debug mode on [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 3. Code structure

house-rental/
│
├── .env                        # Environment variables (not included in version control)
├── .vscode/                    # VSCode workspace settings (optional)
│   └── settings.json
├── houserentalenv/             # Virtual environment folder (optional)
├── instance/                   # Contains instance-specific files (optional)
│   └── config.py
├── static/
│   ├── css/
│   │   └── style.css           # Custom CSS file
│   ├── images/
│   └── js/
├── uploads/                    # Stores uploaded images and screenshots
├── templates/
│   ├── add_listing.html        # Form for creating a new listing
│   ├── admin_dashboard.html    # Admin overview, unapproved listings, revenue, etc.
│   ├── base.html               # Base template with navbar and structure
│   ├── compare.html            # Compare multiple listings side by side
│   ├── edit_listing.html       # Edit form for an existing listing
│   ├── index.html              # Homepage with featured listings and compare option
│   ├── listing.html            # Detailed view of a single house listing
│   ├── login.html              # User login form
│   ├── register.html           # User registration form
│   ├── search.html             # Search results page
│   ├── wishlist.html           # Displays user’s wishlist
│   └── ...
├── yourapp/
│   ├── __init__.py             # Initialize the Flask app
│   ├── auth.py                 # Authentication logic
│   ├── forms.py                # WTForms definitions
│   ├── routes.py               # Separate routes for better organization
│   ├── listings.py             # Separate listing logic
│   └── models.py               # Database models
├── app.py                      # Main Flask application file, routes, and models
├── config.py                   # Configuration settings (e.g., database, secret key)
├── house_rental.db             # SQLite database (generated at runtime if not existing)
├── package.json                # (If used for front-end dependencies or node scripts)
├── requirements.txt            # Python dependencies
└── PROJECT_TREE.md             # (Optional doc explaining the file structure)
## 4. User Guide

### 4.1 Registration and Login
- **Register:** Click the “Register” link in the navbar to create a new account (username, email, and password).
- **Login:** Use the “Login” link to sign in with your credentials.

### 4.2 Browsing Listings
- **Homepage (/):** Displays a paginated list of active listings (approved by an admin or paid by the user).
- **Search:** Use the navbar search bar to filter listings by keywords, min price, and max price. Results are displayed in `search.html`.

### 4.3 Creating a New Listing
1. Navigate to the “Add Listing” page (only available to logged-in users).
2. Fill out the form with details such as title, price, location, number of rooms, amenities, contact info, and image uploads.
3. **Payment:** Non-admin users must pay a fee (e.g., 500 birr) and provide a payment screenshot.
4. **Submit:** The listing appears immediately for admins, while non-admin listings need admin approval.

### 4.4 Editing and Deleting Listings
- Listing owners or admins can edit or delete listings from the listing detail page (`/listing/<id>`).
- Admins can modify or delete any listing.

### 4.5 Admin Dashboard
- **Access:** Restricted to admin users at `/admin_dashboard`.
- **Features:**
  - View the count of active listings and the associated revenue (500 birr per approved listing).
  - Monitor top recent searches and their counts.
  - Approve or delete pending listings.

### 4.6 Listing Details 
- **Images:**  Show the list of available images in a grid with the ability to open the image to see in better detail.
- **Details:** Shows the details of the listing in a neatly organized manner.
- **Map:** Shows the approximate location of the listing in a map using Leaflet and Open Street Maps.

### 4.7 Comparing Listings (Bonus)
- Select multiple listings using “Compare” checkboxes on the homepage or search results page.
- Click “Compare Selected” to view them side by side in `compare.html`.

### 4.8 Wishlist (Bonus)
- Add listings to your wishlist via the “Wishlist” button on the homepage or listing page.
- Access and manage your wishlist through the navbar.

### 4.9 Review and Rating
- Add a rating and review to a listing

### 4.10 Additional Features
- **Pagination:** Available on the homepage and search pages.
- **Search Trends:** Records each search query for analysis.
- **File Uploads:** Uploaded images and screenshots are stored in `static/uploads`.

  
