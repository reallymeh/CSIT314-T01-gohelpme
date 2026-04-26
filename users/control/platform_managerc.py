from users.entity.fracategory import FRACategory

class CreateFRACategoryController:
    def createFRACategory(self, cat_name: str, description: str, status: int) -> bool:
        return FRACategory.createCategory(cat_name, description, status)

class ViewFRACategoryController:
    def viewFRACategory(self, category_name: str) -> FRACategory | None:
        return FRACategory.getCategory(category_name)

# check for backend for this user story
class UpdateFRACategoryController:
    def updateFRACategory(self, old_name: str, new_name: str, description: str, status: int) -> bool:
        return FRACategory.updateFRACategory(old_name, new_name, description, status)
    
class ViewAllFRACategoryController:
    def viewAllFRACategory(self):
        return FRACategory.getAllCategory()
    
