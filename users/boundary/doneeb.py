# Donee Boundary
from dataclasses import asdict
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from users.control.doneec import (
    ViewAllFRAController,
    SearchActiveFRAController,
    ViewActiveFRAController,
    SaveFavouriteController,
    RemoveFavouriteController,
    ViewFavouriteController,
    SearchFavouriteController,
    ViewDonationHistoryController,
    SearchDonationHistoryController,
)
from users.control.fundraiserc import ViewFRAViewStatsController
# Entity imports (for type hints and asdict)
from users.entity.fra import FRA
from users.entity.favourite import Favourite
from users.entity.donationhistory import DonationHistory

donee_bp = Blueprint('donee', __name__, url_prefix='/donee')


def get_donee_email():
    """Returns the logged-in donee's email from session, or None."""
    return session.get('email_address')


def require_donee_login():
    """Redirect to login if no session. Returns None when session is valid."""
    if not get_donee_email():
        return redirect(url_for('user.show_login'))
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  Donee Dashboard (view all active FRAs)
# ─────────────────────────────────────────────────────────────────────────────

class ViewAllFRAPage:
    def __init__(self):
        self.controller = ViewAllFRAController()

    def displayAllFRA(self) -> list[FRA]:
        return self.controller.viewAllFRA()

    def displayNoResult(self) -> str:
        return "There are currently no active fundraising activities."


@donee_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Render the Donee dashboard"""
    guard = require_donee_login()
    if guard:
        return guard
    return render_template('donee/DoneeHomePage.html')


@donee_bp.route('/api/view_all_fra', methods=['GET'])
def api_view_all_fra():
    """API: GET /donee/api/view_all_fra"""
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    page = ViewAllFRAPage()
    results = page.displayAllFRA()

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayNoResult()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #26 — Search all active FRAs by name
# ─────────────────────────────────────────────────────────────────────────────

class SearchActiveFRAPage:
    """
    Boundary: SearchActiveFRAPage
    User Story #26 (Donee): As a Donee, I want to search all active FRA by name 
    so that I can find a specific FRA that I am interested in.
    Sequence: Donee → SearchActiveFRAPage → SearchActiveFRAController → FRA
    """
    def __init__(self):
        self.controller = SearchActiveFRAController()

    def searchActiveFRA(self, name: str) -> list[FRA]:
        return self.controller.searchActiveFRA(name)

    def displayNoResult(self) -> str:
        return "No active fundraising activities found."


@donee_bp.route('/api/search_fra', methods=['POST'])
def api_search_fra():
    """
    API: POST /donee/api/search_fra   Body: { "name": "<search term>" }
    US26 — SearchActiveFRAPage → SearchActiveFRAController → FRA.searchActiveFRA()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json()
    name = data.get('name', '')

    page = SearchActiveFRAPage()
    results = page.searchActiveFRA(name)

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayNoResult()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #27 — View a FRA
# ─────────────────────────────────────────────────────────────────────────────

class ViewActiveFRAPage:
    """
    Boundary: ViewActiveFRAPage
    User Story #27 (Donee): As a Donee, I want to view an active FRA 
    so that I can view existing FRA information that needs donation.
    Sequence: Donee → ViewActiveFRAPage → ViewActiveFRAController → FRA
    """
    def __init__(self):
        self.controller = ViewActiveFRAController()
        self.fav_controller = SaveFavouriteController()

    def viewActiveFRA(self, fraId: str) -> FRA | None:
        return self.controller.viewActiveFRA(fraId)

    def displayError(self) -> str:
        return "FRA not found."


@donee_bp.route('/view/<fraId>', methods=['GET'])
def view_fra(fraId):
    """
    Render the FRA detail page.
    Passes is_favourited flag so the Save button shows the correct state (US28).
    US27 — ViewActiveFRAPage → ViewActiveFRAController → FRA.viewActiveFRA()
    """
    guard = require_donee_login()
    if guard:
        return guard

    donee_email = get_donee_email()
    page = ViewActiveFRAPage()
    fra = page.viewActiveFRA(fraId)

    if not fra:
        return redirect(url_for('donee.dashboard'))

    ViewFRAViewStatsController.recordView(fraId, donee_email, fra.created_by, fra.title, fra.category)

    is_fav = page.fav_controller.isFavourite(donee_email, fraId)
    return render_template('donee/DoneeViewFRA.html', fra=fra, is_favourited=is_fav)


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #28 — Save a FRA to favourite list
# ─────────────────────────────────────────────────────────────────────────────

class SaveFavouritePage:
    """
    Boundary: SaveFavouritePage
    User Story #28 (Donee): As a Donee, I want to save a FRA to my favourite list
    so that I can decide on a donation later.
    Sequence: Donee → SaveFavouritePage → SaveFavouriteController → Favourite
    """
    def __init__(self):
        self.controller = SaveFavouriteController()

    def saveFavourite(self, donee_email: str, fraId: str) -> bool:
        return self.controller.saveFavourite(donee_email, fraId)

    def displaySuccess(self) -> str:
        return "FRA saved to your favourites!"

    def displayAlreadySaved(self) -> str:
        return "This FRA is already in your favourites."

    def displayError(self) -> str:
        return "Failed to save FRA to favourites. Please try again."


@donee_bp.route('/save_favourite', methods=['POST'])
def save_favourite():
    """
    API: POST /donee/save_favourite   Body: { "fraId": "<FRA001>" }
    US28 — SaveFavouritePage → SaveFavouriteController → Favourite.saveFavourite()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    data = request.get_json()
    fraId = data.get('fraId', '').strip()

    if not fraId:
        return jsonify({"success": False, "message": "fraId is required"}), 400

    page = SaveFavouritePage()

    if page.controller.isFavourite(donee_email, fraId):
        return jsonify({"success": False, "message": page.displayAlreadySaved()})

    saved = page.saveFavourite(donee_email, fraId)
    return jsonify({"success": saved, "message": page.displaySuccess() if saved else page.displayError()})


# ─────────────────────────────────────────────────────────────────────────────
# Remove a FRA from favourite list
# ─────────────────────────────────────────────────────────────────────────────

class RemoveFavouritePage:
    def __init__(self):
        self.controller = RemoveFavouriteController()

    def removeFavourite(self, donee_email: str, fraId: str) -> bool:
        return self.controller.removeFavourite(donee_email, fraId)

    def displaySuccess(self) -> str:
        return "FRA removed from your favourites."

    def displayError(self) -> str:
        return "Failed to remove FRA from favourites. Please try again."


@donee_bp.route('/remove_favourite', methods=['POST'])
def remove_favourite():
    """
    API: POST /donee/remove_favourite   Body: { "fraId": "<FRA001>" }
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    data = request.get_json()
    fraId = data.get('fraId', '').strip()

    if not fraId:
        return jsonify({"success": False, "message": "fraId is required"}), 400

    page = RemoveFavouritePage()
    removed = page.removeFavourite(donee_email, fraId)
    return jsonify({"success": removed, "message": page.displaySuccess() if removed else page.displayError()})


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #29 — Search FRA in favourite list by name
# ─────────────────────────────────────────────────────────────────────────────

class SearchFavouritePage:
    """
    Boundary: SearchFavouritePage
    User Story #29 (Donee): As a Donee, I want to search for an active FRA in my favourite list by name 
    so that I can find a specific FRA within the favourite list.
    Sequence: Donee → SearchFavouritePage → SearchFavouriteController → Favourite
    """
    def __init__(self):
        self.controller = SearchFavouriteController()

    def searchFavourites(self, donee_email: str, name: str) -> list[Favourite]:
        return self.controller.searchFavourites(donee_email, name)

    def displayNoResult(self) -> str:
        return "No favourites found matching your search."


@donee_bp.route('/api/search_favourites', methods=['POST'])
def api_search_favourites():
    """
    API: POST /donee/api/search_favourites   Body: { "name": "<search term>" }
    US29 — SearchFavouritePage → SearchFavouriteController → Favourite.searchFavourites()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    data = request.get_json()
    name = data.get('name', '')

    page = SearchFavouritePage()
    results = page.searchFavourites(donee_email, name)

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayNoResult()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #30 — View all FRAs in favourite list
# ─────────────────────────────────────────────────────────────────────────────

class ViewFavouritePage:
    """
    Boundary: ViewFavouritePage
    User Story #30 (Donee): As a Donee, I want to view FRA in my favourite list
    so that I can view all FRA within the favourite list.
    Sequence: Donee → ViewFavouritePage → ViewFavouriteListController → Favourite
    """
    def __init__(self):
        self.controller = ViewFavouriteController()

    def viewFavourites(self, donee_email: str) -> list[Favourite]:
        return self.controller.viewFavourites(donee_email)

    def displayEmpty(self) -> str:
        return "You have not saved any FRAs to your favourites yet."


@donee_bp.route('/favourites', methods=['GET'])
def favourites():
    """Render the Favourites page (US4 + US5 entry point)."""
    guard = require_donee_login()
    if guard:
        return guard
    return render_template('donee/DoneeFavourites.html')


@donee_bp.route('/api/view_favourites', methods=['GET'])
def api_view_favourites():
    """
    API: GET /donee/api/view_favourites
    US30 — ViewFavouritePage → ViewFavouriteListController → Favourite.searchFavourites("")
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    page = ViewFavouritePage()
    results = page.viewFavourites(donee_email)

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayEmpty()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #31 — Search donation history by FRA category and date period
# ─────────────────────────────────────────────────────────────────────────────

class SearchDonationHistoryPage:
    """
    Boundary: SearchDonationHistoryPage
    User Story #31 (Donee): As a Donee, I want to search history of donation by
    FRA category and date period so that I can find a specific FRA I had donated.
    Sequence: Donee → SearchDonationHistoryPage → SearchDonationHistoryController → DonationHistory
    """
    def __init__(self):
        self.controller = SearchDonationHistoryController()

    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list[DonationHistory]:
        return self.controller.searchHistory(donee_email, category, date_from, date_to)

    def displayNoResult(self) -> str:
        return "No donation records found for the selected filters."


@donee_bp.route('/api/search_history', methods=['POST'])
def api_search_history():
    """
    API: POST /donee/api/search_history
    Body: { "category": "", "date_from": "YYYY-MM-DD", "date_to": "YYYY-MM-DD" }
    US31 — SearchDonationHistoryPage → SearchDonationHistoryController → DonationHistory.searchHistory()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    data = request.get_json()
    category  = data.get('category', '')
    date_from = data.get('date_from', '')
    date_to   = data.get('date_to', '')

    page = SearchDonationHistoryPage()
    results = page.searchHistory(donee_email, category, date_from, date_to)

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayNoResult()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  User Story #32 — View all donation history
# ─────────────────────────────────────────────────────────────────────────────

class ViewDonationHistoryPage:
    """
    Boundary: ViewDonationHistoryPage
    User Story #32 (Donee): As a Donee, I want to view the history of donation 
    so that I can evaluate the impact of my donation and consider another donation.
    Sequence: Donee → ViewDonationHistoryPage → ViewDonationHistoryController → DonationHistory
    """
    def __init__(self):
        self.controller = ViewDonationHistoryController()

    def viewHistory(self, donee_email: str) -> list[DonationHistory]:
        return self.controller.viewHistory(donee_email)

    def displayEmpty(self) -> str:
        return "You have no donation history yet."


@donee_bp.route('/donation_history', methods=['GET'])
def donation_history():
    """Render the Donation History page (US6 + US7 entry point)."""
    guard = require_donee_login()
    if guard:
        return guard

    donee_email = get_donee_email()
    page = SearchDonationHistoryPage()
    records = page.searchHistory(donee_email, '', '', '')
    categories = sorted({r.fra_category for r in records})
    return render_template('donee/DoneeDonationHistory.html', categories=categories)


@donee_bp.route('/api/view_history', methods=['GET'])
def api_view_history():
    """
    API: GET /donee/api/view_history
    US32 — ViewDonationHistoryPage → ViewDonationHistoryController → DonationHistory.searchHistory()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    donee_email = get_donee_email()
    page = ViewDonationHistoryPage()
    results = page.viewHistory(donee_email)

    return jsonify({
        "success": True,
        "data": [asdict(r) for r in results],
        "message": "" if results else page.displayEmpty()
    })
