from users.entity.fracategory import FRACategory
from typing import List, Dict, Any

from users.entity.fra_view import FRAView

'''
User Story #35: As a platform manager, I want to create FRA categories so that I can create a new category for FRA.
'''
class CreateFRACategoryController:
    def createFRACategory(self, cat_name: str, description: str, status: int) -> bool:
        return FRACategory.createCategory(cat_name, description, status)


'''
User Story #36: As a platform manager, I want to view FRA categories so that I can view the FRA categories I created.
'''
class ViewFRACategoryController:
    def viewFRACategory(self, category_name: str) -> FRACategory | None:
        return FRACategory.getCategory(category_name)


'''
User Story #37: As a platform manager, I want to update FRA categories so that I can ensure the information is latest.
'''
class UpdateFRACategoryController:
    def updateFRACategory(self, old_name: str, new_name: str, description: str, status: int) -> bool:
        return FRACategory.updateFRACategory(old_name, new_name, description, status)


'''
Not in user stories, but needed for the platform manager to view the list of FRA categories and manage them.
'''
class ViewAllFRACategoryController:
    def viewAllFRACategory(self):
        return FRACategory.getAllCategory()


'''
User Story #38: As a platform manager, I want to suspend FRA categories so that I can make it easier for users to navigate the platform.
'''   
class SuspendFRACategoryController:
    def suspendFRACategory(self, category_name: str) -> bool:
        return FRACategory.suspendCategory(category_name)
    
    
'''
User Story #39: As a platform manager, I want to search FRA categories so that I can filter the current FRA categories the platform has.
'''
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
    

"""
User Story #40: As a platform manager, I want to generate a daily report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class DailyReportController:
    def generateDailyReport(self) -> Dict[str, Any]:
        category_rows = FRAView.getViewsGroupedByDayAndCategory()
        categories = sorted({r["fra_category"] for r in category_rows})
        period_cat: Dict[str, Dict[str, int]] = {}
        for r in category_rows:
            period_cat.setdefault(r["period"], {})[r["fra_category"]] = r["count"]
        rows = [
            {"period": period, "count": sum(by_cat.values()), "by_category": by_cat}
            for period, by_cat in sorted(period_cat.items())
        ]
        return {"total_views": sum(r["count"] for r in rows), "categories": categories, "rows": rows}


"""
User Story #41: As a platform manager, I want to generate a weekly report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class WeeklyReportController:
    def generateWeeklyReport(self) -> Dict[str, Any]:
        category_rows = FRAView.getViewsGroupedByWeekAndCategory()
        categories = sorted({r["fra_category"] for r in category_rows})
        period_cat: Dict[str, Dict[str, int]] = {}
        for r in category_rows:
            period_cat.setdefault(r["period"], {})[r["fra_category"]] = r["count"]
        rows = [
            {"period": period, "count": sum(by_cat.values()), "by_category": by_cat}
            for period, by_cat in sorted(period_cat.items())
        ]
        return {"total_views": sum(r["count"] for r in rows), "categories": categories, "rows": rows}


"""
User Story #42: As a platform manager, I want to generate a monthly report, so that I can analyze the total number of views of all FRA and each FRA category.
"""
class MonthlyReportController:
    def generateMonthlyReport(self) -> Dict[str, Any]:
        category_rows = FRAView.getViewsGroupedByMonthAndCategory()
        categories = sorted({r["fra_category"] for r in category_rows})
        period_cat: Dict[str, Dict[str, int]] = {}
        for r in category_rows:
            period_cat.setdefault(r["period"], {})[r["fra_category"]] = r["count"]
        rows = [
            {"period": period, "count": sum(by_cat.values()), "by_category": by_cat}
            for period, by_cat in sorted(period_cat.items())
        ]
        return {"total_views": sum(r["count"] for r in rows), "categories": categories, "rows": rows}