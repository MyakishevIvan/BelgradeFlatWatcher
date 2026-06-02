import asyncio

from data_base.models.subscriptions_model import Subscription
from pages.components.flat_components.flat import Flat
from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository
from services.flats.search_executor import SearchExecutor
from services.flats.search_filters import SearchFilters
from services.telegram.telegram_search_utils import build_filters_from_model, convert_to_model


class FlatsService:
    def __init__(
            self,
            search_executor: SearchExecutor,
            flats_repo: SeenFlatRepository,
            subscribe_repo: SubscriptionRepository,
    ) -> None:
        self._flats_repo = flats_repo
        self._subscribe_repo = subscribe_repo
        self._search_executor = search_executor

    async def search_by_filters(self, filters: SearchFilters) -> list[Flat]:
        flats = await asyncio.to_thread(self._search_executor.execute, filters)
        return flats

    def remove_user_data(self, user_id: int) -> None:
        self._flats_repo.remove(telegram_user_id=user_id)
        self._subscribe_repo.remove(telegram_user_id=user_id)
    
    def save_flats(self, flats: list[Flat]) -> None:
        self._flats_repo.save_all(flats)
    
    def save_subscriptions(self, subscription: Subscription) -> None:
        self._subscribe_repo.save(subscription)
        
    def get_all_subscriptions(self) -> list[Subscription]:
        return self._subscribe_repo.get_all()
    
    async def search_new_flats(self, user_id: str) -> None:
        subscribe_model = self._subscribe_repo.get_by_user_id(telegram_user_id=user_id)
        if not subscribe_model:
            raise RuntimeError('Subscription not found')
        filters = build_filters_from_model(subscribe_model)
        new_flats = await self._select_new_flats(filters=filters, user_id=user_id)
        self._flats_repo.save_all(convert_to_model(new_flats, user_id))
        return new_flats

    async def _select_new_flats(self, filters: SearchFilters, user_id: int) -> list[Flat]:
        all_flats = await self.search_by_filters(filters=filters)
        seen_flat = self._flats_repo.get_by_user_id(telegram_user_id=user_id)
        seen_flats_ids = {flat.flat_id for flat in seen_flat}
        return [flat for flat in all_flats if flat.id not in seen_flats_ids]