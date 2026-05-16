from users.control.platform_managerc import CreateFRACategoryController, ViewFRACategoryController, UpdateFRACategoryController, ViewAllFRACategoryController, SearchFRACategoryController, SuspendFRACategoryController, DailyReportController, WeeklyReportController, MonthlyReportController
from users.entity.fracategory import FRACategory
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

from typing import List, Dict, Any

platform_manager_bp = Blueprint('platform_manager', __name__, url_prefix='/manager')


def get_manager_email():
    """Returns the logged-in platform manager's email from session, or None."""
    return session.get('email_address')


def require_manager_login():
    """Redirect to login if no session. Returns None when session is valid."""
    if not get_manager_email():
        return redirect(url_for('user.show_login'))
    return None


'''
User Story #35: As a platform manager, I want to create FRA categories so that I can create a new category for FRA.
'''
class CreateFRACategoryBoundary:
    def __init__(self):
        self.controller = CreateFRACategoryController()

    def createFRACategory(self, cat_name: str, description: str, status: int) -> bool:
        return self.controller.createFRACategory(cat_name, description, status)

    def displaySuccess(self):
        return 'Category created successfully!'

    def displayFailure(self):
        return 'Failed to create category. Category may already exist.'

@platform_manager_bp.route('/create_category', methods=['GET'])
def show_create_category():
    guard = require_manager_login()
    if guard:
        return guard
    return render_template('platform_manager/PlatformManagerCreateCategory.html')

@platform_manager_bp.route('/create_category', methods=['POST'])
def create_category():
    guard = require_manager_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    status = int(data.get('status', 1))

    boundary = CreateFRACategoryBoundary()
    if boundary.createFRACategory(name, description, status):
        return jsonify({'success': True, 'message': boundary.displaySuccess()})
    else:
        return jsonify({'success': False, 'message': boundary.displayFailure()})


'''
User Story #36: As a platform manager, I want to view FRA categories so that I can view the FRA categories I created.
'''
class ViewFRACategoryBoundary:
    def __init__(self):
        self.controller = ViewFRACategoryController()

    # viewFRACategory(): FRACategory — receives category_name and returns FRACategory from controller
    def viewFRACategory(self, category_name: str) -> FRACategory | None:
        return self.controller.viewFRACategory(category_name)

@platform_manager_bp.route('/viewcategory/<category_name>', methods=['GET'])
def view_category(category_name):
    guard = require_manager_login()
    if guard:
        return guard
    category = ViewFRACategoryBoundary().viewFRACategory(category_name)
    # BCE BOUNDARY: displayViewResult() — Flask renders category details via Jinja2
    return render_template('platform_manager/PlatformManagerViewCategory.html', category=category)


'''
User Story #37: As a platform manager, I want to update FRA categories so that I can ensure the information is latest.
'''
# 1. Replace hardcoded return with real category data pre-filled
# 2. Add POST route to process update
# category = ViewFRACategoryBoundary().viewFRACategory(category_name)
# return render_template('PlatformManagerUpdateCategory.html', category=category)

class UpdateFRACategoryBoundary:
    def __init__(self):
        self.controller = UpdateFRACategoryController()
    
    def displayUpdateSuccess(self):
        message = "Update Successful!"
        return {"success": True, "message": message}

    def displayUpdateFail(self):
        message = "Update Failed!"
        return {"success": False, "message": message}
    
    def updateFRACategory(self, old_name:str, new_name:str, description: str, status:int) -> dict:
        if self.controller.updateFRACategory(old_name, new_name, description, status):
            return self.displayUpdateSuccess()
        
        else:
            return self.displayUpdateFail()

@platform_manager_bp.route('/updatecategory/<category_name>', methods=['GET'])
def update_category(category_name):
    guard = require_manager_login()
    if guard:
        return guard
    boundary = UpdateFRACategoryBoundary()
    category = ViewFRACategoryController().viewFRACategory(category_name)
    
    if category is None:
        return "Category not found", 404
    
    # Pass the category object to the template
    return render_template(
        'platform_manager/PlatformManagerUpdateCategory.html',
        category=category
    )

@platform_manager_bp.route('/updatecategory/<category_name>', methods=['POST'])
def update_category_post(category_name):
    guard = require_manager_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    boundary = UpdateFRACategoryBoundary()
    
    data = request.get_json()
    
    new_name = data.get('new_name')
    description = data.get('description')
    status = data.get('status')
    
    result = boundary.updateFRACategory(
        old_name=category_name,
        new_name=new_name,
        description=description,
        status=status
    )
    
    return jsonify(result)


'''
Not in user stories, but needed for the platform manager to view the list of FRA categories and manage them.
'''
class ViewAllFRACategoryBoundary:
    def __init__(self):
        self.controller = ViewAllFRACategoryController()
    
    def viewAllFRACategory(self):
        return self.controller.viewAllFRACategory()
    
@platform_manager_bp.route('/categories', methods=['GET'])
def view_all_category():
    guard = require_manager_login()
    if guard:
        return guard
    boundary = ViewAllFRACategoryBoundary()
    categories = boundary.viewAllFRACategory()
    
    return render_template('platform_manager/PlatformManagerCategories.html', categories=categories)


'''
User Story #38: As a platform manager, I want to suspend FRA categories so that I can make it easier for users to navigate the platform.
'''   
class SuspendFRACategoryBoundary:
    def __init__(self):
        self.controller = SuspendFRACategoryController()

    def displaySuspendSuccess(self) -> str:
        return 'Category suspended successfully!'

    def displaySuspendFail(self) -> str:
        return 'Failed to suspend category. Category may already be suspended or does not exist.'

    def suspendFRACategory(self, category_name: str) -> bool:
        return self.controller.suspendFRACategory(category_name)

@platform_manager_bp.route('/suspend_category', methods=['POST'])
def suspend_category():
    guard = require_manager_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    category_name = data.get('category_name', '').strip()

    boundary = SuspendFRACategoryBoundary()
    if boundary.suspendFRACategory(category_name):
        return jsonify({'success': True, 'message': boundary.displaySuspendSuccess()})
    else:
        return jsonify({'success': False, 'message': boundary.displaySuspendFail()})
    

'''
User Story #39: As a platform manager, I want to search FRA categories so that I can filter the current FRA categories the platform has.
'''
class SearchFRACategory:
    def __init__(self):
        self.controller = SearchFRACategoryController()
    
    def searchFRACategory(self, query:str) -> List["FRACategory"]:
        return self.controller.searchFRACategory(query)

@platform_manager_bp.route('/search_categories', methods=['GET'])
def search_categories():
    guard = require_manager_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    query = request.args.get('q', '').strip().lower()
    
    boundary = SearchFRACategory()
    results = boundary.searchFRACategory(query)
    
    data = [
        {
            "category_name": cat.category_name, 
            "description": getattr(cat, 'description', ''),
            "status": getattr(cat, 'status', 1)
        }
        for cat in results
    ]
    
    return jsonify(data)


# ========== BCE BOUNDARY: GenerateReport ==========
# User Stories: #40 Daily, #41 Weekly, #42 Monthly

@platform_manager_bp.route('/reports', methods=['GET'])
def show_reports():
    guard = require_manager_login()
    if guard:
        return guard
    return render_template('platform_manager/PlatformManagerReports.html')

"""
User Story #40: As a platform manager, I want to generate a daily report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class DailyReportBoundary:
    """
    Boundary: GenerateDailyReport
    Sequence: Platform Manager → GenerateDailyReport → DailyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = DailyReportController()

    def generateDailyReport(self) -> Dict[str, Any]:
        return self.controller.generateDailyReport()

@platform_manager_bp.route('/reports/daily', methods=['GET'])
def daily_report():
    guard = require_manager_login()
    if guard:
        return guard
    boundary = DailyReportBoundary()
    daily = boundary.generateDailyReport()
    return render_template('platform_manager/PlatformManagerDailyReport.html', daily=daily)


"""
User Story #41: As a platform manager, I want to generate a weekly report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class WeeklyReportBoundary:
    """
    Boundary: GenerateWeeklyReport
    Sequence: Platform Manager → GenerateWeeklyReport → WeeklyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = WeeklyReportController()

    def generateWeeklyReport(self) -> Dict[str, Any]:
        return self.controller.generateWeeklyReport()

@platform_manager_bp.route('/reports/weekly', methods=['GET'])
def weekly_report():
    guard = require_manager_login()
    if guard:
        return guard
    boundary = WeeklyReportBoundary()
    weekly = boundary.generateWeeklyReport()
    return render_template('platform_manager/PlatformManagerWeeklyReport.html', weekly=weekly)


"""
User Story #42: As a platform manager, I want to generate a monthly report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class MonthlyReportBoundary:
    """
    Boundary: GenerateMonthlyReport
    Sequence: Platform Manager → GenerateMonthlyReport → MonthlyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = MonthlyReportController()

    def generateMonthlyReport(self) -> Dict[str, Any]:
        return self.controller.generateMonthlyReport()

@platform_manager_bp.route('/reports/monthly', methods=['GET'])
def monthly_report():
    guard = require_manager_login()
    if guard:
        return guard
    boundary = MonthlyReportBoundary()
    monthly = boundary.generateMonthlyReport()
    return render_template('platform_manager/PlatformManagerMonthlyReport.html', monthly=monthly)