from users.entity.fracategory import FRACategory

class CreateFRACategoryController:
    def createFRACategory(cself, cat_name:str, description:str):
        return FRACategory.createCategory(cat_name, description)

