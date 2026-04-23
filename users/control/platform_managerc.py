from users.entity.fracategory import FRACategory

class CreateFRACategoryController:
    def createFRACategory(self, cat_name:str, description:str):
        return FRACategory.createCategory(cat_name, description)

class ViewFRACategoryController:
    def viewFRACategory(self, category_name: str) -> FRACategory | None:
        return FRACategory.getCategory(category_name)