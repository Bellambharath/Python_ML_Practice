from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_bootstrap import Bootstrap5


class MyForm(FlaskForm):
    name = StringField(label='name')


app = Flask(__name__)
app.secret_key = "any_key"
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/success")
def success():
    login_form = MyForm()
    return render_template('success.html', form=login_form)


@app.route("/denied")
def denied():
    return render_template('denied.html')


@app.route("/base")
def login():
    return render_template('base.html')


# @app.route('/submit', methods=['GET', 'POST'])
# def submit():
#     form = MyForm()
#    print(form.validate_on_submit())


if __name__ == '__main__':
    app.run(debug=True)
