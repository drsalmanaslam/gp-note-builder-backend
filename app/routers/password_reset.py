from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
import secrets
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.database import get_db
from app.models import User
from app.auth import get_password_hash

router = APIRouter(prefix="/password-reset", tags=["password-reset"])

# Store reset tokens (in production, use database)
reset_tokens = {}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

def send_reset_email(email: str, token: str):
    """Send password reset email via SendGrid"""
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    
    if not api_key or not from_email:
        print("SendGrid not configured - skipping email")
        return
    
    reset_link = f"https://gp-project-ruddy.vercel.app/reset-password?token={token}"
    
    message = Mail(
        from_email=from_email,
        to_emails=email,
        subject="GP Note Builder - Password Reset",
        html_content=f"""
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>This link expires in 1 hour.</p>
        <p>If you didn't request this, ignore this email.</p>
        """
    )
    
    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
    except Exception as e:
        print(f"Failed to send email: {e}")

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send password reset email"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success even if email not found (security best practice)
    if not user:
        return {"message": "If that email exists, a reset link has been sent."}
    
    # Generate reset token
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
        "user_id": user.id,
        "expires": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    
    # Send email
    send_reset_email(user.email, token)
    
    return {"message": "If that email exists, a reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token"""
    token_data = reset_tokens.get(request.token)
    
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    if datetime.now(timezone.utc) > token_data["expires"]:
        del reset_tokens[request.token]
        raise HTTPException(status_code=400, detail="Token has expired")
    
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    # Remove used token
    del reset_tokens[request.token]
    
    return {"message": "Password reset successfully"}