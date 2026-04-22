from control.platform_managerc import CreateFRACategoryController

class CreateFRACategoryBoundary:
    def __init__(self):
        self.controller = CreateFRACategoryController()
    
    def createFRACategory(self, cat_name:str, description:str) -> bool:
        return self.controller.createFRACategory(cat_name, description)
    
    def displaySuccess():
        print("Creation Success")
    
    def displayFailure():
        print("Creation Failed")