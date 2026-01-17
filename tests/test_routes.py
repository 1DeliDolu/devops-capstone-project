"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once after test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(
                BASE_URL,
                json=account.serialize(),
                content_type="application/json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="test/html",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    ######################################################################
    #  LIST (GET /accounts)
    ######################################################################

    def test_list_accounts_empty(self):
        """It should List all Accounts when none exist"""
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json(), [])

    def test_list_accounts(self):
        """It should List all Accounts"""
        self._create_accounts(2)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    ######################################################################
    #  READ (GET /accounts/<id>)
    ######################################################################

    def test_read_account(self):
        """It should Read an Account"""
        created = self._create_accounts(1)[0]
        account_id = created.id

        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(data["id"], account_id)

    def test_read_account_not_found(self):
        """It should not Read an Account that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  UPDATE (PUT /accounts/<id>)
    ######################################################################

    def test_update_account(self):
        """It should Update an existing Account"""
        created = self._create_accounts(1)[0]
        account_id = created.id

        update_data = created.serialize()
        update_data.pop("id", None)
        update_data["name"] = f"{update_data.get('name', 'Account')} Updated"

        resp = self.client.put(
            f"{BASE_URL}/{account_id}",
            json=update_data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(data["id"], account_id)
        self.assertEqual(data["name"], update_data["name"])

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        # 404'ü garanti etmek için valid JSON gönder
        account = AccountFactory()
        resp = self.client.put(
            f"{BASE_URL}/0",
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account_unsupported_media_type(self):
        """It should not Update an Account when sending the wrong media type"""
        created = self._create_accounts(1)[0]
        account_id = created.id

        resp = self.client.put(
            f"{BASE_URL}/{account_id}",
            json=created.serialize(),
            content_type="test/html",
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    ######################################################################
    #  DELETE (DELETE /accounts/<id>)
    ######################################################################

    def test_delete_account(self):
        """It should Delete an Account"""
        created = self._create_accounts(1)[0]
        account_id = created.id

        resp = self.client.delete(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.data, b"")

        # silindi mi kontrol (Read 404 dönmeli)
        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account_not_found(self):
        """It should not Error when Deleting an Account that does not exist"""
        resp = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.data, b"")

    ######################################################################
    #  EXTRA COVERAGE / ERROR PATHS
    ######################################################################

    def test_method_not_allowed(self):
        """It should return 405 for unsupported methods"""
        resp = self.client.patch(BASE_URL)  # /accounts PATCH desteklemez
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_found_returns_json(self):
        """It should return JSON on 404 errors"""
        resp = self.client.get("/this-route-does-not-exist")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(resp.get_json())
