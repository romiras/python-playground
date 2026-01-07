from typing import Any, ClassVar
import requests
from functools import cmp_to_key
from pydantic import BaseModel, Field, field_validator


class Card(BaseModel):
    code: str = Field(..., description="Card's code")
    image: str = Field(..., description="Card's image")
    value: str = Field(..., description="Card's value")
    suit: str = Field(..., description="Card's suit")

    VALUE_MAPPING: ClassVar[dict] = {
        '10': '0',
        'JACK': 'J',
        'QUEEN': 'Q',
        'KING': 'K',
        'ACE': 'A'
    }
    
    VALID_VALUES: ClassVar[list] = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']

    # Custom validator for additional checks
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if len(v) != 2:
            raise ValueError("Invalid card code")
        return v

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        # Check if we need to map the value
        if v in cls.VALUE_MAPPING:
            v = cls.VALUE_MAPPING[v]
            
        if v not in cls.VALID_VALUES:
            raise ValueError(f"Invalid card value: {v}")
        return v

class DeckManager:
    BASE_API_HOST = "https://www.deckofcardsapi.com"
    CARDS_SUITS_ORDER = [
        "S", # Spades
        "C", # Clubs
        "D", # Diamonds
        "H", # Hearts
    ]
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = []
        self.deck_id = None

    def _api_get(self, url_path: str):
        resp = requests.get(f"{self.BASE_API_HOST}{url_path}", headers={'Accept': 'application/json'})
        if resp.status_code != 200 or resp.headers['Content-Type'] != 'application/json':
            print(resp.status_code)
            print(resp.headers['Content-Type'])
            raise Exception(f"Error: #{resp.content}")
        return resp.json()

    def generate_new_shuffled_deck(self):
        """
        generate a list of cards
        """
        print("Generating a new shuffled deck")
        data = self._api_get("/api/deck/new/")
        self.deck_id = data["deck_id"]
        self._reshuffle_cards()

    def _reshuffle_cards(self):
        print("Reshuffling a deck")
        data = self._api_get(f"/api/deck/{self.deck_id}/shuffle/")
        self.deck_id = data["deck_id"] # we got a new deck id

    def draw_cards(self, count: int):
        """
        draw count cards from a current deck
        """
        print("Draw from a deck")
        data = self._api_get(f"/api/deck/{self.deck_id}/draw/?count={count}")
        self.cards = [Card.model_validate(card) for card in data['cards']]

    def _card_code_to_rank(self, card_item: Card) -> int:
        """
        extract a code and convert to rank
        """
        code = card_item.code
        value = code[0]
        suit = code[1]
        return (len(self.CARDS_SUITS_ORDER) - self.CARDS_SUITS_ORDER.index(suit)) * 16 + \
                self.RANKS.index(value)

    def _compare(self, card_item1, card_item2):
        return self._card_code_to_rank(card_item2) - self._card_code_to_rank(card_item1)

    def _sort_cards(self):
        self.cards = sorted(self.cards, key=cmp_to_key(self._compare))

    def print_cards(self):
        print("Cards:")
        # print cards in one line
        for card_item in self.cards:
            print(f"{card_item.code}", end=" ")
        print()

def main():
    print("--Deck manager--")
    man = DeckManager()
    man.generate_new_shuffled_deck()
    man.draw_cards(15)
    man.print_cards()
    man._sort_cards()
    man.print_cards()

if __name__ == "__main__":
    main()
