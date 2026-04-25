# controller
import time
from users.entity.fra import FRA

'''
Dashboard: Fund Raiser Home Page
'''
class FRAController:
    def get_all_fra(self):
        rows = FRA.get_all_fra()

        return [
    {
        "fraId": r[0],
        "title": r[1],
        "description": r[2],
        "category": r[3],
        "target_amount": r[4],
        "collected_amount": r[5],
        "start_date": r[6],
        "end_date": r[7],
        "status": r[8],
        "view_count": r[9],
        "location": r[10]
    }
    for r in rows
]
      
        
'''
User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
'''
class CreateFRAController:
    '''Controller class for the Create FRA page. (With parameter same as diagram)'''
    
    def createFRA(self, title: str, description: str, category: str, target_amount: int,  \
                    start_date: str, end_date: str, status: int, location: str) -> bool:
        
        collected_amount = 0
        view_count = 0
        
        try:
            FRA.createFRA(title, description, category, target_amount, collected_amount, \
            start_date, end_date, status, view_count, location)
            return True

        except Exception as e:
            print(e)
            return False


'''
User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
'''
class ViewFRAController:
    def viewFRA(self, fraId):
        fra = FRA.viewFRA(fraId)

        if fra:
            return fra
        return None

'''
User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
'''
class UpdateFRAController:

    def updateFRA(self, fraId, title, description, category,
                  target_amount, start_date, end_date, location):

        if not fraId or not title:
            return False

        try:
            return FRA.updateFRA(fraId, title, description, category, \
                target_amount, start_date, end_date, location)
            
        except Exception as e:
            print("UPDATE ERROR:", e)
            return False