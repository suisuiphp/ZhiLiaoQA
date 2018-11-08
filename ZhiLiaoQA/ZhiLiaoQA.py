#encoding:utf-8
from flask import Flask,url_for,render_template,redirect,request,session
from exts import db
import config
from models import User,Question,Answer
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
@login_required
def index():
    context = {
        "questions":Question.query.order_by("-create_time").all()
    }
    print(context)
    return render_template("index.html",**context)

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")

        user = User.query.filter(User.telephone == telephone, User.password == password).first()

        if not user:
            return u"手机号或密码错误"
        else:
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for("index"))

@app.route("/regist/",methods=["GET","POST"])
def regist():
    if request.method == "GET":
        return render_template("rejist.html")
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #手机号码验证，如果被注册了就不能再注册了
        user = User.query.filter(User.telephone==telephone).first()
        if user:
            return u'该手机号码已被注册'
        else:
            #判断两次输入密码是否一致
            if password1 != password2:
                return u"两次输入密码不一致，请重新填写"
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))

@app.route("/question/",methods=["GET","POST"])
def question():
    if request.method=="GET":
        return render_template("question.html")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        question = Question(title=title,content=content)
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        question.author = user

        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/detail/<question_id>/")
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    print(question_model.id,question_model.title,question_model.content)

    return render_template("detail.html",question=question_model)

@app.route("/add_answer",methods=["POST"])
@login_required
def add_answer():
    content = request.form.get("answer_content")
    question_id = request.form.get("question_id")
    answer = Answer(content=content,question_id=question_id)
    user_id = session["user_id"]
    answer.author_id = user_id
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("detail",question_id=question_id))

if __name__ == '__main__':
    app.run()
