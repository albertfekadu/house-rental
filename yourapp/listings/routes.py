from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from yourapp.forms import AddListingForm  # Updated import
from ..models import HouseListing, Wishlist, db  # Updated import
import os
from werkzeug.utils import secure_filename

listings_bp = Blueprint('listings', __name__)

LISTINGS_PER_PAGE = 6

@listings_bp.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    listings = HouseListing.query.paginate(page=page, per_page=LISTINGS_PER_PAGE)
    return render_template('listings/index.html', listings=listings)

@listings_bp.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    form = AddListingForm()
    if form.validate_on_submit():
        # ... add listing logic ...
        return redirect(url_for('listings.home'))
    return render_template('listings/add_listing.html', form=form)

# ... other listing routes ...