from typing import Dict, Any
from datetime import datetime

from .mock import MockCreditsRepository


class CreditsRepository(MockCreditsRepository):
    """
    Responsible for management of clients' credits
    """

    def __init__(self, db, config: Dict[str, Any]):
        super().__init__(db)
        self.config = config

        assert "initial_credits" in self.config
        assert "replenish_credits" in self.config
        assert "max_credits" in self.config

        self.initial_credits = self.config["initial_credits"] # an initial number of credits for clients
        self.replenish_credits = self.config["replenish_credits"] # a number of credits replenished each second after last client's activity
        self.charge_credits = self.config["charge_credits"] # a number credits charged for all clients
        self.max_credits = self.config["max_credits"] # a maximum allowed credits for all clients

        assert self.initial_credits > 0
        assert self.initial_credits <= self.max_credits


    def _get_avail_credits(self, client_id: str, cur_time: datetime) -> tuple[int, datetime]:
        """
        Retrieves the current balance and the last updated timestamp for a client.
        If the client does not exist, it initializes them with initial_credits.
        """
        record = self._get(client_id)
        if record is None:
            self._insert(client_id=client_id, initial_credits=self.initial_credits, updated_at=cur_time)
            return self.initial_credits, cur_time

        return record["balance"], record["updated_at"]


    def _calc_avail_balance(self, client_id: str, cur_time: datetime) -> int:
        """
        Calculates the available balance for a client, including any credits
        replenished since their last activity.
        """
        avail_credits, updated_at = self._get_avail_credits(client_id, cur_time)

        elapsed_seconds = int((cur_time - updated_at).total_seconds()) # a number of whole seconds passed since last client's activity
        replenish = self.replenish_credits * elapsed_seconds
        new_balance = min(avail_credits + replenish, self.max_credits)

        assert new_balance >= 0

        return new_balance


    def charge(self, client_id: str) -> bool:
        """
        Attempts to deduct credits from a client's balance for a request.
        Returns True if the operation was successful, False if there are insufficient credits.
        """
        cur_time = datetime.now() # TODO: make sure we obtain a timestamp as soon as possible, before any I/O or calculations !!!
        avail_balance = self._calc_avail_balance(client_id, cur_time)
        if avail_balance < self.charge_credits:
            return False

        new_balance = avail_balance - self.charge_credits
        self._update(client_id=client_id, new_balance=new_balance, updated_at=cur_time)
        return True
