import hashlib
from sqlalchemy import Column, Integer, String, Boolean
from backend.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="ReadOnly")  # Admin, Operator, ReadOnly
    is_active = Column(Boolean, default=True)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256 for local authentication context"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)
