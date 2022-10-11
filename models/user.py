import uuid
import bcrypt
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, DateTime

from app import db


class User(db.Model, UserMixin):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    fullname = Column(String(256))
    username = Column(String(256), primary_key=True, nullable=False)
    password = Column(LargeBinary)
    role = Column(String(128), server_default="user")
    alternative_id = Column(String(128), server_default=uuid.uuid4().hex)
    is_active_user = Column(Boolean(), server_default="true")
    createDate = Column(DateTime(), server_default=func.now())
    updateDate = Column(DateTime(), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.alternative_id)

    def hash_pass(self, password):
        """Hash a password for storing."""
        salt = bcrypt.gensalt()
        pw = password.encode("utf-8")

        self.password = bcrypt.hashpw(pw, salt)

    def verify_pass(self, provided_password):
        """Verify a stored password against one provided by user"""

        return bcrypt.checkpw(provided_password.encode("utf-8"), self.password)

    @classmethod
    def find_by_username(cls, username: str) -> "User":
        return cls.query.filter_by(username=username).first()
