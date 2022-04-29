from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes/new')
def new_recipe():
    if "users_id" not in session:
        return redirect('/')
    data = {
        "id":session['users_id']
    }
    return render_template('new_recipes.html', user=User.get_by_id(data))

@app.route('/recipe/create',methods=['POST'])
def create_recipe():
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data ={ 
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under30": request.form['under30'],
        "date_made": request.form['date_made'],
        "users_id": session['users_id']
        }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipe_register', methods=['POST'])
def validate_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    return redirect('/dashboard')

@app.route('/recipes/view/<int:id>')
def view(id):
    if "users_id" not in session:
        return redirect('/')
    data ={
        "id":id
    }
    data_user = {
        "id": session['users_id']
    }
    return render_template("show_recipe.html", user=User.get_by_id(data_user),recipe=Recipe.get_by_id(data))

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if "users_id" not in session:
        return redirect('/')
    data ={
        "id":id
    }
    data_user = {
        "id": session['users_id']
    }
    print(data)
    print(data_user)
    return render_template("edit.html", user=User.get_by_id(data_user), recipe=Recipe.get_by_id(data))

@app.route('/recipes/update',methods=['POST'])
def update():
    Recipe.update(request.form)
    print(request.form)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def delete(id):
    data={
        'id':id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')