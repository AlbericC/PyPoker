# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Cards.py
# Purpose:     provides basic classes for manipulating cards
#
# Author:      Albéric
#
# Created:     2014-08-27
# Copyright:   (c) Albéric 2014
# Licence:     Creative commons CC-BY-SA
#-------------------------------------------------------------------------------

import random


def verbal(some_class):
    """intended as a class decorator allowing to list all attributes and where
    they come from"""

    def tell(inst):
        print(
            "{:>16}: {}\n".format("instance", ", ".join(
                a for a in vars(inst) if not a.startswith("__"))
            ) +
            "".join([
                "{:>16}: {}\n".format(cls.__name__, ", ".join(
                    sorted([a for a in vars(cls) if not a.startswith("__")])
                ))  for cls in type(inst).__mro__
            ]) +
            "{:>16}: {}\n".format(type(type(inst)).__name__, ", ".join(
                a for a in vars(type(type(inst))) if not a.startswith("__"))
            )
        )
    some_class.tell = tell
    return some_class

#-------------------------------------------------------------------------------
# Generic Cards
#-------------------------------------------------------------------------------

@verbal
class CardPack():
    """Class for representing a pack of cards"""

    def __init__(self,numCards=None,cardsList=None):
        if cardsList :
            self.cards = cardsList
        elif numCards == 32:
            self.cards = [ "{}{}".format(carte,couleur)
                    for carte in "789TJQKA"
                    for couleur in "CSHD"]
        else:
            self.cards = [ "{}{}".format(carte,couleur)
                        for carte in "23456789TJQKA"
                        for couleur in "CSHD"]
        self.shuffle()

    def __repr__(self):
        """returns the description of this object
        """
        return "Pack of {} cards".format( len(self.cards) )

    def __str__(self):
        return self.__repr__

    def __call__(self,number):
        return self.take(number)

    # Here we surcharge operations for CardPacks to make it easy to manipulate
    def __rshift__(self, other): # >>
        """Allows alias :
        this >> that  instead of that.put(this)
        (only with cardPacks & subclasses)"""
        if not isinstance( other, type(self) ):
            return NotImplemented
        other.put(self)
    def __rrshift__(self,other): # >> (from the right side)
        """Allows alias :
        this >> that  instead of that.put(this)
        (only with cardPacks & subclasses)"""
        if isinstance( other, type(self) ):
            self.put(other)
        else:
            return NotImplemented

    def shuffle(self):
        """shuffle the pack"""
        random.shuffle( self.cards )

    def take(self,num):
        """pick num cards from this pack"""
        self.cards, out = self.cards[:-num], self.cards[-num:]
        return CardPack(cardsList=out)

    def put(self, pack):
        """put back some cards in the deck"""
        self.cards += pack.cards
        pack._empty() # Empty the other CardPack

    def removeCards(self, pack):
        """remove cards from this pack"""
        for c in pack.cards:
            if c in self.cards:
                self.cards.remove(c)

    def _empty(self):
        self.cards = []

    def show(self,peek=None):
        """Have a look at some cards"""
        if peek :
            return " ".join( sorted( self.cards[-peek] ) )
        else :
            return " ".join( sorted( self.cards ) )

class CardTable():
    def __init__(self, players, cardsPerPlayer,cards=None):
        """Generic Class for a playing cards Table"""
        self.Pack = CardPack(cards)
        self.Pack.shuffle()
        self.packs = [ self.Pack.take(cardsPerPlayer) for p in range(players) ]