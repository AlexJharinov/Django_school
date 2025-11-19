# payments/services.py

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product_and_price_for_course(course):
    """
    Создаёт продукт и цену в Stripe для курса, если они ещё не созданы.
    Возвращает (product_id, price_id).
    """
    # если уже есть — просто возвращаем
    if course.stripe_product_id and course.stripe_price_id:
        return course.stripe_product_id, course.stripe_price_id

    # 1. Product
    product = stripe.Product.create(
        name=course.title,
        # можно ещё description, metadata и т.п.
    )

    # 2. Price (цена в центах! поэтому умножаем на 100)
    price = stripe.Price.create(
        unit_amount=int(course.price * 100),
        currency="usd",  # или другая валюта
        product=product.id,
    )

    course.stripe_product_id = product.id
    course.stripe_price_id = price.id
    course.save(update_fields=["stripe_product_id", "stripe_price_id"])

    return product.id, price.id


def create_checkout_session_for_course(course, user=None):
    """
    Создаёт Stripe Checkout Session для оплаты курса.
    Возвращает объект session.
    """
    _, price_id = create_stripe_product_and_price_for_course(course)

    success_url = settings.STRIPE_SUCCESS_URL
    cancel_url = settings.STRIPE_CANCEL_URL

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        # можно положить что-то в metadata
        metadata={
            "course_id": course.id,
            "user_id": getattr(user, "id", None),
        },
    )
    return session
