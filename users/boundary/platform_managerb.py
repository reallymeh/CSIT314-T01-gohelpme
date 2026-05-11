from users.control.platform_managerc import CreateFRACategoryController, ViewFRACategoryController, UpdateFRACategoryController, ViewAllFRACategoryController, SearchFRACategoryController, SuspendFRACategoryController, DailyReportController, WeeklyReportController, MonthlyReportController
from users.entity.fracategory import FRACategory
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from typing import List, Dict, Any

platform_manager_bp = Blueprint('platform_manager', __name__, url_prefix='/manager')

# ========== BCE BOUNDARY: CreateFRACategory ==========
# User Story: #35 As a platform management, I want to create FRA categories
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
    return render_template('platform_manager/PlatformManagerCreateCategory.html')

@platform_manager_bp.route('/create_category', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    status = int(data.get('status', 1))

    boundary = CreateFRACategoryBoundary()
    if boundary.createFRACategory(name, description, status):
        return jsonify({'success': True, 'message': boundary.displaySuccess()})
    else:
        return jsonify({'success': False, 'message': boundary.displayFailure()})

# ========== BCE BOUNDARY: ViewFRACategory ==========
# User Story: #36 As a platform management, I want to view FRA categories
class ViewFRACategoryBoundary:
    def __init__(self):
        self.controller = ViewFRACategoryController()

    # viewFRACategory(): FRACategory — receives category_name and returns FRACategory from controller
    def viewFRACategory(self, category_name: str) -> FRACategory | None:
        return self.controller.viewFRACategory(category_name)

@platform_manager_bp.route('/viewcategory/<category_name>', methods=['GET'])
def view_category(category_name):
    category = ViewFRACategoryBoundary().viewFRACategory(category_name)
    # BCE BOUNDARY: displayViewResult() — Flask renders category details via Jinja2
    return render_template('platform_manager/PlatformManagerViewCategory.html', category=category)

# ========== BCE BOUNDARY: UpdateFRACategory ==========
# User Story: #37 As a platform management, I want to update FRA categories
# HARDCODED — backend needs to:
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
    boundary = UpdateFRACategoryBoundary()
    category = FRACategory.getCategory(category_name)
    
    if category is None:
        return "Category not found", 404
    
    # Pass the category object to the template
    return render_template(
        'platform_manager/PlatformManagerUpdateCategory.html',
        category=category
    )

@platform_manager_bp.route('/updatecategory/<category_name>', methods=['POST'])
def update_category_post(category_name):
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

class ViewAllFRACategoryBoundary:
    def __init__(self):
        self.controller = ViewAllFRACategoryController()
    
    def viewAllFRACategory(self):
        return self.controller.viewAllFRACategory()
    
@platform_manager_bp.route('/categories', methods=['GET'])
def view_all_category():
    boundary = ViewAllFRACategoryBoundary()
    categories = boundary.viewAllFRACategory()
    
    return render_template('platform_manager/PlatformManagerCategories.html', categories=categories)

class SearchFRACategory:
    def __init__(self):
        self.controller = SearchFRACategoryController()
    
    def searchFRACategory(self, query:str) -> List["FRACategory"]:
        return self.controller.searchFRACategory(query)

@platform_manager_bp.route('/search_categories', methods=['GET'])
def search_categories():
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

# ========== BCE BOUNDARY: SuspendFRACategory ==========
# User Story: #38 As a platform management, I want to suspend FRA categories
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
    data = request.get_json()
    category_name = data.get('category_name', '').strip()

    boundary = SuspendFRACategoryBoundary()
    if boundary.suspendFRACategory(category_name):
        return jsonify({'success': True, 'message': boundary.displaySuspendSuccess()})
    else:
        return jsonify({'success': False, 'message': boundary.displaySuspendFail()})
    
# ========== BCE BOUNDARY: GenerateReport ==========
# User Stories: #40 Daily, #41 Weekly, #42 Monthly

@platform_manager_bp.route('/reports', methods=['GET'])
def show_reports():
    return render_template('platform_manager/PlatformManagerReports.html')

# ─────────────────────────────────────────────────────────────────────────────
#  User Story #40 — Generate Daily Report
# ─────────────────────────────────────────────────────────────────────────────
class DailyReportBoundary:
    """
    Boundary: GenerateDailyReport
    User Story #40 (Platform Manager): As a platform manager, I want to generate a daily report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    Sequence: Platform Manager → GenerateDailyReport → DailyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = DailyReportController()

    def generateDailyReport(self) -> Dict[str, Any]:
        return self.controller.generateDailyReport()

@platform_manager_bp.route('/reports/daily', methods=['GET'])
def daily_report():
    boundary = DailyReportBoundary()
    daily = boundary.generateDailyReport()
    return render_template('platform_manager/PlatformManagerDailyReport.html', daily=daily)

# ─────────────────────────────────────────────────────────────────────────────
#  User Story #41 — Generate Weekly Report
# ─────────────────────────────────────────────────────────────────────────────
class WeeklyReportBoundary:
    """
    Boundary: GenerateWeeklyReport
    User Story #41 (Platform Manager): As a platform manager, I want to generate a weekly report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    Sequence: Platform Manager → GenerateWeeklyReport → WeeklyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = WeeklyReportController()

    def generateWeeklyReport(self) -> Dict[str, Any]:
        return self.controller.generateWeeklyReport()

@platform_manager_bp.route('/reports/weekly', methods=['GET'])
def weekly_report():
    boundary = WeeklyReportBoundary()
    weekly = boundary.generateWeeklyReport()
    return render_template('platform_manager/PlatformManagerWeeklyReport.html', weekly=weekly)

# ─────────────────────────────────────────────────────────────────────────────
#  User Story #42 — Generate Monthly Report
# ─────────────────────────────────────────────────────────────────────────────
class MonthlyReportBoundary:
    """
    Boundary: GenerateMonthlyReport
    User Story #42 (Platform Manager): As a platform manager, I want to generate a monthly report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    Sequence: Platform Manager → GenerateMonthlyReport → MonthlyReportController → FRA and FRACategory data
    """
    def __init__(self):
        self.controller = MonthlyReportController()

    def generateMonthlyReport(self) -> Dict[str, Any]:
        return self.controller.generateMonthlyReport()

@platform_manager_bp.route('/reports/monthly', methods=['GET'])
def monthly_report():
    boundary = MonthlyReportBoundary()
    monthly = boundary.generateMonthlyReport()
    return render_template('platform_manager/PlatformManagerMonthlyReport.html', monthly=monthly)