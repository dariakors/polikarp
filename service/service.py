from flasgger import Swagger
from flask import Flask, request, jsonify


app = Flask(__name__)
swagger = Swagger(app)


def is_int(number):
    try:
        int(number)
    except ValueError:
        return False

    return True


@app.route("/")
def hello():
    return "Hello, I'm Polikarp! Let's help you to understand whether number is even or not"


@app.route("/is_even", methods=["GET"])
def is_even():
    """Endpoint returns whether number is even or not
        ---
        parameters:
          - name: number
            in: query
            required: true
        responses:
            200:
                description: true or false is returned
            415:
                description: number must be integer
            400:
                description: you've missed the 'number' parameter or too much numbers are gotten
    """
    number = request.args.getlist('number')

    if len(number) > 1:
        return jsonify({"error": "Too much numbers"}), 400

    try:

        if is_int(number[0]):

            if int(number[0]) % 2 == 0:
                return jsonify(True)

            return jsonify(False)

        return jsonify({"error": "Number must be integer"}), 415

    except IndexError:
        return jsonify({"error": "You've missed the 'number' parameter"}), 400


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
