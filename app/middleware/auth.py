from fastapi import Depends, HTTPException, status
from app.auth import get_current_active_user
from app.models import User

async def get_current_admin(current_user: User = Depends(get_current_active_user)):
    """Check if the current user is an admin."""
    print(f"Checking admin status for user: {current_user.username}, role: {current_user.role}")  # Debug
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    return current_user

async def get_current_user_or_admin(current_user: User = Depends(get_current_active_user)):
    return current_user

def require_admin():
    return Depends(get_current_admin)

def require_user():
    return Depends(get_current_active_user)