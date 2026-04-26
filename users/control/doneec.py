# Donee Controller
from users.entity.fra import FRA
from users.entity.favourite import Favourite
from users.entity.donationhistory import DonationHistory


'''
User Story #1 (Donee): As a Donee, I want to search all FRA by name
so that I can find a specific FRA that I am interested in.
'''
class SearchFRAController:
    def searchFRA(self, name: str) -> list:
        return FRA.searchActiveFRA(name)


'''
User Story #2 (Donee): As a Donee, I want to view a FRA
so that I can view existing FRA information that needs donation.
'''
class ViewFRAController:
    def viewFRA(self, fraId: str) -> dict | None:
        return FRA.viewFRA(fraId)


'''
User Story #3 (Donee): As a Donee, I want to save a FRA to favourite list
so that I can decide a donation later.
'''
class SaveFavouriteController:
    def saveFavourite(self, donee_email: str, fraId: str) -> bool:
        if Favourite.isFavourited(donee_email, fraId):
            return False   # already saved — not a DB error, just a duplicate
        return Favourite.saveFavourite(donee_email, fraId)

    def isFavourited(self, donee_email: str, fraId: str) -> bool:
        return Favourite.isFavourited(donee_email, fraId)


'''
User Story #4 (Donee): As a Donee, I want to search FRA in favourite list by name
so that I can find a specific FRA within the favourite list.
'''
class SearchFavouriteController:
    def searchFavourites(self, donee_email: str, name: str) -> list:
        return Favourite.searchFavourites(donee_email, name)


'''
User Story #5 (Donee): As a Donee, I want to view FRA in favourite list
so that I can view all FRA within the favourite list.
'''
class ViewFavouriteListController:
    def viewFavourites(self, donee_email: str) -> list:
        return Favourite.searchFavourites(donee_email, "")   # empty name = all


'''
User Story #6 (Donee): As a Donee, I want to search history of donation
by FRA category and date period so that I can find a specific FRA I had donated.
'''
class SearchDonationHistoryController:
    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list:
        return DonationHistory.searchHistory(donee_email, category, date_from, date_to)

    def getCategories(self, donee_email: str) -> list:
        return DonationHistory.getDistinctCategories(donee_email)


'''
User Story #7 (Donee): As a Donee, I want to view history of donation
so that I can evaluate the impact of my donation and consider another donation.
'''
class ViewDonationHistoryController:
    def viewHistory(self, donee_email: str) -> list:
        return DonationHistory.searchHistory(donee_email, "", "", "")  # no filters = all
