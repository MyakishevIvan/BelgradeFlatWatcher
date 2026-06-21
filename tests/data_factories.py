from datetime import date

from pygments.lexers import data

from data_base.models.subscriptions_model import Subscription
from data_base.models.seen_flats_model import SeenFlat
from pages.components.flat_components.flat import Flat
from services.flats.search_filters import SearchFilters


def make_filter() -> SearchFilters:
    return SearchFilters(
        min_price='450',
        max_price='500',
        min_square='20',
        max_square='45',
        rooms_type='1',
    )

def make_flats_list(flats_count: int = 60) -> list[Flat]:
    flats_list = []
    for i in range(flats_count):
        flats_list.append(make_flat(flat_id=i))
        
    return flats_list

def make_flat(flat_id: int = 1) -> Flat:
    return Flat(
        id=flat_id,
        url=f'https://test.com/flats/{flat_id}',
        name=f'Test flat {flat_id}',
        price='300',
        square='40',
        publication_date=date.today(),
    )


def make_subscription(user_id: int = 1) -> Subscription:
    return Subscription.from_filters(
        telegram_user_id=user_id,
        chat_id=user_id,
        filters=make_filter(),
    )


def make_seen_flat(user_id: int = 1, flat_id: int = 1) -> SeenFlat:
    return SeenFlat.from_flat(
        telegram_user_id=user_id,
        flat=make_flat(flat_id),
    )