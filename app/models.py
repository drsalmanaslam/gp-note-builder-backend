from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Association table for many-to-many relationship between users and favourite templates
user_favourites = Table(
    'user_favourites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('template_id', Integer, ForeignKey('templates.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default='user')
    subscription_status = Column(String(20), default='inactive')  # inactive, trialing, active, cancelled, past_due
    stripe_customer_id = Column(String(100), unique=True, nullable=True)
    stripe_subscription_id = Column(String(100), unique=True, nullable=True)
    subscription_plan = Column(String(50), nullable=True)  # basic, pro, enterprise
    subscription_started = Column(DateTime(timezone=True), nullable=True)
    subscription_expires = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    templates = relationship("Template", back_populates="creator", cascade="all, delete-orphan")
    favourite_templates = relationship("Template", secondary=user_favourites, back_populates="favourited_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)
    content = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    is_public = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # ← ADD THIS LINE
    
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    
    # ... rest of the code
    
    # NEW: Share fields
    share_token = Column(String(100), unique=True, index=True, nullable=True)
    share_created_at = Column(DateTime(timezone=True))
    share_views = Column(Integer, default=0)
    share_expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    creator = relationship("User", back_populates="templates")
    favourited_by = relationship("User", secondary=user_favourites, back_populates="favourite_templates")
    category_rel = relationship("Category", backref="templates")  # NEW: Relationship to Category

class TemplateVersion(Base):
    __tablename__ = "template_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)
    version = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    changes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    
    # Relationships
    template = relationship("Template", backref="versions")
    creator = relationship("User")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    icon = Column(String(50))
    description = Column(Text)
    color = Column(String(20), default='#3B82F6')  # NEW: Color for category
    is_active = Column(Boolean, default=True)      # NEW: Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"
class UserActivity(Base):
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)
    action = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    template = relationship("Template")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    theme = Column(String(20), default='light')
    language = Column(String(10), default='en')
    notifications_enabled = Column(Boolean, default=True)
    email_frequency = Column(String(20), default='daily')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", backref="preferences")
    
    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, theme='{self.theme}')>"

