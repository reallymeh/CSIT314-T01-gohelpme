# Donee Boundary
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from users.control.doneec import (
    SearchFRAController,
    ViewFRAController,
    SaveFavouriteController,
    SearchFavouriteController,
    ViewFavouriteListController,
    SearchDonationHistoryController,
    ViewDonationHistoryController,
)

donee_bp = Blueprint('donee', __name__, url_prefix='/donee')


def get_donee_email():
    """Helper — returns the logged-in donee's email from session, or None."""
    return session.get('email_address')


def require_donee_login():
    """Redirect to login if no session. Returns None when session is valid."""
    if not get_donee_email():
        return redirect(url_for('user.show_login'))
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  US1 — Search all FRA by name
# ─────────────────────────────────────────────────────────────────────────────

class SearchFRAPage:
    '''
    Boundary: SearchFRAPage
    User Story #1: As a Donee, I want to search all FRA by name
    so that I can find a specific FRA that I am interested in.
    Sequence: Donee searches → SearchFRAPage(Boundary)
              → SearchFRAController(Controller) → FRA(Entity)
    '''
    def __init__(self):
        self.controller = SearchFRAController()

    def searchFRA(self, name: str) -> list:
        return self.controller.searchFRA(name)

    def displayNoResult(self) -> str:
        return "No active fundraising activities found."


@donee_bp.route('/homepage', methods=['GET'])
def homepage():
    """Render the Donee homepage (search all FRAs — US1 entry point)."""
    guard = require_donee_login()
    if guard:
        return guard
    return render_template('DoneeHomePage.html')


@donee_bp.route('/api/search_fra', methods=['POST'])
def api_search_fra():
    """
    API: POST /donee/api/search_fra
    Body: { "name": "<search term>" }
    Returns JSON list of active FRAs matching the name.
    US1 — SearchFRAPage → SearchFRAController → FRA.searchActiveFRA()
    """
    guard = require_donee_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json()
    name = data.get('name', '')

    page = SearchFRAPage()
    results = page.searchFRA(name)

    return jsonify({
        "success": True,
        "data": results,
        "message": "" if results else page.displayNoResult()
    })


# ─────────────────────────────────────────────────────────────────────────────
#  US2 — View a FRA
# ─────────────────────────────────────────────────────────────────────────────

class ViewFRAPage:
    '''
    Boundary: ViewFRAPage
    User Story #2: As a Donee, I want to view a FRA
    so that I can view existing FRA information that needs donation.
    Sequence: Donee clicks View → ViewFRAPage(Boundary)
              → ViewFRAController(Controller) → FRA(Entity)
    '''
    def __init__(self):
        self.controller = ViewFRAController()
        self.fav_controller = SaveFavouriteController()

    def displayFRA(self, fraId: str) -> dict | None:
        fra = self.controller.viewFRA(fraId)
        return fra

    def displayError(self) -> str:
        return "FRA not found."


@donee_bp.route('/view/<fraId>', methods=['GET'])
def view_fra(fraId):
    """
    Render the View FRA detail page.
    Also passes is_favourited flag so the Save button shows correct state (US3).
    US2 — ViewFRAPage → ViewFRAController → FRA.viewFRA()
    """
    guard = require_donee_login()
    if guard:
        return guard

    donee_email = get_donee_email()
    page = ViewFRAPage()
    fra = page.displayFRA(fraId)

    if not fra:
        return redirect(url_for('donee.homepage'))

    is_fav = page.fav_controller.isFavourited(donee_email, fraId)
    return render_template('DoneeViewFRA.html', fra=fra, is_favourited=is_fav)


# ─────────────────────────────────────────────────────────────────────────────
#  US3 — Save a FRA to favourite list
# ─────────────────────────────────────────────────────────────────────────────

class SaveFavouritePage:
    '''
    Boundary: SaveFavouritePage
    User Story #3: As a Donee, I want to save a FRA to favourite list
    so that I can decide a donation later.
    Sequence: Donee clicks Save → SaveFavouritePage(Boundary)
              → SaveFavouriteController(Controller) → Favourite(Entity)
    '''
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
    API: POST /donee/save_favourite
    Body: { "fraId": "<FRA001>" }
    US3 — SaveFavouritePage → SaveFavouriteController → Favourite.saveFavourite()
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

    # Check duplicate before attempting save
    if page.controller.isFavourited(donee_email, fraId):
        return jsonify({"success": False, "message": page.displayAlreadySaved()})

    saved = page.saveFavourite(donee_email, fraId)
    message = page.displaySuccess() if saved else page.displayError()

    return jsonify({"success": saved, "message": message})


# ─────────────────────────────────────────────────────────────────────────────
#  US4 — Search FRA in favourite list by name
#  US5 — View all FRA in favourite list
# ─────────────────────────────────────────────────────────────────────────────

class SearchFavouritePage:
    '''
    Boundary: SearchFavouritePage
    User Story #4: As a Donee, I want to search FRA in favourite list by name.
    User Story #5: As a Donee, I want to view FRA in favourite list.
    Sequence: Donee searches/views → SearchFavouritePage(Boundary)
              → SearchFavouriteController / ViewFavouriteListController
              → Favourite(Entity)
    '''
    def __init__(self):
        self.search_controller  = SearchFavouriteController()
        self.view_controller    = ViewFavouriteListController()

    def searchFavourites(self, donee_email: str, name: str) -> list:
        return self.search_controller.searchFavourites(donee_email, name)

    def viewFavourites(self, donee_email: str) -> list:
        return self.view_controller.viewFavourites(donee_email)

    def displayNoResult(self) -> str:
        return "No favourites found matching your search."

    def displayEmpty(self) -> str:
        return "You have not saved any FRAs to your favourites yet."


@donee_bp.route('/favourites', methods=['GET'])
def favourites():
    """Render the Favourites page (US4 + US5 entry point)."""
    guard = require_donee_login()
    if guard:
        return guard
    return render_template('DoneeFavourites.html')


@donee_bp.route('/api/search_favourites', methods=['POST'])
def api_search_favourites():
    """
    API: POST /donee/api/search_favourites
    Body: { "name": "<search term>" }   — empty name returns all (US5 view)
    US4/US5 — SearchFavouritePage → SearchFavouriteController → Favourite.searchFavourites()
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
        "data": results,
        "message": "" if results else (
            page.displayNoResult() if name else page.displayEmpty()
        )
    })


# ─────────────────────────────────────────────────────────────────────────────
#  US6 — Search history of donation by FRA category and date period
#  US7 — View history of donation
# ─────────────────────────────────────────────────────────────────────────────

class SearchDonationHistoryPage:
    '''
    Boundary: SearchDonationHistoryPage
    User Story #6: As a Donee, I want to search history of donation by FRA category and date period.
    User Story #7: As a Donee, I want to view history of donation.
    Sequence: Donee filters/views → SearchDonationHistoryPage(Boundary)
              → SearchDonationHistoryController / ViewDonationHistoryController
              → DonationHistory(Entity)
    '''
    def __init__(self):
        self.search_controller = SearchDonationHistoryController()
        self.view_controller   = ViewDonationHistoryController()

    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list:
        return self.search_controller.searchHistory(donee_email, category, date_from, date_to)

    def viewHistory(self, donee_email: str) -> list:
        return self.view_controller.viewHistory(donee_email)

    def getCategories(self, donee_email: str) -> list:
        return self.search_controller.getCategories(donee_email)

    def displayNoResult(self) -> str:
        return "No donation records found for the selected filters."

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
    categories = page.getCategories(donee_email)
    return render_template('DoneeDonationHistory.html', categories=categories)


@donee_bp.route('/api/search_history', methods=['POST'])
def api_search_history():
    """
    API: POST /donee/api/search_history
    Body: { "category": "", "date_from": "YYYY-MM-DD", "date_to": "YYYY-MM-DD" }
    All fields optional — omitting all is equivalent to US7 (view all).
    US6/US7 — SearchDonationHistoryPage → SearchDonationHistoryController
              → DonationHistory.searchHistory()
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
        "data": results,
        "message": "" if results else (
            page.displayNoResult() if (category or date_from or date_to)
            else page.displayEmpty()
        )
    })
