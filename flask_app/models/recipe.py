from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = "recipes_schema"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name,description,instructions,under30,date_made,users_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(under30)s,%(date_made)s,%(users_id)s)"
        print(query)
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append( cls(row))
        return recipes

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def update(cls,data): #goes to model, sends query to database, database handles the data
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,under30=%(under30)s,date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
            query = "DELETE FROM recipes WHERE id = %(id)s;"
            print(query)
            return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        if 'under30' not in recipe:
            flash("Was this under 30 minutes?.", "recipe")
            is_valid = False
        if len(recipe['date_made']) == '': 
            flash("Fill in date", "recipe")
            is_valid = False
        return is_valid
