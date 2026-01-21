"""
Account Service Routes

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, make_response, abort
from service.models import Account
from service.common import status
from service import app

######################################################################
# Health Endpoint
######################################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# Index Endpoint
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return jsonify(
        name="Account REST API Service",
        version="1.0",
    ), status.HTTP_200_OK


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_account():
    """Creates an Account"""
    app.logger.info("Request to create an Account")

    # Check Content-Type
    if request.headers.get("Content-Type") != "application/json":
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Content-Type must be application/json",
        )

    data = request.get_json()
    if not data:
        abort(status.HTTP_400_BAD_REQUEST, "No data provided")

    account = Account()
    try:
        account.deserialize(data)
    except (KeyError, TypeError, ValueError):
        abort(status.HTTP_400_BAD_REQUEST, "Invalid Account data")

    account.create()

    return make_response(
        jsonify(account.serialize()),
        status.HTTP_201_CREATED,
        {"Location": f"/accounts/{account.id}"},
    )


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Retrieve a single Account"""
    app.logger.info("Request to read Account %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an existing Account"""
    app.logger.info("Request to update Account %s", account_id)

    if request.headers.get("Content-Type") != "application/json":
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Content-Type must be application/json",
        )

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    try:
        account.deserialize(request.get_json())
    except (KeyError, TypeError, ValueError):
        abort(status.HTTP_400_BAD_REQUEST, "Invalid Account data")

    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""
    app.logger.info("Request to delete Account %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    account.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)