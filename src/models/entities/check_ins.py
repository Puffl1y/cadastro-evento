from src.models.settings.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeigKey
from sqlalchemy.sql import func

class CheckIns(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True)
    creat_at = Column(DateTime, default = func.now())
    attendeeId = Column(String, ForeigKey("attendees.id"))


    def __repr__(self):
        return f"Check_ins [attendeeId={self.attendeeId}]"