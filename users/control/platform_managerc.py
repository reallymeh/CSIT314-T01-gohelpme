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
    """
    User Story #40 (Platform Manager): As a platform manager, I want to generate a daily report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    """
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

class WeeklyReportController:
    """
    User Story #41 (Platform Manager): As a platform manager, I want to generate a weekly report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    """
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

class MonthlyReportController:
    """
    User Story #42 (Platform Manager): As a platform manager, I want to generate a monthly report, 
    so that I can analyze the total number of views of all FRA and each FRA category.
    """
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