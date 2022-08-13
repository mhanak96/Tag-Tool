from flask import Flask, render_template, request, session
from cs50 import SQL
from flask_session import Session

app = Flask(__name__)
db = SQL("sqlite:///tagdatabase.db")

# configuring session (filesystem storage)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    # setting feedback counter (a showing feedback comment from database and a place to store
    # user decisions regarding it) - I chosed storing it in session not in the database because
    # detabase is always one and multiple users would like to check how it work so this is a better idea
    # of course if this was a reall application I would store tagged content in database so it can be reused
    session["feedback_counter"] = 0
    session["c_data"] = []
    return render_template("index.html")

@app.route("/tagging", methods=["GET", "POST"])
def tagging():
    # after the POST usage the site refreshed so i lost all my saved data. Because I always reading
    #informations from session first this is not longer a problem
    feedback_counter = session["feedback_counter"]
    write_to_session = session["c_data"]

    # loading feedback for a first time
    feedback_data = db.execute("SELECT feedback FROM opinions")



    # When using form to POST data:
    if request.method == 'POST':

        # Getting submit button value. Thanks to: https://stackoverflow.com/questions/19794695/flask-python-buttons
        # I tried to make an increase AND decrease buttons but the decrease button made some strange error
        # and i couldn't solve it - so it had more sens earlier 😅

        # submiting button is increasing counter so we can read another feedback comment

         if request.form['btn_increase'] == 'increase':
            feedback_counter = feedback_counter + 1

        # Prevent server error 500 thanks to
        # https://stackoverflow.com/questions/6362047/how-to-check-if-a-name-value-pair-exists-when-posting-data
        # although they got it wrong it's request.form not request.POST

            # case 1: user doesn't decide if comment is positive or negative
            if('pos-neg' not in request.form):
                return render_template("tagging.html", s_data = write_to_session, f_data = feedback_data, f_counter = feedback_counter - 1)

            # case 2: user doesn't chose departament
            elif('chosen' not in request.form):
                return render_template("tagging.html", s_data = write_to_session, f_data = feedback_data, f_counter = feedback_counter - 1)

            # case 3: user finished tagging is below - so I can resue my code

        # If everything is correct:

            else:
                # Add data to session:
                session["feedback_counter"] = feedback_counter
                dbText = db.execute("SELECT feedback FROM opinions WHERE id=?", feedback_counter)
                dbNick = db.execute("SELECT nick FROM opinions WHERE id=?", feedback_counter)
                position = ""
                departament = ""

                # Setting the type of decision
                if request.form['pos-neg'] == 'positive':
                    position = "Positive"
                elif request.form['pos-neg'] == 'negative':
                     position = "Negative"

                # Setting the departament
                if request.form['chosen'] == 'IT':
                    departament = "IT"
                elif request.form['chosen'] == 'Legal':
                    departament = "Legal"
                elif request.form['chosen'] == 'Marketing':
                    departament = "Marketing"

                # Puting everything together to the row list
                row = []
                row.append(feedback_counter)
                row.append(dbNick[0]['nick'])
                row.append(position)
                row.append(departament)
                row.append(dbText[0]['feedback'])

                # Adding row list to write to session list
                write_to_session.append(row)

                # Updating session, so it can have a newly created row
                session["c_data"] = write_to_session


                # case 3: user finished judging all the tags
                if(feedback_counter > len(feedback_data) - 1):
                    return render_template("tagged.html", s_data = write_to_session)

                return render_template("tagging.html", s_data = write_to_session, f_data = feedback_data, f_counter = feedback_counter)

    # If the request is GET just render the page
    else:

         return render_template("tagging.html", s_data = write_to_session, f_data = feedback_data, f_counter = feedback_counter)

@app.route("/tagged")
def tagged():
    #if user finished tagging process
    return render_template("tagged.html")
