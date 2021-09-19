from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Role, User

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Nome', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Nomes de usuários devem ter apenas letras, números, pontos ou'
               'underscores')])
    cpf = StringField('CPF', validators=[DataRequired(), Length(1, 11)])
    telephone = StringField('Telefone', validators=[DataRequired(),
                                                    Length(1, 11)])
    confirmed = BooleanField('Confirmado')
    role = SelectField('Role', coerce=int)
    address = StringField('Endereço', validators=[DataRequired(),
                                                  Length(1, 100)])
    number = StringField('Número', validators=[DataRequired(), Length(1, 10)])
    zipcode = StringField('CEP', validators=[DataRequired(), Length(1, 8)])
    neighborhood = StringField('Bairro', validators=[DataRequired(),
                                                     Length(1, 64)])
    complement = StringField('Complemento', validators=[DataRequired(),
                                                        Length(1, 64)])
    city = StringField('Cidade', validators=[DataRequired(), Length(1, 64)])
    state = StringField('Estado', validators=[DataRequired(), Length(1, 2)])
    submit = SubmitField('Enviar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Esse email já está em uso!')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Esse nome de usuário já está em uso!')

    def validate_telephone(self, field):
        if field.data != self.user.telephone and \
                User.query.filter_by(telephone=field.data).first():
            raise ValidationError('Número de telefone já está em uso!')

    def validate_cpf(self, field):
        if field.data != self.user.cpf and \
                User.query.filter_by(cpf=field.data).first():
            raise ValidationError('Esse cpf já está em uso!')


class EditProfileForm(FlaskForm):
    telephone = StringField('Telefone', validators=[DataRequired(),
                                                    Length(1, 11)])
    address = StringField('Endereço', validators=[DataRequired(),
                                                  Length(1, 100)])
    number = StringField('Número', validators=[DataRequired(), Length(1, 10)])
    zipcode = StringField('CEP', validators=[DataRequired(), Length(1, 8)])
    neighborhood = StringField('Bairro', validators=[DataRequired(),
                                                     Length(1, 64)])
    complement = StringField('Complemento', validators=[DataRequired(),
                                                        Length(1, 64)])
    city = StringField('Cidade', validators=[DataRequired(), Length(1, 64)])
    state = StringField('Estado', validators=[DataRequired(), Length(1, 2)])
    submit = SubmitField('Enviar')

    def validate_telephone(self, field):
        if User.query.filter_by(telephone=field.data()).first():
            raise ValidationError('Número de telefone já em uso!')




