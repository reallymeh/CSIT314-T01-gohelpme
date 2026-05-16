# Donee Controller
from users.entity.fra import FRA
from users.entity.favourite import Favourite
from users.entity.donationhistory import DonationHistory


"""
User Story #26: As a Donee, I want to search all active FRA by name so that I can find a specific FRA that I am interested in.
"""
class SearchActiveFRAController:
    def searchActiveFRA(self, name: str) -> list[FRA]:
        return FRA.searchActiveFRA(name)


"""
User Story #27: As a Donee, I want to view an active FRA so that I can view existing FRA information that needs donation.
"""
class ViewActiveFRAController:
    def viewActiveFRA(self, fraId: str) -> "FRA | None":
        return FRA.viewActiveFRA(fraId)


"""
User Story #28: As a Donee, I want to save a FRA to my favourite list so that I can decide on a donation later.
"""
class SaveFavouriteController:
    def saveFavourite(self, donee_email: str, fraId: str) -> bool:
        if Favourite.isFavourite(donee_email, fraId):
            return False  # already saved — not a DB error, just a duplicate
        return Favourite.saveFavourite(donee_email, fraId)

    def isFavourite(self, donee_email: str, fraId: str) -> bool:
        return Favourite.isFavourite(donee_email, fraId)


'''Not a user story, but is optional for the Donee to manage their favourite list.'''
class RemoveFavouriteController:
    def removeFavourite(self, donee_email: str, fraId: str) -> bool:
        return Favourite.removeFavourite(donee_email, fraId)


"""
User Story #29: As a Donee, I want to search for an active FRA in my favourite list by name so that I can find a specific FRA within the favourite list.
"""
class SearchFavouriteController:
    def searchFavourites(self, donee_email: str, name: str) -> list[Favourite]:
        return Favourite.searchFavourites(donee_email, name)


"""
User Story #30: As a Donee, I want to view FRA in my favourite list so that I can view all FRA within the favourite list.
"""
class ViewFavouriteController:
    def viewFavourites(self, donee_email: str) -> list[Favourite]:
        return Favourite.viewFavourites(donee_email)


"""
User Story #31: As a Donee, I want to search history of donation byFRA category and date period so that I can find a specific FRA I had donated.
"""
class SearchDonationHistoryController:
    def searchHistory(self, donee_email: str, category: str,
                      date_from: str, date_to: str) -> list[DonationHistory]:
        return DonationHistory.searchHistory(donee_email, category, date_from, date_to)


"""
User Story #32: As a Donee, I want to view the history of donation so that I can evaluate the impact of my donation and consider another donation.
"""
class ViewDonationHistoryController:
    def viewHistory(self, donee_email: str) -> list[DonationHistory]:
        return DonationHistory.viewHistory(donee_email) 


"""Not specifically mentioned in user stories, but needed for the donee to view the list of active FRAs and find one they are interested in."""
class ViewAllFRAController:
    def viewAllFRA(self) -> list[FRA]:
        return FRA.viewAllActiveFRA()