from users.entity.userprofile import UserProfile
from users.control.useradminc import UpdateUserProfileController
from users.boundary.useradminb import CreateUserProfile, ViewUserProfile, UpdateUserProfile

import sqlite3
import pytest
import os

from users.entity import userprofile

# to run python -m pytest test\sprint_1_test.py -v

TEST_DB_PATH = "test_user.db"

@pytest.fixture(scope="function") # the fixture is destroyed at the end of the test.
def temp_db(monkeypatch):
    """Create a fresh test database for the entire test class"""
    
    # Remove old test db if it exists
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except:
            pass

    # Create new database and table
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("""CREATE TABLE user_profile (
        name TEXT PRIMARY KEY,
        access_level INTEGER,
        status INTEGER,
        description TEXT
    )""")
    conn.commit()
    conn.close()

    def mock_connect_db():
        new_conn = sqlite3.connect(TEST_DB_PATH)
        return new_conn, new_conn.cursor()

    monkeypatch.setattr(userprofile, "connect_db", mock_connect_db)

    yield

    # Cleanup after all tests in the class
    try:
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
    except:
        pass

@pytest.mark.usefixtures("temp_db")
class TestUserProfile:

    # USER STORY #3
    def create_test_user(self, name="Robert", access_level=1, status=1, description="User Admin"):
        """Helper to create a user and return the result."""
        return userprofile.UserProfile.createUserProfile(name, access_level, status, description)

    # entity

    def test_create_user_profile_success(self):
        result = self.create_test_user()
        assert result is True, "createUserProfile should return True on successful insertion"

    def test_create_user_profile_fail(self):
        result = self.create_test_user(name="")
        assert result is False, "createUserProfile should return False, as name has no value"

    # boundary

    def test_click_create_display_success(self):
        boundary = CreateUserProfile()
        result = boundary.clickCreate(
            "Robert",
            1,
            1,
            "User Admin"
        )
        assert result == "Profile created successfully!"

    def test_click_create_display_fail(self):
        result = CreateUserProfile().clickCreate(
            "",
            1,
            1,
            "User Admin"
        )
        assert result == "Failed to create profile. Please check the input and try again."

    # USER STORY 4

    # entity

    def test_get_profile(self):
        # populate table
        self.create_test_user()

        # get profile
        up = UserProfile.getProfile("Robert")

        assert up.name == "Robert"
        assert up.access_level == 1
        assert up.status == 1
        assert up.description == "User Admin"

    # boundary
    def test_view_user_profile(self):
        # populate table
        self.create_test_user()

        boundary = ViewUserProfile()
        up = boundary.controller.viewUserProfile("Robert")

        assert up.name == "Robert"
        assert up.access_level == 1
        assert up.status == 1
        assert up.description == "User Admin"
    
    # USER STORY 5

    def test_update_user_profile_success(self):
        self.create_test_user()

        # update user profile
        result = UserProfile.updateUserProfile(
            "Robert",
            "Mary",
            2,
            "This is Mary"
        )

        assert result is True, "User Profile Robert should be updated."

        # check if user profile is updated correctly
        up = UserProfile.getProfile("Mary")
        assert up.access_level == 2
        assert up.description == "This is Mary"
    
    def test_update_user_profile_fail(self):
        self.create_test_user()

        result = UserProfile.updateUserProfile(
            "Unknown User",
            "Mary",
            2,
            "This is Mary"
        )

        assert result is False, "Assert should return False as User Profile does not exist"

    def test_update_user_profile_controller_success(self):
        controller = UpdateUserProfileController()

        self.create_test_user()
        result = controller.updateUserProfile("Robert", "Mary", 2, "New Description")
        assert result is True
    
    def test_update_user_profile_controller_fail(self):
        controller = UpdateUserProfileController()

        self.create_test_user()
        result = controller.updateUserProfile("Robert", "Mary", -1, "New Description")
        assert result is False, "Assert should be False as the access level is out of bounds"

        result = controller.updateUserProfile("Robert", "Mary", 5, "New Description")
        assert result is False, "Assert should be False as the access level is out of bounds"

    def test_update_user_profile_boundary_fail(self):
        self.create_test_user()

        boundary = UpdateUserProfile()
        controller = boundary.controller

        result = controller.updateUserProfile("Robert", "Mary", -1, "New Description")
        assert result is False, "Assert should be False as the access level is out of bounds"

        result = controller.updateUserProfile("Robert", "Mary", 5, "New Description")
        assert result is False, "Assert should be False as the access level is out of bounds"

    def test_update_user_profile_boundary_success(self):
        self.create_test_user()

        boundary = UpdateUserProfile()
        controller = boundary.controller
        
        result = controller.updateUserProfile("Robert", "Mary", 2, "New Description")
        assert result is True


        




       




