from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Team')

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name',
                               validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description', validators=[Length(max=255)])
    completed = BooleanField('Completed')
    team_id = SelectField('Team', coerce=int)  # We'll update choices in the view function
    submit = SubmitField('Add Project')

    def update_teams(self, teams):
        # Update the choices for the team_id field
        self.team_id.choices = [(team.id, team.team_name) for team in teams]