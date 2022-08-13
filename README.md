# Tag Tool
#### Video Demo:  https://youtu.be/nhLyz9O2msE
#### Description:
This is a flask application, which is responsible for helping the companies categorize the feedback they get from customers, so the right people can get to know it and potentialy take action about it.
##### How it works?
The user is deciding if given feedback about the company is good or bad and also what departament should recive it. It is made by the user based on the comment from client he recive and he can see all his decison in the "database" on the right side of the panel (however it's not a real database because I assumed that more users then one will be using my app so it will be a trouble to clear it, instead my application is using session storage).

Tag Tool is consisting of:
- app.py - the most important file here! It is responsible for all the things you see, sucha as: managing values in session, connecting to database, catching and reacting to errors and of course rendering to you all this sites. More about it you can see below.
- templates folder - folder consisting of: layout.html, index.html, tagging.html and tagged.html - which are sites that you can see yourself
- static folder - consisting of style.css (application is build on bootstrap, however I sometimes use css, I don't yet know how to do everything in this awesome framework)
- tagdatabase.db - a database containing opinions table which has 3 rows (id, nick, feedback). Data from it is being used in this application.
- flask_session folder - storing session values

###### Logic behind app.py
This file is creating/clearing session when user enters index.html (which is the site you are reading now). Session consist of two types of data:
- counter - which is required mainly to show the next feedback text in feedback panel. This value is being increased everytime the user press the next button.
- c_data - which is responsible for storing your tagged results in your session. Application is also using it to generate table on the right on the panel.

The application was created in such a way that prevents errors: it catches if user didin't clicked the positive/negative button or didn't choose the department at all. It also redirect the user to tagged.html when he finished the tagging process preventing counter from asking endlessly about feedback from database.

The most important thing is however the fact that app.py is putting collected data (from form and database) together and inserting it to the List called "row". Then the raw is being appended() to c_data and passed to tagging.html

###### tagging.html
This file is responsible for showing the user form inputs and POST them to app.py. This site is being rendered as long as user didin't reach the end of feedback comments (in such a case - app.py is rendering similar page called tagged.html). As mentioned above this page is showing feedback comment in feedback panel collected from database with the id of counter. It also contains 2 for loops, which are responsible for generating the table on the righ of the panel

I think that the most interesting thing on this site are buttons, which are actually not a buttons but radio type of input (to create them I used this [trick](https://getbootstrap.com/docs/5.0/forms/checks-radios/) from bootstrap documentation). To make them work i also used javascript, which is assigning the name="chosen" attribute to the button currently pressed and then this checkbox value is being sent via POST to app.py, enabling it to collect it's value

##### Special thanks
To be honest I don't really like python (JS is much better choice for me) but i don't know enough of node.js so I python for my backend. I had some minior problems, but fortunately I found some solution on stackoverflow, so I would like to thank:

User: Miguel Grinberg - for an idea of how to create button which sends it's value via POST (especially the if statement in python) [link](https://stackoverflow.com/questions/19794695/flask-python-buttons) - his code was adapted to work in my application, under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

Users: Pablo Castellazzi and Thomas K - for an idea of how to check for an exsistance of value which are being POSTed [link](https://stackoverflow.com/questions/6362047/how-to-check-if-a-name-value-pair-exists-when-posting-data) - their code solutions were adapted to work in my application, under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

Last but not least I would like to thank CS50 team for making it all possible and also for Finance problem set, which introduced me to Flask and helped me with some issues I had with Tag Tool.