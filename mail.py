from flask import Flask, render_template, request

from flask_mail import Mail,Message

app = Flask(__name__)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "mrmyname.97@gmail.com"
app.config['MAIL_PASSWORD'] = "btsexoshineeikon"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("delete.html")

@app.route("/send_message", methods=["GET"])
def send_message():
    if request.method == "POST":
        email = request.form['email']
        msg = request.form['message']

        message = Message(sender="mrmyname.97@gmail.com", recipients=[email])
        message.body = msg
        mail.send(message)
        success = "Message Sent"
        return render_template("result.html", success=success)

if __name__ == "__main__":
    app.run(debug=True)
