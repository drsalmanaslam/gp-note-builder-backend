from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Any

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    role: Optional[str] = 'user'

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: str = 'user'
    subscription_status: Optional[str] = 'inactive'
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(UserResponse):
    hashed_password: str

# ============ CATEGORY SCHEMAS ============
class CategoryBase(BaseModel):
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = '#3B82F6'

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    template_count: int = 0
    
    class Config:
        from_attributes = True

# ============ TEMPLATE SCHEMAS ============
class TemplateBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    content: dict
    is_public: bool = True

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[dict] = None
    is_public: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: int
    version: int
    view_count: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    creator: Optional[UserResponse]
    is_favourite: bool = False
    category_id: Optional[int] = None
    category_details: Optional[CategoryResponse] = None  # ✅ NOW WORKS
    
    class Config:
        from_attributes = True

class TemplateVersionResponse(BaseModel):
    id: int
    template_id: int
    version: int
    content: dict
    changes: Optional[str]
    created_at: datetime
    created_by: Optional[int]
    
    class Config:
        from_attributes = True
class TemplateBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    content: dict
    is_public: bool = True
    red_flags: Optional[List[dict]] = []  # NEW

class TemplateResponse(TemplateBase):
    id: int
    version: int
    view_count: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    creator: Optional[UserResponse]
    is_favourite: bool = False
    category_id: Optional[int] = None
    category_details: Optional[CategoryResponse] = None
    
    class Config:
        from_attributes = True

# ============ FAVOURITES & ACTIVITY ============
class FavouriteResponse(BaseModel):
    template_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    id: int
    template_id: int
    action: str
    created_at: datetime
    template: Optional[TemplateResponse]
    
    class Config:
        from_attributes = True

# ============ CONSULTATION NOTE SCHEMAS ============
class NoteQuestionAnswer(BaseModel):
    question_id: str
    value: Any

class NoteSectionData(BaseModel):
    section_id: str
    title: str
    answers: List[NoteQuestionAnswer]

    class Config:
        from_attributes = True