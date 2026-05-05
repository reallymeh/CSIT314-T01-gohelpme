# Donee Controller
from users.entity.fra import FRA
from users.entity.favourite import Favourite
from users.entity.donationhistory import DonationHistory


class ViewAllFRAController:
    """
    User Story #1 (Donee): As a Donee, I want to view all active FRAs on the
    dashboard so that I can browse all available fundraising activities.
    """
    def viewAllFRA(self) -> list:
        return FRA.viewAllActiveFRA()


class SearchFRAController:
    """
    User Story #1 (Donee): As a Donee, I want to search all FRA by name
    so that I can find a specific FRA that I am interested in.
    """
    def searchFRA(self, name: str) -> list:
        return FRA.searchActiveFRA(name)


class ViewFRAController:
    """
    User Story #2 (Donee): As a Donee, I want to view a FRA
    so that I can view existing FRA information that needs donation.
    """
    def viewFRA(self, fraId: str) -> dict | None:
        return FRA.viewFRA(fraId)


class SaveFavouriteController:
    """
    User Story #3 (Donee): As a Donee, I want to save a FRA to favourite list
    so that I can decide a donation later.
    """
    def saveFavourite(self, donee_email: str, fraId: str) -> bool:
        if Favourite.isFavourited(donee_email, fraId):
            return False  # already saved — not a DB error, just a duplicate
        return Favourite.saveFavourite(donee_email, fraId)

    def isFavourited(self, donee_email: str, fraId: str) -> bool:
        return Favourite.isFavourited(donee_email, fraId)


class RemoveFavouriteController:
    """
    User Story #3b (Donee): As a Donee, I want to remove a FRA from my favourite list.
    """
    def removeFavourite(self, donee_email: str, fraId: str) -> bool:
        return Favourite.removeFavourite(donee_email, fraId)


class SearchFavouriteController:
    """
    User Story #4 (Donee): As a Donee, I want to search FRA in favourite list by name
    so that I can find a specific FRA within the favourite list.
    """
    def searchFavourites(self, donee_email: str, name: str) -> list:
        return Favourite.searchFavourites(donee_email, name)


class ViewFavouriteController:
    """
    User Story #5 (Donee): As a Donee, I want to view FRA in favourite list
    so that I can view all FRA within the favourite list.
    """
    def viewFavourites(self, donee_email: str) -> list:
        return Favourite.viewFavourites(donee_email)


class SearchDonationHistoryController:
    """
    User Story #6 (Donee): As a Donee, I want to search history of donation
    by FRA category and date period so that I can find a specific FRA I had donated.
    """
    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list:
        return DonationHistory.searchHistory(donee_email, category, date_from, date_to)

    def getCategories(self, donee_email: str) -> list:
        return DonationHistory.getCategories(donee_email)


class ViewDonationHistoryController:
    """
    User Story #7 (Donee): As a Donee, I want to view history of donation
    so that I can evaluate the impact of my donation and consider another donation.
    """
    def viewHistory(self, donee_email: str) -> list:
        return DonationHistory.viewHistory(donee_email) 
