# FRA Boundary
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from users.control.fundraiserc import CreateFRAController, FRAController

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
    def createFRA(self, title: str, description: str, category: str, targetAmount: int, \
                    startDate: str, endDate: str, status: int,  location: str) -> str:
        
        controller = CreateFRAController()

        success = controller.createFRA(title, description, category, targetAmount, \
                                        startDate, endDate, status, location)

        if success:
            self.displaySuccess()
        else:
            self.displayError()
    '''
    def displaySuccess(self): 
        return "FRA created successfully!"

    def displayError(self):
        return "Failed to create FRA."

@fundraiser_bp.route('/create', methods=['POST'])
def create_fra():
    data = request.get_json()

    controller = CreateFRAController()
    success = controller.createFRA(
        data['title'],
        data['description'],
        data['category'],
        int(data['targetAmount']),
        data['startDate'],
        data['endDate'],
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

# Logout functionality for Fund Raiser
class LogoutPage:
    def logout(self):
        return 'You have logged out successfully!'

@fundraiser_bp.route('/logout')
def logout():
    page = LogoutPage()
    message = page.logout()
    return redirect(url_for('user.homepage', message=message))
