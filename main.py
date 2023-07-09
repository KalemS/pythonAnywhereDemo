from flask import Flask, render_template, url_for, flash, redirect, url_for, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import git
app = Flask(__name__)                    
# this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '8ecdaee7a5c293f5f359d5717ee6ea0f'

@app.route("/")            
@app.route("/home")              
# this tells you the URL the method below is related to
def hello_world():
     return render_template('home.html', subtitle='Home Page', text='This is the home page')
    # this prints HTML to the webpage

@app.route("/second_page")
def second_page():
   return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/CHANGE_TO_PYTHON_ANYWHERE_USERNAME/CHANGE_TO_GITHUB_REPO_NAME')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':               
  # this should always be at the end
    app.run(debug=True, host="0.0.0.0")