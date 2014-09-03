# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        Poker.py
# Purpose:     defines basic classes for modelling poker
#
# Author:      Albéric
#
# Created:     2014-08-27
# Copyright:   (c) Albéric 2014
# Licence:     Creative commons CC-BY-SA
#-------------------------------------------------------------------------------

from Cards import CardPack, CardTable

class PokerHand(CardPack):
    """Specific subclass for Poker Hands (5 cards)
    High Card: Highest value card.
    One Pair: Two cards of the same value.
    Two Pairs: Two different pairs.
    Three of a Kind: Three cards of the same value.
    Straight: All cards are consecutive values.
    Flush: All cards of the same suit.
    Full House: Three of a kind and a pair.
    Four of a Kind: Four cards of the same value.
    Straight Flush: All cards are consecutive values of same suit.
    Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
    """

    def fromCardPack(pack):
        """Pick 5 cards in the pack and create a PokerHand"""
        return PokerHand(pack.take(5))

    def fromCards(cardslist):
        """Make a PokerHand from the given cards"""
        return PokerHand(CardPack(cardsList = cardslist))

    def __init__( self, pack : CardPack ):
        super().__init__()
        self.cards = pack.cards
        self.rank()

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        """returns representation of self
            """
        qualifiers = ['High Card',
                      'One Pair',
                      'Two Pairs',
                      'Three of a Kind',
                      'Straight',
                      'Flush',
                      'Full House',
                      'Four of a Kind',
                      'Straight Flush',
                      'Royal Flush']
        return "PokerHand : {} - {}".format(
            " ".join(sorted(self.cards)),
            qualifiers[self._rank[0]]
        )

    def __getattr__( self, name ):
        if name == '_rank':
            return self.rank()
        else:
            raise AttributeError("Attribute {} does not compute".format(name))

    def put(self,other):
        super().put(other)
        # content has changed, rank is obsolete
        del self._rank

    def __gt__( self, other ):
        me = self._rank
        him = other._rank
        for soup in range( min(len(me), len(him) ) ):
            if me[soup] != him[soup]:
                return me > him

    def whathand(self):
        return [ 'High Card',
                 'One Pair',
                 'Two Pairs',
                 'Three of a Kind',
                 'Straight',
                 'Flush',
                 'Full House',
                 'Four of a Kind',
                 'Straight Flush',
                 'Royal Flush'][ self._rank[0] ]

    def _empty(self):
        super()._empty()
        del self._rank

    def rank(self):
        """Should return a list composed of
        -the index of the type of hand (high card == 0, Royal Flush == 9)
        -the values of the cards, sorted by numer of identical cards
                then by value (inverse)"""
        scoreList = []
        SuitsDic = { A[1]:sorted([ C[0]
                                for C in self.cards if C[1]==A[1]
                                ]
                               )
                    for A in self.cards }
        ValueDic = { C[0]:sorted(
                                B[1] for B in self.cards if B[0]==C[0]
                                )
                    for C in self.cards
                    }
        # BEGIN TESTS
        if len(self.cards) != 5:
            scoreList = [0]
        elif sorted(self.cards) in list( sorted( [ "{}{}".format(carte,couleur)
                                        for carte in "TJQKA" ]
                                        )
                              for couleur in "CHSD"
                              ):
            scoreList.append(9) #Royal Flush !
        elif any([ sorted("23456789TJQKA"[i:i+5]) in SuitsDic.values()
                 for i in range(13-5)]
                ):
            scoreList.append(8) # Straight Flush
        elif 4 in { len(A) for A in ValueDic.values() }:
            scoreList.append(7) # four of a kind
        elif { len(A) for A in ValueDic.values() } == {3,2} :
            scoreList.append(6) # Full House
        elif len( { A[1] for A in self.cards } ) == 1:
            scoreList.append(5) # Flush
        elif any([ sorted("23456789TJQKA"[i:i+5]) in list(ValueDic.keys())
                for i in range(13-5)]
                ):
            scoreList.append(4) # Straight
        elif 3 in { len(A) for A in ValueDic.values() }:
            scoreList.append(3) # Brelan !
        elif len( ValueDic ) == 3 :
            scoreList.append(2) # Two Pairs
        elif 2 in { len(A) for A in ValueDic.values() }:
            scoreList.append(1) # one Pair
        else :
            scoreList.append(0) # High Card, sucker !
        # END TYPE OF HAND TESTS
        PokerCardValue = lambda Card : "23456789TJQKA".index(Card)
        cardsnum = { PokerCardValue(c):len(ValueDic[c]) for c in ValueDic}
        for num_cards in range (4,0,-1):
            templist = []
            for i in cardsnum:
                if cardsnum[i] == num_cards:
                    templist.append(i)
            scoreList += sorted(templist,reverse=True)
        self._rank = scoreList
        return scoreList



class PokerTable(CardTable):
    def __init__(self, players):
        super().__init__(players, 5)
        self.n_players = players
        self.Pack = CardPack(52)
        self.Pack.shuffle()
        self.deal()

    def getAll(self):
        """retrieve all players cards"""
        for p in self.players:
            self.Pack.put(p)

    def deal(self):
        """deal 5 (five) cards per player (Poker, dude!)"""
        if len( self.Pack.cards ) < 52:
            self.getAll()
        self.Pack.shuffle()
        self.players = list( map( PokerHand.fromCardPack ,
                                  self.n_players*[self.Pack]
                                  ) )

    def whatWins(self):
        """returns the type of hand that wins now"""
        winner = max(self.players)
        descript = winner.rank() # funky format list
        qualifs = ['High Card',
        'One Pair',
        'Two Pairs',
        'Three of a Kind',
        'Straight',
        'Flush',
        'Full House',
        'Four of a Kind',
        'Straight Flush',
        'Royal Flush']
        cards = "23456789TJQKA"
        return "{} - {}".format( qualifs[descript[0]], cards[descript[1]] )