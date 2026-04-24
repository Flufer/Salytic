import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


def create_checkout_session(user_id: str):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price": os.environ.get("STRIPE_PRICE_ID"),
            "quantity": 1,
        }],
        success_url="https://your-app.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://your-app.com/cancel",
        metadata={
            "user_id": user_id
        }
    )

    return session.url