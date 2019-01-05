import psycopg2
import json
from werkzeug.security import generate_password_hash, check_password_hash


class Database(object):
    """class for the database"""

    def __init__(self):
        """initialize  connection """
        try:
            """
            creates a db
            """

            self.connection = psycopg2.connect(host="localhost", database="iReporter", users="postgres", password="nataliepostgres")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.create_tables()
        except(Exception, psycopg2.DatabaseError) as e:
            print('There was an error' + str(e))

    def create_tables(self):

        """ create tables """
        create_table = """CREATE TABLE users
            (user_id SERIAL PRIMARY KEY, first_name VARCHAR(30),last_name VARCHAR(30), other_name VARCHAR(30), username VARCHAR(30),
            email VARCHAR(50),password VARCHAR(150), phone_number VARCHAR(100),
            isAdmin BOOLEAN DEFAULT FALSE )"""
        self.cursor.execute(create_table)
        self.connection.commit()

        try:
            password = generate_password_hash('useradmin')
            sql = """INSERT INTO users(user_id,first_name, last_name, other_name, username, password, phone_number,email,isAdmin)
                    VALUES (001,'Abio','Nataline','talie','abbie',{},'0752030815','abionatline@gmail.com',True)""".format(password)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as ex:
            return str(ex)

        create_table = """ CREATE TABLE redflags(
            flag_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            description VARCHAR (500),
            user_email VARCHAR (50),
            status VARCHAR (25) DEFAULT 'Action to be taken',
            location VARCHAR (50),
            createdby VARCHAR(50)
            createdOn NOT NULL DEFAULT CURRENT_TIMESTAMP,last_modifiedOn DEFAULT CURRENT_TIMESTAMP)"""
        self.cursor.execute(create_table)
        self.connection.commit()

    def insert_into_user(self, firstname, lastname, othername, username, email, phone_number,password):
        """
        Query to add a new user
        :admin,user
        """
        user = """INSERT INTO users(firstname, lastname, othername, username, email, phone_number,password)
                VALUES ('{}','{}','{}','{}','{}','{}','{}');
                """.format(firstname, lastname, othername, username, email, phone_number,password)
        self.cursor.execute(user)
        self.connection.commit()

    def insert_into_redflag(self, redflag_description, user_id, user_email, status,createdby, location):
        """
        Query for a user to add a new redflag to the database
        """
        redflag_query = """INSERT INTO redflag(redflag_description, user_id, user_email, status,createdby, location)
                    VALUES('{}','{}','{}','{}','{}','{}'); """.format(redflag_description, user_id, user_email, sender_phonenumber, username_name, location)
        self.cursor.execute(redflag_query)
        self.connection.commit()

    def get_all_redflags(self):
        """
        Query gets all redflag-posts that are available
        :admin
        """

        self.cursor.execute("SELECT * FROM redflags")
        all_redflags = self.cursor.fetchall()
        redflag_list = []
        for redflag in all_redflags:
            redflag_list.append(redflag)
        return redflag_list

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        user_list = []
        for user in users:
            user_list.append(user)
        return user_list

    def get_redflag_by_value(self, table_name, table_column, value):
        """
        Function  gets items from the
        same table with similar ids :admin
        """
        try:

            query = "SELECT * FROM {} WHERE {} = '{}';".format(
                table_name, table_column, value)
            self.cursor.execute(query)
            results = self.cursor.fetchone()
            return results
        except Exception as e:
            return None

    def get_user_by_value(self, table_name, column, value):
        """
        Function  gets items from the
        same table with similar email :email
        """
        query = "SELECT * FROM {} WHERE {} = '{}';".format(table_name, column, value)
        self.cursor.execute(query)
        results = self.cursor.fetchone()
        return results

    def get_user_redflags(self, user_id):
        """
        Select from redflags where redflag.user_id = user.user_id
        :Admin
        """
        query = "SELECT * FROM  redflags WHERE user_id = '{}';".format(user_id)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            return results
        return "No redflags yet"

    def update_redflag_status(self, stat, id):
        """
        update table redflags set status ='' where redflag_id = id
        :Admin
        """

        status = ['Resolved', 'under_investigation', 'Rejected', 'on_going']
        if stat in status:
            query = """UPDATE redflags SET status = '{}'
                        WHERE redflag_id ='{}' """.format(stat, id)
            self.cursor.execute(query)
            self.connection.commit()
            return "status updated successfully"
        return "status error"

    def is_post_Resolved(self, id):
        sql = "SELECT status FROM redflags WHERE redflag_id ='{}'".format(id)
        self.cursor.execute(sql)
        self.connection.commit()
        post = self.cursor.fetchone()
        status = post[0]
        if status == 'Resolved':
            return True
        return False

    def update_role(self, id):
        query = """UPDATE users SET is_admin = {}
                    WHERE user_id ='{}' """.format(True, id)
        self.cursor.execute(query)
        self.connection.commit()

    def revoke_admin_previledges(self, id):
        query = """UPDATE users SET is_admin = {}
                    WHERE user_id ='{}' """.format(False, id)
        self.cursor.execute(query)
        self.connection.commit()

    def delete_table_column(self, table_name, table_colum, id):
        delete_query = "DELETE from {} WHERE {} = '{}';".format(
            table_name, table_colum, id)
        self.cursor.execute(delete_query)
        self.connection.commit()

    def change_present_location(self, location, redflag_id):
        query = "UPDATE  redflags SET location = '{}' WHERE redflag_id ={};".format(location, redflag_id)
        self.cursor.execute(query)
        self.connection.commit()

    def cancel_redflag(self, id):
        sql = "UPDATE redflags SET status='{}' WHERE redflag_id = '{}'".format('cancelled', id)
        self.cursor.execute(sql)
        self.connection.commit()
        return self.get_redflag_by_value('redflags', 'redflag_id', id)

    def is_redflag_owner(self, redflag_id, user_id):
        sql = "SELECT user_id FROM redflags WHERE user_id ='{}'".format(user_id)
        self.cursor.execute(sql)
        self.connection.commit()
        post = self.cursor.fetchone()
        if post:
            return True
        return False

    def drop_tables(self):
        drop_query = "DROP TABLE IF EXISTS {0} CASCADE"
        tables = ["users", "redflags"]
        for table in tables:
            self.cursor.execute(drop_query.format(table))

    def isAdmin(self, user_id):
        sql = "SELECT isAdmin from users WHERE user_id ={}".format(user_id)
        self.cursor.execute(sql)
        self.connection.commit()
        results = self.cursor.fetchone()
        return results[0]

    def get_user_email(self, user_id):
        sql = "SELECT email from users WHERE user_id ={}".format(user_id)
        self.cursor.execute(sql)
        self.connection.commit()
        results = self.cursor.fetchone()
        return results[0]

    def change_status(self, param, id):
        query = "UPDATE redflags SET status = '{}' WHERE redflag_id ={};".format(param, id)
        self.cursor.execute(query)
        self.connection.commit()

    def new_redflag_has_fishy_behaviour(self, user_id, reciever_email, desc):
        sql = "SELECT * FROM redflags WHERE user_id = {} AND recipient_email= '{}' and redflag_description = '{}'".format(
            user_id, reciever_email, desc)
        self.cursor.execute(sql)
        self.connection.commit()
        results = self.cursor.fetchall()
        return results

    def get_location(self, id):
        query = "SELECT location FROM redflags WHERE redflag_id={}".format(id)
        self.cursor.execute(query)
        self.connection.commit()
        results = self.cursor.fetchone()
        return results[0]

    def get_redflag_owner_id(self, id):
        query = "SELECT user_id FROM redflags WHERE redflag_id={}".format(id)
        self.cursor.execute(query)
        self.connection.commit()
        results = self.cursor.fetchone()
        return results[0]

