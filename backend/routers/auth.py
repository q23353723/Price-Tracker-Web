from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import database, models, schemas, auth, notifier

router = APIRouter(tags=["Authentication"])

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(auth.get_current_user)):
    """取得目前登入使用者的個人資料"""
    return current_user

@router.put("/me/profile", response_model=schemas.UserResponse)
def update_user_profile(
    profile: schemas.UserProfileUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """更新使用者個人資料（email、Line User ID）"""
    if profile.email is not None and profile.email != current_user.email:
        # 檢查新 email 是否已被使用
        existing = db.query(models.User).filter(models.User.email == profile.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = profile.email

    if profile.line_token is not None:
        # 檢查是否為解除綁定（原本有 token，現在傳入空字串或 null）
        is_unlinking = bool(current_user.line_token) and not profile.line_token.strip()

        if is_unlinking:
            try:
                notifier.send_line_message(current_user.line_token, "⚠️ 您已成功解除 Line 價格追蹤通知綁定！\n\n未來若想重新收到通知，請隨時登入網頁重新綁定喔。")
            except Exception as e:
                print(f"Failed to send unlink notification: {e}")

        current_user.line_token = profile.line_token if profile.line_token.strip() else None
        
        if not current_user.line_token:
             # 如果是解除綁定，順便清空可能遺留的 OTP
             current_user.line_otp = None
             current_user.line_otp_expires_at = None

    db.commit()
    db.refresh(current_user)
    return current_user

import random
from datetime import datetime

@router.post("/me/line-otp", response_model=schemas.LineOTPResponse)
def generate_line_otp(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """產生 LINE 綁定用的 6 位數一次性驗證碼"""
    # 產生 6 位數數字字串
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    current_user.line_otp = otp
    current_user.line_otp_expires_at = expires_at
    db.commit()

    return {"otp": otp, "expires_at": expires_at}

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # Helper endpoint for JSON body login (easier for frontend)
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
