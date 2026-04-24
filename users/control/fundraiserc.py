# controller
import time
from users.entity.fra import FRA

'''Dashboard: Fund Raiser Home Page'''
class FRAController:
    def get_all_fra(self):
        rows = FRA.get_all_fra()

        return [
            {
                "title": r[1],
                "description": r[2]
            }
            for r in rows
        ]
        
'''
User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
'''
class CreateFRAController:
    '''Controller class for the Create FRA page. (With parameter same as diagram)'''
    
    def createFRA(self, title: str, description: str, category: str, targetAmount: int,  \
                    startDate: str, endDate: str, status: int, location: str) -> bool:
        
        fraId = "FRA" + str(int(time.time()))
        collectedAmount = 0
        viewCount = 0
        
        try:
            FRA.createFRA(fraId, title, description, category, targetAmount,collectedAmount, \
            startDate, endDate, status, viewCount, location)
            return True

        except Exception as e:
            print(e)
            return False