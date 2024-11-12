# First Flask example
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/") #the app route for slash is the home page for our site, the @ is a wrap around
def index():
    return("Hello World! <p>Welcome to my very boring site.")

# Now Run the application
if __name__ == "__main__":
    app.run(debug=True)