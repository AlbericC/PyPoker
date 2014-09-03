# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose: do stuff...
#
# Author:      Albéric
#
# Created:     2014-08-27
# Copyright:   (c) Albéric 2014
# Licence:     Creative commons CC-BY-SA
#-------------------------------------------------------------------------------

from Cards import CardPack
from Poker import PokerHand, PokerTable

#-------------------------------------------------------------------------------
# Tool for performance analysis
#-------------------------------------------------------------------------------

from time import time


def timed(f):
    #decorator for performance
    def wrapper(*args, **keywords):
        start = time()
        result = f(*args, **keywords)
        elapsed = time() - start
        if elapsed:
            print("\t\t\t{}{} took {b:03.3f} seconds to finish"
                  .format(f.__name__, args, b=elapsed))
        return result
    return wrapper


#-------------------------------------------------------------------------------
# main() : demo code using Poker Values
#-------------------------------------------------------------------------------


# noinspection PyTypeChecker
@timed
def main():
    def max_dict(di: dict):
        maximum = max(di.values())
        for k in di:
            if di[k] == maximum:
                return k

    def sorted_tuples(di):
        out = []
        dictionary = di
        while dictionary:
            best = max_dict(dictionary)
            out.append((best, dictionary[best]))
            dictionary.pop(best)
        return out

    # Face-to-face contests
    print("""
1000 hands will be dealt one after another from the deck, each time only the
winner remains: this is what remains at the end of this face-to-face tournament.
""")
    pack = CardPack()
    # noinspection PyCallByClass
    a, b = PokerHand.fromCardPack(pack), PokerHand.fromCardPack(pack)
    for game in range(1000):
        a, b = min(a, b), max(a, b)
        pack.put(a)
        pack.shuffle()
        a = PokerHand(pack.take(5))
    print(b)

    # Monte Carlo : Who wins in classic Poker ?
    print("""
10 players are dealt random hands from a common deck. After 1000 games, here are
the hands that won the most.
""")
    for player in range(10, 11):
        print("{} players".format(player))
        has_won = dict()
        table = PokerTable(player)
        for donne in range(1000):
            w = table.whatWins()
            if w not in has_won:
                has_won[w] = 1
            else:
                has_won[w] += 1
            table.deal()
        has_won = sorted_tuples(has_won)
        for i in has_won[:10]:
            print("\t {:20} {}".format(i[0], i[1]))

##    # Class mangling - usually a bad idea
##    p = CardPack()
##    a = p.take(5)
##    # A is a CardPack, because CardPack.take returns a CardPack() instance
##    a.__class__ = PokerHand
##    # Changed its nature to be a PokerHand instance instead
##    # in this case, A gained PokerHand class methods in the process
##    a.rank()
##    # This creates A._rank, the memory of the result of A.rank()
##    a.__class__ = CardPack
##    # Back to a basic Card pack instance
##    a >> p
##    # All cards are destroyed
##    a.__class__ = PokerHand
##    # This instance of PokerHand has wrong _rank attribute.


if __name__ == '__main__':
    main()