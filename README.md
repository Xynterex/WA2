**Taekwondo Physical Training Tracker**


**Purpose**

This web app allows Taekwondo CCA members and EXCOs to make an account and submit forms to acknowledge that a PT (Physical Training) is done or to set new PT.

The application allows for a ease-of-use method of communication between both parties on the PT completion statuses. Therefore, members will stay on task and will be clear on the PT to do and their respective due dates.


**Description**

The front-end application is done using HTML/CSS/JS which mainly consists to inputs and forms to enter account details or PT completion statuses.

The back-end application is done using Flask(Python) as the server and a .db database file. The server processes inputs and forms and mainly verifies account details and send queries to the database to store the updated data.

The features are as follows:

**Sign Up Process**

Anyone can enter a username and password in the sign up page.
The name cannot match any other name that is used for another account.
The password requires a minimum length of 8 and a numeric, lower and upper character each.
Users must select if they are signing up as a member or an EXCO. An EXCO pin is required for the latter.

**Log In Process**

Similar to the sign up process, users are required to fill in their name and password and select if they are a member or EXCO.
An EXCO pin is required for the latter.

**Member Account**

A table will display each PT per row with the following details:

- PT ID
- Name
- Sets
- Reps
- Description
- Assigned Date
- Due Date

A form is provided for members to select the PT ID of the Physical Training that they have completed.

**EXCO Account**

The account will have the same features as the member account mentioend. Essentially, an EXCO still needs to do the PT that the members have to do.

Additionally, a form is provided to add a new PT with the following details:

- Name (required)
- Description
- Number of Sets (required)
- Number of Reps
- Duration of PT in days (required; starting from the date assigned)

**Security**

The use of a global account ID variable is used to ensure that the user has to login everytime the web app starts running. The various routes will change the variable accordingly and reroute to the homepage if the ID variable does not match.

**Challenges Encountered**

Lots of bugs here and there, mainly in the main.py file (no pun intended)
The sqlite3 lines are new to me so it took a lot of print statements to obtain the desired output to be returned to the html templates.

The css styling was a small challenge as I needed to figure out how to make the fonts and elements of appropriate sizes for laptop and phone screens.

**What I learned**

Patience is the key. Often times, I had to print variables and check the console after every action to understand what is going on in the python program.

Being open-minded. As I was encouraged to try out out of syllabus tasks like front-end processing and deployment, I took my research to the free online resources to pick them up.

Independece. Picking new skills up on my own wasn't easy. With the other two virtues learnt, I did so independently and confidently.

Lastly, don't take website applications for granted. Never will I ever visit a website without at least thinking of some of the processing, styling or structure that runs them.

**What's Next**

I notice that the runtime instance lasts as long as the web app is running (a misconception on my part that entering the web app will create a new instance).

Therefore, I will consider learning how to create individual global variables for each client such that they are be obtained and updated across routes.

As for the app's overall purpose, I am still uncertain if my CCA will accept this web app to replace their use a few flat xlsx files.

Well I have had a conversation with my CCA Captain who was curious what these H2 Computing geeks are up to for WA2, for which I shared about the general scope, not so about my own submission.

Perhaps if I could have another nice chat with him, could we discuss a plan to utilise the web app.

If so, I, as a responsible H2 computing student, have to work on the feedback of my clients (aka my CCA mates and EXCOs) and improve on the security and integrity of the application.

We'll see how first... But in the meantime, I'll do some youtube videos. :)
