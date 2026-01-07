import requests

class DeckManager:
    BASE_API_HOST = "https://www.deckofcardsapi.com"
    CARDS_SUITS_ORDER = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']

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
        self.cards = data['cards']

    def _card_code_to_rank(code: str) -> int:
        """
        extract a code and convert to rank
        """
        pass

    def _sort_cards():
        sorted_cards = []
        for suit in CARDS_SUITS_ORDER:
            # sort cards by suit
            # then sort cards code
            rank = self.RANKS.index(code)

    def print_cards(self):
        print("Cards:")
        print(self.cards)

def main():
    print("--Deck manager--")
    man = DeckManager()
    man.generate_new_shuffled_deck()
    man.draw_cards(15)
    man.print_cards()

if __name__ == "__main__":
    main()
