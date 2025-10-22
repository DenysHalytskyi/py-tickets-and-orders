from django.db import transaction

from db.models import Order, Ticket, User, MovieSession
from datetime import datetime


def create_order(tickets: list[dict], username: str, date: datetime | None = None) -> Order:
    with transaction.atomic():
        user, _= User.objects.get_or_create(username=username)

        if date:
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)

        for tickets_data in tickets:
            Ticket.objects.create(
                movie_session_id=tickets_data["movie_session"],
                order=order,
                row=tickets_data["row"],
                seats=tickets_data["seat"],
            )

        return order

def get_orders(username: str | None = None) -> list[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            return Order.objects.none()
    else:
        return Order.objects.all()