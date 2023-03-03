# # models.py
# from typing import Optional
# from pydantic import BaseModel, EmailStr
#
# from sqlalchemy import Column, String, Integer
#
# from database import Base, engine
#
#
# class User(Base):
#     __tablename__ = 'user'  # 数据库表名
#
#     username = Column(String(255), nullable=False)
#     uid = Column(Integer, primary_key=True)
#     password = Column(String(255), nullable=False)
#
#
#
#
# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
#
