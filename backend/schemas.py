from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    line_token: Optional[str] = None
    line_otp: Optional[str] = None
    line_otp_expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class LineOTPResponse(BaseModel):
    otp: str
    expires_at: datetime

class UserProfileUpdate(BaseModel):
    """使用者個人資料更新"""
    email: Optional[EmailStr] = None
    line_token: Optional[str] = None

class ProductBase(BaseModel):
    url: str
    name: str
    image_url: Optional[str] = None
    current_price: Optional[float] = None

class ProductResponse(ProductBase):
    id: UUID
    last_checked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class SubscriptionBase(BaseModel):
    product_url: str # User inputs URL
    target_price: float
    notify_method: str = "EMAIL" # EMAIL, LINE, BOTH

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    """訂閱項目更新"""
    target_price: Optional[float] = None
    notify_method: Optional[str] = None  # EMAIL, LINE, BOTH

class SubscriptionResponse(BaseModel):
    id: UUID
    target_price: float
    notify_method: str
    is_active: bool
    created_at: datetime
    product: ProductResponse

    model_config = {"from_attributes": True}
