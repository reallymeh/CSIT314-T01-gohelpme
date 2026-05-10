# Donee Controller
from users.entity.fra import FRA
from users.entity.favourite import Favourite
from users.entity.donationhistory import DonationHistory


class ViewAllFRAController:
    def viewAllFRA(self) -> list:
        return FRA.viewAllActiveFRA()


class SearchActiveFRAController:
    """
    User Story #26 (Donee): As a Donee, I want to search all active FRA by name
    so that I can find a specific FRA that I am interested in.
    """
    def searchActiveFRA(self, name: str) -> list:
        return FRA.searchActiveFRA(name)


class ViewActiveFRAController:
    """
    User Story #27 (Donee): As a Donee, I want to view an active FRA 
    so that I can view existing FRA information that needs donation.
    """
    def viewActiveFRA(self, fraId: str) -> dict | None:
        return FRA.viewActiveFRA(fraId)


class SaveFavouriteController:
    """
    User Story #28 (Donee): As a Donee, I want to save a FRA to my favourite list
    so that I can decide on a donation later.
    """
    def saveFavourite(self, donee_email: str, fraId: str) -> bool:
        if Favourite.isFavourite(donee_email, fraId):
            return False  # already saved — not a DB error, just a duplicate
        return Favourite.saveFavourite(donee_email, fraId)

    def isFavourite(self, donee_email: str, fraId: str) -> bool:
        return Favourite.isFavourite(donee_email, fraId)


class RemoveFavouriteController:
    def removeFavourite(self, donee_email: str, fraId: str) -> bool:
        return Favourite.removeFavourite(donee_email, fraId)


class SearchFavouriteController:
    """
    User Story #29 (Donee): As a Donee, I want to search for an active FRA in my favourite list by name 
    so that I can find a specific FRA within the favourite list.
    """
    def searchFavourites(self, donee_email: str, name: str) -> list:
        return Favourite.searchFavourites(donee_email, name)


class ViewFavouriteController:
    """
    User Story #30 (Donee): As a Donee, I want to view FRA in my favourite list
    so that I can view all FRA within the favourite list.
    """
    def viewFavourites(self, donee_email: str) -> list:
        return Favourite.viewFavourites(donee_email)


class SearchDonationHistoryController:
    """
    User Story #31 (Donee): As a Donee, I want to search history of donation by
    FRA category and date period so that I can find a specific FRA I had donated.
    """
    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list:
        return DonationHistory.searchHistory(donee_email, category, date_from, date_to)



class ViewDonationHistoryController:
    """
    User Story #32 (Donee): As a Donee, I want to view the history of donation 
    so that I can evaluate the impact of my donation and consider another donation.
    """
    def viewHistory(self, donee_email: str) -> list:
        return DonationHistory.viewHistory(donee_email) 
