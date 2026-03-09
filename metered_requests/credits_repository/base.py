from typing import Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod


class BaseCreditsRepository(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def _get(self, client_id: str) -> Dict[str, Any] | None:
        """
        find a record for client_id in a table `client_credits`
        """
        pass

    @abstractmethod
    def _update(self, client_id: str, new_balance: int, updated_at: datetime) -> None:
        """
        set a new balance for client_id in a table `client_credits`
        """
        pass

    @abstractmethod
    def _insert(self, client_id: str, initial_credits: int, updated_at: datetime) -> None:
        """
        insert initial balance and updated_at for client_id in a table `client_credits`
        """
        pass
