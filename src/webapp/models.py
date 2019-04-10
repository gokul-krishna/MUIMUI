from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt


class User(db.Model, UserMixin):

    """ A user who has an account on the website. """

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        """ Returns First Name and Last Name"""
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        """ Returns Password """
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """ Generates hashed password"""
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        """ Checks password entered by user with original password """
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        """ Returns user's email """
        return self.email


class InstaInfluencer(db.Model):
    """ Instagram influencer's table """

    __tablename__ = 'insta_influencer'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    user_handle = db.Column(db.String)
    user_last_scrapped = db.Column(db.DateTime)


class Products(db.Model):
    """Product inventory table
    """

    __tablename__ = 'products'

    """
    TYPES = [('babana_republic', 'Banana Republic'),
             ('hm', 'H&M'),
             ('topshop', 'TopShop'),
             ('mango', 'Mango'),
             ('macys', "Macy's")]
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    page_link = db.Column(db.String)
    date_scrapped = db.Column(db.DateTime)
    image_link = db.Column(db.String)
    price = db.Column(db.Float)
    origin_site = db.Column(db.String)
