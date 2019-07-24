from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello!"


@app.route("/is_even", methods=["GET"])
def is_even():
    number = request.args.get('number')

    if int(number) % 2 == 0:
        return jsonify(True)

    return jsonify(False)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
