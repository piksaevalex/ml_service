from app.db.database import Base
from sqlalchemy import Column, String, Integer, Identity, LargeBinary


class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, Identity(), primary_key=True)
    model_type = Column(String(255),  nullable=False, unique=False)
    model_name = Column(String(255),  nullable=False, unique=False)
    model_data = Column(LargeBinary(), nullable=False,)

    def serialize(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'model_name': self.model_name,
        }

    def __repr__(self):
        return f'<item id={self.id}  model_type={self.model_type} model_name={self.model_name}>'
