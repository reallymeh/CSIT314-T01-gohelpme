from users.control.platform_managerc import CreateFRACategoryController, ViewFRACategoryController
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

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

@platform_manager_bp.route('/categories', methods=['GET'])
def category_list():
    return render_template('PlatformManagerCategories.html')

@platform_manager_bp.route('/create_category', methods=['GET'])
def show_create_category():
    return render_template('PlatformManagerCreateCategory.html')

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

    # viewFRACategory(): void — receives category_name and passes to controller
    def viewFRACategory(self, category_name: str) -> None:
        return self.controller.viewFRACategory(category_name)

    # displayViewResult(): void — triggers rendering of category details
    def displayViewResult(self, category) -> None:
        pass

@platform_manager_bp.route('/viewcategory/<category_name>', methods=['GET'])
def view_category(category_name):
    boundary = ViewFRACategoryBoundary()
    category = boundary.viewFRACategory(category_name)
    # BCE BOUNDARY: displayViewResult() — renders category details
    boundary.displayViewResult(category)
    return render_template('PlatformManagerViewCategory.html', category=category)