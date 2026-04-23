from users.control.platform_managerc import CreateFRACategoryController, ViewFRACategoryController
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

platform_manager_bp = Blueprint('platform_manager', __name__, url_prefix='/manager')

# ========== BCE BOUNDARY: CreateFRACategory ==========
# User Story: #35 As a platform management, I want to create FRA categories
class CreateFRACategoryBoundary:
    def __init__(self):
        self.controller = CreateFRACategoryController()

    def createFRACategory(self, cat_name: str, description: str) -> bool:
        return self.controller.createFRACategory(cat_name, description)

    def displaySuccess(self):
        return 'Category created successfully!'

    def displayFailure(self):
        return 'Failed to create category. Category may already exist.'

@platform_manager_bp.route('/categories', methods=['GET'])
def category_list():
    # BACKEND: Replace hardcoded return with DisplayFRACategoryController
    # categories = DisplayFRACategoryBoundary().displayFRACategory()
    # return render_template('PlatformManagerCategories.html', categories=categories)
    return render_template('PlatformManagerCategories.html')

@platform_manager_bp.route('/create_category', methods=['GET'])
def show_create_category():
    return render_template('PlatformManagerCreateCategory.html')

@platform_manager_bp.route('/create_category', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()

    boundary = CreateFRACategoryBoundary()
    if boundary.createFRACategory(name, description):
        return jsonify({'success': True, 'message': boundary.displaySuccess()})
    else:
        return jsonify({'success': False, 'message': boundary.displayFailure()})

# ========== BCE BOUNDARY: ViewFRACategory ==========
# User Story: #36 As a platform management, I want to view FRA categories
class ViewFRACategoryBoundary:
    def __init__(self):
        self.controller = ViewFRACategoryController()

    def displayViewResult(self, category: FRACategory):
        return category

    def displayViewFail(self):
        return None

    def viewFRACategory(self, category_name: str):
        return self.controller.viewFRACategory(category_name)

# ========== BCE BOUNDARY: ViewFRACategory ==========
@platform_manager_bp.route('/viewcategory/<category_name>', methods=['GET'])
def view_category(category_name):
    category = ViewFRACategoryBoundary().viewFRACategory(category_name)
    if category is None:
        # BCE BOUNDARY: displayViewFail()
        return redirect(url_for('platform_manager.category_list'))
    # BCE BOUNDARY: displayViewResult()
    return render_template('PlatformManagerViewCategory.html', category=category)