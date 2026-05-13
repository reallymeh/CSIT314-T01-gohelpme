# FRA Boundary
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from typing import List
from users.control.fundraiserc import CreateFRAController, DisplayFRAController, ViewFRAController, UpdateFRAController, SuspendFRAController, SearchFRAController, SearchCompletedFRAHistoryController, ViewCompletedFRAController, ViewFRAShortlistCountController, ViewFRAViewStatsController
from users.entity.fracategory import FRACategory


fundraiser_bp = Blueprint('fundraiser', __name__, url_prefix='/fundraiser')


def get_fundraiser_email():
    """Returns the logged-in fundraiser's email from session, or None."""
    return session.get('email_address')


def require_fundraiser_login():
    """Redirect to login if no session. Returns None when session is valid."""
    if not get_fundraiser_email():
        return redirect(url_for('user.show_login'))
    return None


'''
User Story #344: As a Fund Raiser, I want to view all FRAs so that I can view many FRAs at the same time.
'''
# Link to Fund Raiser Homepage
@fundraiser_bp.route('/homepage', methods=['GET'])
def homepage():
    guard = require_fundraiser_login()
    if guard:
        return guard
    boundary = DisplayFRAPage()
    fra_data = boundary.displayFRA()
    message = request.args.get('message')

    return render_template('fundraiser/FundRaiserHomePage.html', fra_data=fra_data, message=message)

class DisplayFRAPage:
    def __init__(self):
        self.controller = DisplayFRAController()

    def displayFRA(self):
        return self.controller.displayFRA()

    
'''
User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
'''
# Link to Create FRA page once clicked on "Create FRA" button
@fundraiser_bp.route('/create', methods=['GET'])
def show_create_fra():
    guard = require_fundraiser_login()
    if guard:
        return guard
    categories = [c.category_name for c in FRACategory.getAllCategory() if c.status == 1]
    return render_template('fundraiser/FundRaiserCreateFRA.html', categories=categories)

class CreateFRAPage:
    def __init__(self):
        self.controller = CreateFRAController()

    def createFRA(self, title: str, description: str, category: str,
                target_amount: int, start_date: str, end_date: str,
                status: int, location: str) -> bool:
        
        created_by = session.get("email_address") 
        
        return self.controller.createFRA(title, description, category, target_amount, 
                                        start_date, end_date, status, location, created_by)

    def displaySuccess(self) -> str: 
        return "Success: FRA created successfully."

    def displayError(self) -> str:
        return "Something went wrong."

# Link to Create FRA function once clicked on "Create FRA" button
@fundraiser_bp.route('/create', methods=['POST'])
def create_fra():
    guard = require_fundraiser_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()

    boundary = CreateFRAPage()
    success = boundary.createFRA(
        data['title'],
        data['description'],
        data['category'],
        int(data['target_amount']),
        data['start_date'],
        data['end_date'],
        int(data['status']),
        data['location']
    )

    message = boundary.displaySuccess() if success else boundary.displayError()

    return jsonify({
        "success": success,
        "message": message
    })


'''
User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
'''
class ViewFRAPage:

    def __init__(self):
        self.controller = ViewFRAController()

    def displayFRA(self, fraId: str):    
        fra = self.controller.viewFRA(fraId)

        if fra:
            return fra
        else:
            return None

    
# Link to View FRA page once clicked on "View" button for each FRA in the Fund Raiser Homepage
@fundraiser_bp.route('/view/<fraId>', methods=['GET'])
def view_fra(fraId):
    guard = require_fundraiser_login()
    if guard:
        return guard
    page = ViewFRAPage()
    fra = page.displayFRA(fraId)
    
    return render_template('fundraiser/FundRaiserViewFRA.html', fra=fra)

    
'''
User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
'''
# Show Update FRA page once clicked on "Update" button for each FRA in the Fund Raiser Homepage
@fundraiser_bp.route('/update/<fraId>', methods=['GET'])
def show_update_page(fraId):
    guard = require_fundraiser_login()
    if guard:
        return guard
    page = ViewFRAPage()
    fra = page.displayFRA(fraId)
    categories = [c.category_name for c in FRACategory.getAllCategory() if c.status == 1]
    
    return render_template('fundraiser/FundRaiserUpdateFRA.html', fra=fra, categories=categories)
    
class UpdateFRAPage:
    def __init__(self):
        self.controller = UpdateFRAController()
    
    def updateFRA(self, fraId: str, title: str, description: str, category: str,
                  target_amount: int, start_date: str, end_date: str, location: str) -> bool:

        return self.controller.updateFRA(
            fraId, title, description, category,
            target_amount, start_date, end_date, location)
        
    def displaySuccess(self) -> str:
        return "Success: FRA updated successfully."

    def displayError(self) -> str:
        return "Update failed."

@fundraiser_bp.route('/update', methods=['POST'])
def update_fra():
    guard = require_fundraiser_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    page = UpdateFRAPage()

    success = page.updateFRA(
        fraId=data['fraId'],
        title=data['title'],
        description=data['description'],
        category=data['category'],
        target_amount=int(data['target_amount']),
        start_date=data['start_date'],
        end_date=data['end_date'],
        location=data['location']
    )

    message = page.displaySuccess() if success else page.displayError()

    return jsonify({
        "success": success,
        "message": message
    })


'''
User Story #18: As a Fund Raiser, I want to suspend a FRA so that I can stop the fund raising activity.
'''
class SuspendFRAPage:

    def __init__(self):
        self.controller = SuspendFRAController()

    def suspendFRA(self, fraId: str) -> bool:
        return self.controller.suspendFRA(fraId)

    def displaySuccess(self) -> str:
        return "FRA suspended successfully!"

    def displayError(self) -> str:
        return "Failed to suspend FRA"
    
@fundraiser_bp.route('/suspend/<fraId>', methods=['POST'])
def suspend_fra(fraId):
    guard = require_fundraiser_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    page = SuspendFRAPage()
    success = page.suspendFRA(fraId)
    message = page.displaySuccess() if success else page.displayError()

    return jsonify({
        "success": success,
        "message": message
    })


'''
User Story #19: As a Fund Raiser, I want to search a FRA so that I can manage and update specific FRA efficiently.
'''
class SearchFRAPage:

    def __init__(self):
        self.controller = SearchFRAController()

    def searchFRA(self, name: str) -> list:
        return self.controller.searchFRA(name)

    def displayNoResult(self) -> str:
        return "No FRA found"

@fundraiser_bp.route('/search', methods=['POST'])
def search_fra():
    guard = require_fundraiser_login()
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

'''
User Story #20: As a Fund Raiser,I want to view the number of views of a FRA so that I can analyze the view of a FRA and adjust my strategy to attract more donees.
'''
class ViewFRAViewCountPage:
    def __init__(self):
        self.stats_controller = ViewFRAViewStatsController()
    def getStats(self, fraId):
        stats = self.stats_controller.getStats(fraId)
        total_views = sum(stat['count'] for stat in stats) if stats else 0
        return {
            "stats": stats,
            "total_views": total_views
        }
    
@fundraiser_bp.route('/viewCount/<fraId>', methods=['GET'])
def view_fra_view_count(fraId):
    guard = require_fundraiser_login()
    if guard:
        return guard
    page = ViewFRAViewCountPage()
    data = page.getStats(fraId)
    return render_template(
        "fundraiser/FundRaiserViewFRAViewCount.html",
        stats=data["stats"],
        total_views=data["total_views"]
    )
'''
User Story #21: As a Fund Raiser, I want to view the number of times a FRA is shortlisted so that I can know how many people are interested in this FRA.
'''
class ViewFRAShortlistCountPage:
    def __init__(self):
        self.controller = ViewFRAShortlistCountController()

    def getFRAShortlistCount(self, fraId):
        return self.controller.getFRAShortlistCount(fraId)
    
@fundraiser_bp.route('/shortlistCount/<fraId>', methods=['GET'])
def view_fra_shortlist_count(fraId):
    guard = require_fundraiser_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    page = ViewFRAShortlistCountPage()
    shortlist_count = page.getFRAShortlistCount(fraId)

    return jsonify({
        "success": True,
        "shortlist_count": shortlist_count
    })


''' 
User Story #22: As a Fund Raiser, I want to search history of completed FRA by service category and date period so that I can search for the past FRA that is completed.
'''
@fundraiser_bp.route('/history', methods=['GET'])
def view_history():
    guard = require_fundraiser_login()
    if guard:
        return guard
    categories = [c.category_name for c in FRACategory.getAllCategory() if c.status == 1]
    return render_template('fundraiser/FundRaiserHistory.html',categories=categories)

class SearchCompletedFRAHistoryPage: 
    def __init__(self): 
        self.controller = SearchCompletedFRAHistoryController()
    
    def searchCompletedFRAHistory(self, category, start_date, end_date):
        return self.controller.searchCompletedFRAHistory(category, start_date, end_date)
    def displaySearchFailed(self):
        return "No results found."

@fundraiser_bp.route('/history/search', methods=['POST'])
def search_completed_fra_history():
    guard = require_fundraiser_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    category = data.get('category', '')
    start_date = data.get('date_from', '')
    end_date = data.get('date_to', '')

    page = SearchCompletedFRAHistoryPage()
    if not category or not start_date or not end_date:
      return jsonify({
        "success": True,
        "data": [],
        "message": "Please select all filters"
    })
    results = page.searchCompletedFRAHistory(category, start_date, end_date)
    return jsonify({
        "success": True,
        "data": results,
        "message": "" if results else page.displaySearchFailed()
    })
  
  
'''
User Story #23: As a Fund Raiser, I want to view the history of completed FRA by service category and date period so that I can review how the past FRA has progressed.
'''
class ViewCompletedFRAPage:
    def __init__(self):
        self.controller = ViewCompletedFRAController()

    def viewCompletedFRA(self, fraId):
        return self.controller.viewCompletedFRA(fraId)

@fundraiser_bp.route('/viewCompleted/<fraId>', methods=['GET'])
def view_comopleted_fra(fraId):
    guard = require_fundraiser_login()
    if guard:
        return guard
    page = ViewCompletedFRAPage()
    fra = page.viewCompletedFRA(fraId)

    return render_template('fundraiser/FundRaiserViewCompletedFRA.html', fra=fra)

