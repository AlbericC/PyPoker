# -*- coding: UTF-8 -*-

#-------------------------------------------------------------------------------
# Name:        Timer
# Purpose:
#
# Author:      Albéric
#
# Created:     08/04/2014
# Copyright:   (c) AlbÃ©ric 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from time import time

def timed(f):
    #decorator for performance
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        if elapsed:
            print("\t\t\t{}{} took {b:03.2f} ms to finish"\
                   .format(f.__name__,args, b=elapsed*1000)
                   )
        return result
    return wrapper

def main():
    pass

if __name__ == '__main__':
    main()
