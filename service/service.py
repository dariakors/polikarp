from flask import Flask, request, jsonify


app = Flask(__name__)


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
    number = request.args.getlist('number')
    print(number)

    if len(number) > 1:
        return jsonify({"error": "Too much numbers"}), 400

    if is_int(number[0]):

        if int(number[0]) % 2 == 0:
            return jsonify(True)

        return jsonify(False)

    return jsonify({"error": "Number must be integer"}), 415


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
