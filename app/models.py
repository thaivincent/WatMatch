from typing import Optional
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)  # Account creation timestamp

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Timetable(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    course_code: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)  # e.g., "CS 135"
    start_time: so.Mapped[datetime] = so.mapped_column(nullable=False)  # Class start time
    end_time: so.Mapped[datetime] = so.mapped_column(nullable=False)  # Class end time
    section: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))  # Optional section/lab info

    # Relationship to User
    user: so.Mapped["User"] = so.relationship(back_populates="timetable")

    def __repr__(self):
        return f'<Timetable {self.course_code} for User {self.user_id}>'

class SocialMedia(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    platform: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)  # e.g., "Discord", "Instagram"
    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)  # e.g., "user#1234", "@username"

    # Relationship to User
    user: so.Mapped["User"] = so.relationship(back_populates="social_media")

    def __repr__(self):
        return f'<SocialMedia {self.platform}: {self.username} for User {self.user_id}>'
    
class Preferences(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True, unique=True)
    is_timetable_public: so.Mapped[bool] = so.mapped_column(default=True)  # Privacy setting
    
    # Relationship to User
    user: so.Mapped["User"] = so.relationship(back_populates="preferences")

    def __repr__(self):
        return f'<Preferences for User {self.user_id}>'   