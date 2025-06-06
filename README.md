# Project Name(Image Gallery)

The Image Gallery Application allows users to upload, manage, and view images.

# How to Run

# Frontend

1. Install Node.js and npm/yarn.
2. Navigate to the frontend folder.
3. Run `npm install` or `yarn install`.
4. Run `npm run dev` or `yarn dev`.
5. The frontend should be running on `localhost:5173`.

# Backend

1. Install Python.
2. Navigate to the backend folder.
3. Make sure you are in the same directory where `main.py` and `requirements.txt` files are present.

# Steps to Create a Virtual Environment

1. If you are using Windows, run Git Bash as PowerShell does not allow running scripts.
2. Run `python -m venv env`.
3. Activate the virtual environment by running `source env/Scripts/activate`.
4. Your virtual environment should now be activated.

# Install Requirements

- Run `pip install -r requirements.txt`.

# Set Environment Variables for the Flask App

- Run `export FLASK_APP=main.py`.

# Setup Database(`if the database doesn't exist`)
`Note: If the database already exists and contains the necessary tables, you can skip the steps below for setting up the database.`

1. Run `flask shell` to start the Python shell.
2. Type `from models import db` and press Enter.
3. Type the following lines of code:
```
>>> with app.app_context():
>>>    db.create_all()

```
- Press Enter to execute the code and create the database tables.
- Exit the shell by typing `exit()` and pressing `Enter`.
- Note: After running the above steps, a folder named `instance` with the database should be created.


# Run the Application
- Run `flask run --debug` to start the Flask development server.
- The application should be running on `http://localhost:5173/`



# Features.
- User Login and Signup.
- Password validation with a minimum length of 5 characters.
- Storing password hash in db for security purposes.
- Already stored email verification via the backend.
- Using `JSON Web Tokens` based authentication to log in the user and
  access protected routes via an access token.
- Image upload option for authenticated users only.
- Showing all images with the uploaded user's name to non-authenticated
  users.
- Showing only user-uploaded images to authenticated users.
- Popup modal to view images in a larger size while overlaying the rest of the webpage.
- Allowing authenticated users to delete images uploaded by them.
- Logging out the user by blocklisting the user access token.
- Axios for handling Ajax calls with Axios interceptor to logout the user
  if the user token is expired and he's trying to access the protected
  route.
