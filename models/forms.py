from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, url
from wtforms import StringField, PasswordField, SubmitField, URLField, HiddenField, SelectField


class LoginForm(FlaskForm):
    username = StringField('Username',
                           id='inputUsername',
                           name="username",
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             id='inputPassword',
                             name="password",
                             validators=[DataRequired()])
    submit = SubmitField(label=('Login'))


class AddServerForm(FlaskForm):
    server_name = StringField('Server Name',
                              id='servername',
                              name="servername",
                              validators=[DataRequired()])

    server_url = URLField("Server URL",
                          id="serverurl",
                          name="serverurl",
                          validators=[DataRequired(), url(require_tld=False)])

    submit = SubmitField(label=('Add Server'))


class EditServerForm(FlaskForm):
    server_id = HiddenField(name="id")

    server_name = StringField('Server Name',
                              id='servername',
                              name="servername",
                              validators=[DataRequired()])

    server_url = URLField("Server URL",
                          id="serverurl",
                          name="serverurl",
                          validators=[DataRequired(), url(require_tld=False)])

    submit = SubmitField(label=('Edit Server'))


class UserRegister(FlaskForm):
    full_name = StringField('Full Name',
                            id='inputFullname',
                            name="fullname",
                            validators=[DataRequired()])
    username = StringField('Username',
                           id='inputUsername',
                           name="username",
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             id='inputPassword',
                             name="password",
                             validators=[DataRequired()])
    role = SelectField("User Role",
                       id="inputRole",
                       name="role",
                       choices=[("admin", "Admin"), ("user", "User")])
    submit = SubmitField(label=('Register'))
