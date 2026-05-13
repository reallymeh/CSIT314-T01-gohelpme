# controller
import time
from users.entity.fra import FRA
from users.entity.fra_view import FRAView
from typing import List
        
'''
User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
'''
class CreateFRAController:    
    def createFRA(self, title: str, description: str, category: str, target_amount: int,  \
                    start_date: str, end_date: str, status: int, location: str, created_by: str) -> bool:
        return FRA.createFRA(title, description, category, target_amount, \
            start_date, end_date, status, location, created_by)



'''
User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
'''
class ViewFRAController:
    def viewFRA(self, fraId: str)-> FRA:
        return FRA.viewFRA(fraId)


'''
User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
'''
class UpdateFRAController:

    def updateFRA(self, fraId: str, title: str, description: str, category: str,
                  target_amount: int, start_date: str, end_date: str, location: str) -> bool:

        return FRA.updateFRA(fraId, title, description, category, \
            target_amount, start_date, end_date, location)
        

'''
User Story #18: As a Fund Raiser, I want to suspend a FRA so that I can stop the fund raising activity.
'''
class SuspendFRAController:

    def suspendFRA(self, fraId: str) -> bool:
        return FRA.suspendFRA(fraId)
    

'''
User Story #19: As a Fund Raiser, I want to search a FRA so that I can manage and update specific FRA efficiently.
'''
class SearchFRAController:

    def searchFRA(self, name: str) -> list:
        return FRA.searchFRA(name)
    
'''
User Story #20: As a Fund Raiser, I want to view the number of views of a FRA so that I can analyze the view of a FRA and adjust my strategy to attract more donees.
'''
class ViewFRAViewStatsController:
    def getStats(self, fraId):
        return FRAView.getViewStatsByDateAndUser(fraId)

    @staticmethod
    def recordView(fraId, viewer_email, owner_email, fra_name, fra_category):
        return FRAView.recordView(fraId, viewer_email, owner_email, fra_name, fra_category)
    
    
'''
User Story #21: As a Fund Raiser, I want to view the number of times a FRA is shortlisted so that I can know how many people are interested in this FRA.
'''
class ViewFRAShortlistCountController:
    def getFRAShortlistCount(self, fraId):
        return FRA.getFRAShortlistCount(fraId)

'''
User Story #22: As a Fund Raiser, I want to search history of completed FRA by service category and date period so that I can search for the past FRA that is completed.
'''
class SearchCompletedFRAHistoryController: 
    def searchCompletedFRAHistory(self, category, start_date, end_date):
        return FRA.searchCompletedFRAHistory(category, start_date, end_date)

'''
User Story #23: As a Fund Raiser, I want to view the history of completed FRA by service category and date period so that I can review how the past FRA has progressed.
'''
class ViewCompletedFRAController:
    def viewCompletedFRA(self, fraId):
        return FRA.viewCompletedFRA(fraId)
    

'''
User Story #344: As a Fund Raiser, I want to view all FRAs so that I can view many FRAs at the same time .
'''
class DisplayFRAController:
    def displayFRA(self) -> list[FRA]:
        return FRA.displayFRA()
