from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from forms import TeamForm, ProjectForm, UpdateTeamForm, DeleteTeamForm, UpdateProfileForm
from model import db, User, Team, Project, connect_to_db
import secrets
import os
from PIL import Image
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)

app.secret_key = "keep this secret"

connect_to_db(app)

user_id = 1

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(random_hex + f_ext)
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    user = User.query.get(user_id)
    if user:
        print(f"User teams: {user.teams}") #debug
        project_form.update_teams(user.teams)
    else:
        print("No user found") #debug    
    return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_id.data

        # Check if team_id is 0 and set it to None
        if team_id == 0:
            team_id = None

        new_project = Project(project_name, completed, team_id, description=description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    
@app.route("/user/<int:user_id>", methods=['GET', 'POST'])
def user_view(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template("404.html"), 404

    update_team_form = UpdateTeamForm()
    delete_team_form = DeleteTeamForm()

    if update_team_form.validate_on_submit():
        team = Team.query.get(request.form.get('team_id'))
        team.team_name = update_team_form.team_name.data
        db.session.commit()
        return redirect(url_for('user_view', user_id=user.id))

    if delete_team_form.validate_on_submit():
        team = Team.query.get(request.form.get('team_id'))
        db.session.delete(team)  # Delete the team directly
        db.session.commit()
        return redirect(url_for('user_view', user_id=user.id))

    return render_template("user_view.html", user=user, update_team_form=update_team_form, delete_team_form=delete_team_form)

@app.route("/user-profile/<int:user_id>", methods=['GET', 'POST'])
def user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template("404.html"), 404

    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.profile_picture = picture_file

        user.update_text = form.update_text.data
        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user_profile', user_id=user.id))

    image_file = url_for('static', filename='profile_pics/' + (user.profile_picture if user.profile_picture else 'default.png'))

    return render_template('user_profile.html', user=user, form=form, image_file=image_file)

if __name__ == "__main__":
    app.run(debug = True)