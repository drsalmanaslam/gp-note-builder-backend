import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

from app.database import get_db
from app.models import User
from app.auth import get_current_active_user

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/stripe", tags=["stripe"])

# ============ CREATE CHECKOUT SESSION ============

@router.post("/create-checkout-session")
def create_checkout_session(
    price_id: str = "price_basic",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe checkout session for subscription."""
    try:
        stripe_price_id = os.getenv("STRIPE_PRICE_BASIC", "price_1TpDI5CmqKOObHdxS6A8HAOn")

        session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            client_reference_id=str(current_user.id),
            mode="subscription",
            line_items=[{
                "price": stripe_price_id,
                "quantity": 1,
            }],
            subscription_data={
                "trial_period_days": 7,
            },
            success_url="http://localhost:5173/login?subscribed=true",

            cancel_url="http://localhost:5173/pricing",
        )
        
        return {"url": session.url}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ CUSTOMER PORTAL ============

@router.post("/customer-portal")
def customer_portal(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe customer portal session."""
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No Stripe customer found")
    
    try:
        session = stripe.billing_portal.Session.create(
            customer=current_user.stripe_customer_id,
            return_url="http://localhost:5173/profile",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ WEBHOOK HANDLER ============

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test")
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    event_type = event["type"]
    data = event["data"]["object"]
    
    if event_type == "checkout.session.completed":
        customer_id = data.get("customer")
        subscription_id = data.get("subscription")
        client_reference_id = data.get("client_reference_id")
        
        if client_reference_id:
            user = db.query(User).filter(User.id == int(client_reference_id)).first()
            if user:
                user.stripe_customer_id = customer_id
                user.stripe_subscription_id = subscription_id
                user.subscription_status = "trialing"
                user.subscription_started = datetime.now(timezone.utc)
                db.commit()
    
    elif event_type == "customer.subscription.updated":
        subscription_id = data.get("id")
        status = data.get("status")
        
        user = db.query(User).filter(User.stripe_subscription_id == subscription_id).first()
        if user:
            if status == "active":
                user.subscription_status = "active"
            elif status == "past_due":
                user.subscription_status = "past_due"
            elif status == "cancelled":
                user.subscription_status = "cancelled"
            db.commit()
    
    elif event_type == "customer.subscription.deleted":
        subscription_id = data.get("id")
        user = db.query(User).filter(User.stripe_subscription_id == subscription_id).first()
        if user:
            user.subscription_status = "cancelled"
            db.commit()
    
    elif event_type == "invoice.payment_succeeded":
        pass
    
    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.subscription_status = "past_due"
            db.commit()
    
    return {"status": "ok"}


# ============ TEST ENDPOINT (Development Only) ============

@router.post("/test-activate-subscription")
def test_activate_subscription(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """DEVELOPMENT ONLY: Manually activate subscription for testing."""
    current_user.subscription_status = "trialing"
    current_user.stripe_customer_id = "cus_test_" + str(current_user.id)
    current_user.stripe_subscription_id = "sub_test_" + str(current_user.id)
    current_user.subscription_started = datetime.now(timezone.utc)
    db.commit()
    return {"message": "Subscription activated (test mode)", "status": current_user.subscription_status}