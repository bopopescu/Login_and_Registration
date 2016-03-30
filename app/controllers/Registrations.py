
from system.core.controller import *

class Registrations(Controller):
    def __init__(self, action):
        super(Registrations, self).__init__(action)

        self.load_model('Registration')

    def index(self):

        return self.load_view('index.html')

    def registration(self):
        user_details={
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'reg_password' : request.form['reg_password'],
        'confirm' : request.form['confirm']

        }

        pword = request.form['reg_password']
        conf= request.form['confirm']
        print "password is " + pword
        print "confirmation is " + conf

        create_status = self.models['Registration'].registration(user_details)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['first_name']
            session['first_name'] = user_details['first_name']

            return redirect('/success')

        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect ('/')

        # session['first_name'] = request.form['first_name']
        # session['last_name'] = request.form['last_name']
        # session['email'] = request.form['email']

        # print session['first_name']
        # print session['last_name']
        # print session['email']


        return redirect('/success')

    def login(self):
        login_details = {
        'email' : request.form['log_email'],
        'password' : request.form['password']
        }

        login = self.models['Registration'].login(login_details)
        if login['status'] == True:
            session['id'] = login['user']['id']
            session['name'] = login['user']['first_name']
            session['first_name'] =  login['user']['first_name']

            return redirect('/success')

        else:
            login['status'] == False
            for message in login:
                flash("Login Fail, try again")
            return redirect ('/')

    def success(self):
        

        return self.load_view('success.html')
