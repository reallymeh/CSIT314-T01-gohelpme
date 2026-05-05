from users.entity.fracategory import FRACategory
from typing import List, Dict, Any

from users.entity.fra_view import FRAView

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

class SearchFRACategoryController:
    def searchFRACategory(self, query: str) -> List["FRACategory"]:
        all_profiles = FRACategory.getAllCategory()

        if not query or query.strip() == "":
            return all_profiles

        query = query.strip().lower()
        results = [
            p for p in all_profiles
            if query in p.category_name.lower() or
               (hasattr(p, 'description') and query in getattr(p, 'description', '').lower())
        ]
        return results
    
class SuspendFRACategoryController:
    def suspendFRACategory(self, category_name: str) -> bool:
        return FRACategory.suspendCategory(category_name)
    
class DailyReportController:
    def generateDailyReport(self) -> Dict[str, Any]:
        total_views = FRAView.getDailyFRAView()
        category_views = FRAView.getDailyCategoryView()

        return {
            "total_views": total_views,
            "category": {
                row["fra_category"]: row["count"]
                for row in category_views
                }
            }
    
class WeeklyReportController:
    def getReport(self) -> Dict[str, Any]:
        total_views = FRAView.getWeeklyFRAViews()
        category_views = FRAView.getWeeklyCategoryViews()

        return {
            "total_views": total_views,
            "category": {
                row["fra_category"]: row["count"]
                for row in category_views
                }
            }

class MonthlyReportController:
    def getReport(self) -> Dict[str, Any]:
        total_views = FRAView.getMonthlyFRAViews()
        category_views = FRAView.getMonthlyCategoryViews()
        print(category_views)
        return {
            "total_views": total_views,
            "category": {
                row["fra_category"]: row["count"]
                for row in category_views
                }
            }