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
from service.common import status
from service.models import db, Account, init_db
from service.routes import app
from service import talisman   # REQUIRED FOR Exercise 5

DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"
HTTPS_ENVIRON = {"wsgi.url_scheme": "https"}

######################################################################
#  A C C O U N T   S E R V I C E   T E S T S
######################################################################


class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        talisman.force_https = False  # 🔑 REQUIRED FOR Exercise 5
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    ##################################################################
    #  H E L P E R   M E T H O D S
    ##################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts"""
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
            data = response.get_json()
            account.id = data["id"]
            accounts.append(account)
        return accounts

    ##################################################################
    #  R O U T E   T E S T S
    ##################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        location = response.headers.get("Location")
        self.assertIsNotNone(location)

        data = response.get_json()
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["address"], account.address)
        self.assertEqual(data["phone_number"], account.phone_number)
        self.assertEqual(data["date_joined"], str(account.date_joined))

    def test_get_account(self):
        """It should Read a single Account"""
        account = self._create_accounts(1)[0]
        response = self.client.get(
            f"{BASE_URL}/{account.id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["name"], account.name)

    def test_bad_request(self):
        """It should not Create an Account with bad data"""
        response = self.client.post(
            BASE_URL,
            json={"name": "bad data"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should reject wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="text/html",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

######################################################################
#  S E C U R I T Y   H E A D E R   T E S T S
######################################################################


class TestSecurityHeaders(TestCase):
    """Test for security headers and CORS"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_security_headers(self):
        """It should return security headers"""
        response = self.client.get(
            "/",
            environ_overrides=HTTPS_ENVIRON,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(
            response.headers.get("X-Content-Type-Options"),
            "nosniff",
        )
        self.assertEqual(
            response.headers.get("Content-Security-Policy"),
            "default-src 'self'; object-src 'none'",
        )
        self.assertEqual(
            response.headers.get("Referrer-Policy"),
            "strict-origin-when-cross-origin",
        )

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get(
            "/",
            environ_overrides=HTTPS_ENVIRON,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            "*",
        )
