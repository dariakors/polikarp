from flasgger import Swagger
from flask import Flask, request, jsonify
import logging
import sys


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
    numbers = request.args.getlist('number')

    service_logger.debug("Polikarp got the following number(s):{}".format(numbers))

    if len(numbers) > 1:
        return jsonify({"error": "Too much numbers"}), 400

    try:

        if is_int(numbers[0]):

            number = int(numbers[0])

            if number % 2 == 0:

                service_logger.debug("Number {} is definitely even..".format(number))
                return jsonify(True)

            service_logger.debug("Number {} is definitely not even..".format(number))
            return jsonify(False)

        service_logger.debug("Number {} has type {}".format(numbers[0], type(numbers[0])))
        return jsonify({"error": "Number must be integer"}), 415

    except IndexError:
        service_logger.debug("Url looks like {}".format(request.args))
        return jsonify({"error": "You've missed the 'number' parameter"}), 400


if __name__ == "__main__":
    logging_formatter = logging.Formatter(u"%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    logging_console_handler = logging.StreamHandler(stream=sys.stdout)
    logging_console_handler.setFormatter(logging_formatter)

    service_logger = logging.getLogger(__name__)
    service_logger.setLevel(logging.DEBUG)
    service_logger.addHandler(logging_console_handler)
    app.run("0.0.0.0", port=8080, debug=True)
