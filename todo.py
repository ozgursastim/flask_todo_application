from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Uygulamın erişeceği veri tabanı konfigürasyonu yapılmaktadır.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ozgur/PycharmProjects/ToDoApp/todo.db'
# SQLAlchemy'nın bir örneği olarak db nesnesi yaratılmaktadır.
# bu nesne kullanılarak SQL komutları yerine nesnenin fonksiyonları kullanılarak SQL işlemleri yapılmaktadır.
db = SQLAlchemy(app)

@app.route("/")
def index():
    # todos diye bir listeye tüm tablonun bilgileri gönderilmektedir.
    todos = Todo.query.all()
    # index sayfasına todos listesine gönderilmektedir.
    return render_template("index.html", todos = todos)

@app.route("/add", methods = ["POST"])
def addTodo():
    # Form üzerinden gelen title bilgisi title alanına aktarılmaktadır.
    title = request.form.get("title")
    # Title ve complete bilgileri gönderilerek yeni bir Todo model örneği oluşturulmaktadır.
    newTodo = Todo(title = title, complete = False)
    # Yeni model örneği tabloya eklenmektedir.
    db.session.add(newTodo)
    # commit özellği kullanılarak tabloya kaydın ekleme işlemi fiziksel olarak yapılmaktadır.
    db.session.commit()
    # kayıt eklendikten sonra index sayfasına yönlendirilmektedir.
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    # Todo modelinden id alanına göre kayıtlar seçilmektedir.
    # first özelliği ile ilk gelen kayıt seçilmektedir.
    todo = Todo.query.filter_by(id=id).first()
    # if todo.complete:
        # todo.complete = False
    # else:
        # todo.complete = True
    # Eğer complete alanı True ise False, False ise True yapılmaktadır.
    todo.complete = not todo.complete
    # commit özellği kullanılarak tabloya kaydın ekleme işlemi fiziksel olarak yapılmaktadır.
    db.session.commit()
    # kaydın statüsü değiştirildikten sonra index sayfasına yönlendirilmektedir.
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    # Todo modelinden id alanına göre kayıtlar seçilmektedir.
    # first özelliği ile ilk gelen kayıt seçilmektedir.
    todo = Todo.query.filter_by(id=id).first()
    # İlgili kayıt veri tabanında silinmektedir.
    db.session.delete(todo)
    # commit özellği kullanılarak tabloya kaydın ekleme işlemi fiziksel olarak yapılmaktadır.
    db.session.commit()
    # kayıt silindikten sonra index sayfasına yönlendirilmektedir.
    return redirect(url_for("index"))

class Todo(db.Model):
    # Integer tipinde bir alan oluşturulmaktadır. primary_key özelliği ile tablonun birincil anahtarı olarak belirlenmektedir.
    id = db.Column(db.Integer, primary_key=True)
    # 80 karakter uzunluğunda string alan oluşturulmaktadır.
    title = db.Column(db.String(80))
    # görevin tamamlanıp tamamlanmadığını belirlemek için mantıksal veri tipi oluşturulmuştur.
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    # Bu kod her seferinde çalıştırılmaktadır. Eğer DB yaratılmış ise tekrar yaratılmamaktadır.
    db.create_all()
    # Debug modda çalıştırılmaktadır.
    app.run(debug=True) 
<