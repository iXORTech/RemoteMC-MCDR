from flask import jsonify


def get_200_response():
    """
    :return: JSON object with status code 200 and message "OK"
    """
    return jsonify({"status_code": 200, "message": "OK"})


def get_204_response():
    """
    :return: JSON object with status code 204 and message "NO_CONTENT"
    """
    return jsonify({"status_code": 204, "message": "NO_CONTENT"})


def get_400_response():
    """
    :return: JSON object with status code 400 and message "BAD_REQUEST"
    """
    return jsonify({"status_code": 400, "message": "BAD_REQUEST"})


def get_401_response():
    """
    :return: JSON object with status code 401 and message "UNAUTHORIZED"
    """
    return jsonify({"status_code": 401, "message": "UNAUTHORIZED"})
