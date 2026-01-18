"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for  # noqa: F401

from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()

    message = account.serialize()
<<<<<<< HEAD
    # Set Location header to the new resource
    location_url = url_for("get_accounts", account_id=account.id, _external=True)
=======
    location_url = url_for("get_accounts", account_id=account.id, _external=True)

>>>>>>> list-accounts
    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# LIST ALL ACCOUNTS
######################################################################
<<<<<<< HEAD


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]

    app.logger.info("Returning [%s] accounts", len(account_list))
    return jsonify(account_list), status.HTTP_200_OK
=======
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns all Accounts"""
    accounts = Account.all()
    # Account.all() bazı şablonlarda dict list dönebilir, bazı şablonlarda model döndürür:
    results = [
        acct.serialize() if hasattr(acct, "serialize") else acct
        for acct in accounts
    ]
    return jsonify(results), status.HTTP_200_OK
>>>>>>> list-accounts


######################################################################
# READ AN ACCOUNT
######################################################################
<<<<<<< HEAD


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

=======
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Retrieves a single Account"""
>>>>>>> list-accounts
    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
<<<<<<< HEAD
            f"Account with id [{account_id}] could not be found.",
        )

=======
            f"Account with id '{account_id}' was not found.",
        )
>>>>>>> list-accounts
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Updates an Account"""
    app.logger.info("Request to update Account with id: %s", account_id)
    check_content_type("application/json")

<<<<<<< HEAD

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Update an Account
    This endpoint will update an Account based on the posted data
    """
    app.logger.info("Request to update an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    account.deserialize(request.get_json())
=======
    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    data = request.get_json(silent=True)
    if data is None:
        abort(status.HTTP_400_BAD_REQUEST, "Invalid JSON body")

    account.deserialize(data)
>>>>>>> list-accounts
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################
<<<<<<< HEAD


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if account:
        account.delete()

=======
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Deletes an Account"""
    app.logger.info("Request to delete Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
>>>>>>> list-accounts
    return "", status.HTTP_204_NO_CONTENT


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    # request.mimetype, "application/json; charset=utf-8" gibi durumlarda da "application/json" döndürür
    if request.mimetype == media_type:
        return

    content_type = request.headers.get("Content-Type")
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
