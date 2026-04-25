# FRA Boundary
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from users.control.fundraiserc import CreateFRAController, FRAController, ViewFRAController, UpdateFRAController

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
    '''
    def createFRA(self, title: str, description: str, category: str, target_amount: int, \
                    start_date: str, end_date: str, status: int,  location: str) -> str:
        
        controller = CreateFRAController()

        success = controller.createFRA(title, description, category, target_amount, \
                                        start_date, end_date, status, location)

        if success:
            self.displaySuccess()
        else:
            self.displayError()
    '''
    def displaySuccess(self): 
        return "FRA created successfully!"

    def displayError(self):
        return "Failed to create FRA."

# Link to Create FRA page once clicked on "Create FRA" button
@fundraiser_bp.route('/create', methods=['POST'])
def create_fra():
    data = request.get_json()

    controller = CreateFRAController()
    success = controller.createFRA(
        data['title'],
        data['description'],
        data['category'],
        int(data['target_amount']),
        data['start_date'],
        data['end_date'],
        int(data['status']),
        data['location']
    )

    boundary = CreateFRAPage()

    if success:
        message = boundary.displaySuccess()
    else:
        message = boundary.displayError()

    return jsonify({
        "success": success,
        "message": message
    })


'''
User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
'''
class ViewFRAPage:
    def displayFRA(self, fraId: int):
        controller = ViewFRAController()
        fra = controller.viewFRA(fraId)

        if fra:
            return fra
        else:
            return None

    def displayError(self):
        return "FRA not found"

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
    
    def displaySuccess(self):
        return "FRA updated successfully!"

    def displayError(self):
        return "Failed to update FRA"

@fundraiser_bp.route('/update', methods=['POST'])
def update_fra():
    data = request.get_json()

    controller = UpdateFRAController()
    success = controller.updateFRA(
        data['fraId'],
        data['title'],
        data['description'],
        data['category'],
        int(data['target_amount']),
        data['start_date'],
        data['end_date'],
        data['location']
    )

    boundary = UpdateFRAPage()

    return jsonify({
        "success": success,
        "message": boundary.displaySuccess() if success else boundary.displayError()
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
