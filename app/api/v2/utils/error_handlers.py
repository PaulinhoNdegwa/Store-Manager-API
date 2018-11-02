from flask import jsonify


def resource_not_found(error):
    """This function handles all resource not found errors Eg. URL NOT FOUND"""

    return jsonify({"message": "Resource not found. Please confirm the URL",
                    "status": 404})


def method_not_allowed(error):
    """This functions catches all invalid methods in resources"""

    return jsonify({"message": "Method not allowed for this resource",
                    "status": 405})


def missing_auth_header(error):
    """This functions catches unauthorised access to resources"""

    return jsonify({"message": "Unauthorised. Missing access token",
                    "status": 401})
