from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class UpdateProfileForm(FlaskForm):
    update_text = StringField('Post an update', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class UpdateTeamForm(FlaskForm):
    team_name = StringField('Team Name')
    submit = SubmitField('Update Team')

class DeleteTeamForm(FlaskForm):
    submit = SubmitField('Delete Team')

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Team')

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name',
                               validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description', validators=[Length(max=255)])
    completed = BooleanField('Completed')
    team_id = SelectField('Team', coerce=int, choices=[])  # Set initial choices to empty
    submit = SubmitField('Add Project')

    def update_teams(self, teams):
        # Update the choices for the team_id field
        print(f"Updating teams: {teams}")
        self.team_id.choices = [(0, 'No team')] + [(team.id, team.team_name) for team in teams]  # Add an option for no team

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')