from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField, FloatField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from ..models import Brand, Theme, Category


class AddProduct(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(1, 64)])
    price = StringField("Preço", validators=[DataRequired()])
    description = TextAreaField("Descrição", validators=[DataRequired()])
    players = IntegerField("Jogadores", validators=[DataRequired()])
    age = StringField("Idade", validators=[DataRequired(), Length(1, 15)])
    brand = SelectField('Marca', coerce=int)
    theme = SelectField('Tema', coerce=int)
    category = SelectField("Categoria", coerce=int)
    image = FileField("Imagem", validators=[FileRequired(), FileAllowed(['jpg','png', 'gif', 'jpeg'], "Images only")])
    submit = SubmitField("Enviar")

    def __init__(self, *args, **kwargs):
        super(AddProduct, self).__init__(*args, **kwargs)
        self.brand.choices = [(brand.id, brand.name)
                              for brand in Brand.query.order_by(Brand.name).all()]
        self.theme.choices = [(theme.id, theme.name)
                              for theme in Theme.query.order_by(Theme.name).all()]
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class EditProduct(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(1, 64)])
    price = StringField("Preço", validators=[DataRequired()])
    description = TextAreaField("Descrição", validators=[DataRequired()])
    players = IntegerField("Jogadores", validators=[DataRequired()])
    age = StringField("Idade", validators=[DataRequired(), Length(1, 15)])
    brand = SelectField('Marca', coerce=int)
    theme = SelectField('Tema', coerce=int)
    category = SelectField("Categoria", coerce=int)
    image = FileField("Imagem", validators=[
        FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                    "Images only")])
    submit = SubmitField("Enviar")

    def __init__(self, *args, **kwargs):
        super(EditProduct, self).__init__(*args, **kwargs)
        self.brand.choices = [(brand.id, brand.name)
                              for brand in Brand.query.order_by(Brand.name).all()]
        self.theme.choices = [(theme.id, theme.name)
                              for theme in Theme.query.order_by(Theme.name).all()]
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class AddBrand(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(1, 25)])
    submit = SubmitField("Enviar")

    def validate_name(self, field):
        if Brand.query.filter_by(name=field.data).first():
            raise ValidationError('Marca já cadastrada!')


class AddTheme(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(1, 25)])
    submit = SubmitField("Enviar")

    def validate_name(self, field):
        if Theme.query.filter_by(name=field.data).first():
            raise ValidationError('Tema já cadastrado!')


class AddCategory(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(1, 25)])
    submit = SubmitField("Enviar")

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Categoria já cadastrada!')


