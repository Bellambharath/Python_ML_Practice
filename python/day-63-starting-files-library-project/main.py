from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = "Abcd"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
bootstrap = Bootstrap5(app)
all_books = []


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# with app.app_context():
#     db.create_all()

# with app.app_context():
#     # new_book = Book(title="Harry Potterr", author="J. K. Rowling", rating=9.3)
#     # db.session.add(new_book)
#     # db.session.commit()
#     result = db.session.execute(db.select(Book).order_by(Book.title))
#     books = result.scalars().all()


class Book_Form(FlaskForm):
    Title = StringField('Title', validators=[DataRequired()])
    Author = StringField('Author', validators=[DataRequired()])
    Rating = StringField('Rating', validators=[DataRequired()])
    Submit = SubmitField(label="Submit")


@app.route('/')
def home():
    print(len(all_books))
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        books = result.scalars().all()
        print(books)
    return render_template("index.html", all_books=books)


@app.route("/add", methods=["Get", "Post"])
def add():
    print("Hit")
    form = Book_Form()
    if form.is_submitted():
        print("inside if")
        books = Book(title=form.Title.data, author=form.Author.data, rating=form.Rating.data)
        # books.title = form.Title.data,
        # books.author = form.Author.data,
        # books.rating = form.Rating.data
        # data = {
        #     "title": form.Title.data,
        #     "author": form.Author.data,
        #     "rating": form.Rating.data,
        # }
        # all_books.append(data)
        # print(all_books)
        db.session.add(books)
        db.session.commit()
        return redirect("/")

    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
