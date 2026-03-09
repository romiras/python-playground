from typing import Dict, Any
from datetime import datetime

from .base import BaseCreditsRepository

class MockCreditsRepository(BaseCreditsRepository):
    credits_vault: Dict[str, Any]

    def __init__(self, db):
        super().__init__(db)
        self.credits_vault = {}

    def _get(self, client_id: str) -> Dict[str, Any] | None:
        # print(f"_get before: {self.credits_vault}")
        return self.credits_vault.get(client_id)

    def _update(self, client_id: str, new_balance: int, updated_at: datetime) -> None:
        # print(f"_update before: {self.credits_vault}")
        self.credits_vault[client_id] = {
            "balance": new_balance,
            "updated_at": updated_at
        }
        # print(f"_update after: {self.credits_vault}")

    def _insert(self, client_id: str, initial_credits: int, updated_at: datetime) -> None:
        # print(f"_insert before: {self.credits_vault}")
        self.credits_vault[client_id] = {
            "balance": initial_credits,
            "updated_at": updated_at
        }
        # print(f"_insert after: {self.credits_vault}")
