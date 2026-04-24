import os
import stripe
from flask import Flask, request
from app import load_usage, save_usage

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")


@app.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return {"error": str(e)}, 400

    # 💳 УСПЕШНАЯ ОПЛАТА
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]

        data = load_usage()

        if user_id in data:
            data[user_id]["is_paid"] = True
            save_usage(data)

        print(f"[STRIPE] User upgraded: {user_id}")

    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(port=4242)