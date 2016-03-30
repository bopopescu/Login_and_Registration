
from system.core.model import Model

import re

class Registration(Model):
    def __init__(self):
        super(Registration, self).__init__()

    def registration(self, user_details):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors=[]

        if not user_details['first_name']:
            errors.append('First Name cannot be blank.')

        elif len(user_details['first_name'])<2:
            errors.append('First Name must be at least 2 characters long.')

        if not user_details['last_name']:
            errors.append('Last Name cannot be blank.')

        elif len(user_details['last_name'])<2:
            errors.append('Last Name must be at least 2 characters long.')

        if not user_details['email']:
            errors.append('Email cannot be blank.')

        elif not EMAIL_REGEX.match(user_details['email']):
            errors.append('Email format must be valid')

        elif not user_details['reg_password']:
            errors.append('Password cannot be blank.')

        elif len(user_details['reg_password'])<1:
            errors.append("Password must be at least 8 characters long.")

        elif user_details['reg_password']!=user_details['confirm']:
            errors.append('Password and confirmation must match.')



        if errors:
            return {"status": False, "errors":errors}

        else:
            hashed_pw =self.bcrypt.generate_password_hash(user_details['reg_password'])
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(),NOW())"
            data = [user_details['first_name'], user_details['last_name'], user_details['email'], hashed_pw]
            add_user = self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)



        return {"status":True, "user":users[0]}  

    def login(self, login_details):
        password = login_details['password']
        user_query="SELECT * FROM users where email=%s"
        user_data=[login_details['email']]

        users = self.db.query_db(user_query, user_data)

        print users

        if users[0]:
            if self.bcrypt.check_password_hash(users[0]['password'], password):
                return {"status":True, "user":users[0]}
        else:

            return {"status": False}


