# -*- coding: UTF-8 -*-

# ---------------------------------------------------------------------
# Author:      Atrament
# Copyright:   (c) Atrament 2014
# Licence:     CC-BY-SA https://creativecommons.org/licenses/by-sa/4.0/
# ---------------------------------------------------------------------
from Cards import CardPack, CardTable

__author__ = 'Albéric'

# Here begins the code


class TexasTable(CardTable):

    def __init__(self, n_players,):
        super().__init__(n_players,cardsPerPlayer=2)
        self.n_players = n_players
        self.flop = CardPack(cardsList=[])
        self.river = CardPack(cardsList=[])
        self.turn = CardPack(cardsList=[])
        self.button = 0  # position of the dealer button : player 0 at the beginning
        self.packs = [None] * self.n_players

    def deal(self):
        """deal 2 cards to each player"""
        if len(self.Pack.cards) < 52:
            self.get_all_players_cards()  # retrieve cards from players hands
            self.clean_table()  # retrieve cards on the table (flop and so on)
            self.Pack.shuffle()  # shuffle cards in the pack (all 52 of them)
        # follow the dealer button to deal cards
        for pack in self.packs[self.button:]+self.packs[:self.button]:
            pack = self.Pack.take(2)  # fixme : does this assign ?

    def clean_table(self):
        self.flop >> self.Pack
        self.turn >> self.Pack
        self.river >> self.Pack

    def get_all_players_cards(self):
        """retrieve all players cards"""
        for p in self.packs:
            self.Pack.put(p)


class TexasHand():
    """Specific class for representing a Texas Hold them draw
    that is, seven cards with different statuses :
    handed (2), flop (3), turn (1), river(1)
    this class has to provide methods to detect what is the best possible hand"""
    # TODO : implement and make very very fast (comparison of ten players should be faster than 5ms)

    def from_pack(pck):
        """Pick 2 cards and make them the hand"""
        pass

    def from_cards(cardslist):
        pass

    def __init__(self, table : TexasTable = None):
        self.hand = [None]*2
        self.table = table

def main():
    """
    Do not forget the docstrings !
    """
    pass


if __name__ == "__main__":
    main()
    pass