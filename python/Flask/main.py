from flask import Flask

app = Flask(__name__)


def make_bold(function):
    def wrapper_fun():
        return f'<b>{function()}</b>'

    return wrapper_fun


def make_emphasis(function):
    def wrapper_fun():
        return f'<em>{function()}</em>'

    return wrapper_fun


def make_underline(function):
    def wrapper_fun():
        return f'<u>{function()}</u>'

    return wrapper_fun


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/bye')
@make_bold
@make_emphasis
@make_underline
def bye():
    return f"Hey , I am here"


if __name__ == "__main__":
    app.run(debug=True)
