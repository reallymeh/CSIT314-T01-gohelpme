# FRA Boundary
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from users.control.fundraiserc import CreateFRAController, FRAController, ViewFRAController, UpdateFRAController, SuspendFRAController, SearchFRAController

fundraiser_bp = Blueprint('fundraiser', __name__, url_prefix='/fundraiser')

# Link to Fund Raiser Homepage
@fundraiser_bp.route('/homepage', methods=['GET'])
def homepage():
    controller = FRAController()
    fra_data = controller.get_all_fra()

    return render_template('FundRaiserHomePage.html', fra_data=fra_data)
    
    
'''
User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
'''
# Link to Create FRA page once clicked on "Create FRA" button
@fundraiser_bp.route('/create', methods=['GET'])
def show_create_fra():
    return render_template('FundRaiserCreateFRA.html')

class CreateFRAPage:
    '''Boundary class for the Create FRA page. (With parameter same as diagram)'''
    def __init__(self):
        self.controller = CreateFRAController()

    def createFRA(self, title: str, description: str, category: str,
                  target_amount: int, start_date: str, end_date: str,
                  status: int, location: str):

        return self.controller.createFRA(title, description, category, target_amount, 
                                         start_date, end_date, status, location)

    def displaySuccess(self): 
        return "Success: FRA created successfully."

    def displayError(self):
        return "Something went wrong."

# Link to Create FRA page once clicked on "Create FRA" button
@fundraiser_bp.route('/create', methods=['POST'])
def create_fra():
    data = request.get_json()

    boundary = CreateFRAPage()
    success = boundary.controller.createFRA(
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
    #controller = ViewFRAController()
    #fra = controller.viewFRA(fraId)
    page = ViewFRAPage()
    fra = page.displayFRA(fraId)
    
    return render_template('FundRaiserViewFRA.html', fra=fra)

    
'''
User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
'''
# Show Update FRA page once clicked on "Update" button for each FRA in the Fund Raiser Homepage
@fundraiser_bp.route('/update/<fraId>', methods=['GET'])
def show_update_page(fraId):
    page = ViewFRAPage()
    fra = page.displayFRA(fraId)
    
    return render_template('FundRaiserUpdateFRA.html', fra=fra)
    
class UpdateFRAPage:
    def __init__(self):
        self.controller = UpdateFRAController()
    
    def updateFRA(self, fraId: str, title: str, description: str, category: str,
                  target_amount: int, start_date: str, end_date: str, location: str):

        return self.controller.updateFRA(
            fraId, title, description, category,
            target_amount, start_date, end_date, location)
        
    def displaySuccess(self):
        return "Success: FRA updated successfully."

    def displayError(self):
        return "Update failed."

@fundraiser_bp.route('/update', methods=['POST'])
def update_fra():
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

    def displaySuccess(self):
        return "FRA suspended successfully!"

    def displayError(self):
        return "Failed to suspend FRA"
    
@fundraiser_bp.route('/suspend/<fraId>', methods=['POST'])
def suspend_fra(fraId):
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

    def searchFRA(self, name):
        return self.controller.searchFRA(name)

    def displayNoResult(self):
        return "No FRA found"

@fundraiser_bp.route('/search', methods=['POST'])
def search_fra():
    data = request.get_json()
    name = data.get('name', '')

    page = SearchFRAPage()
    results = page.searchFRA(name)

    return jsonify({
        "success": True,
        "data": results,
        "message": "" if results else page.displayNoResult()
    })
    
# Logout functionality for Fund Raiser
class LogoutPage:
    def logout(self):
        return 'You have logged out successfully!'

@fundraiser_bp.route('/logout')
def logout():
    page = LogoutPage()
    message = page.logout()
    return redirect(url_for('user.homepage', message=message))