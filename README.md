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
