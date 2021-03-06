#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random

SUITS = ["Hearts", "Diamonds", "Clovers", "Spades"]
NUMBERS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
SPECIAL = ['J', 'K', 'Q', 'JOKER']


class Card(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.display_value = value

        if value == 'A':
            self.value = 1
        else:
            self.value = value

        self.modifiers = []

    def add_mod(self, card):
        self.modifiers.append(card)

    def __str__(self):
        res = ""
        val = self.display_value

        if val == 'JOKER':
            return "Joker"

        if val == 'A':
            res += "Ace"
        elif val == 'J':
            res += "Jack"
        elif val == 'K':
            res += "King"
        elif val == 'Q':
            res += "Queen"
        else:
            res += str(val)

        res += " of %s" % self.suit

        return res

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.suit == other.suit and
                    self.display_value == other.display_value)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Deck(object):

    def __init__(self):
        self.stack = []

        for suit in SUITS:
            for number in NUMBERS:
                self.stack.append(Card(suit, number))

            for special in SPECIAL[:-1]:
                self.stack.append(Card(suit, special))

        self.stack.append(Card(None, 'JOKER'))
        self.stack.append(Card(None, 'JOKER'))

    def shuffle(self):
        random.shuffle(self.stack)

    def draw(self):
        return self.stack.pop()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.stack) == len(other.stack):
                for i in xrange(len(self.stack)):
                    if self.stack[i] != other.stack[i]:
                        return False
                return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Player(object):

    def __init__(self, name, deck):
        self.hand = []
        self.deck = deck
        self.name = name
        self.caravans = []

        for _ in range(8):
            self.hand.append(self.deck.draw())

        for _ in range(3):
            self.caravans.append(Caravan())

    def play_card(self, i, j):
        if i >= len(self.hand) or j >= len(self.caravans):
            raise IndexError("Index out of range")
        else:
            card = self.hand[i]
            caravan = self.caravans[j]

            if caravan.can_add(card):
                caravan.add_card(card)
                return True

        return False

    def discard_card(self, i):
        if i >= len(self.hand):
            raise IndexError("Index out of range")
        else:
            del self.hand[i]

    def discard_caravan(self, i):
        if i >= len(self.caravans):
            raise IndexError("Index out of range")
        else:
            self.caravans[i].reset()


class Caravan(object):

    caravans = []

    def __init__(self):
        self.stack = []
        self.order = None
        Caravan.caravans.append(self)

    def add_card(self, card):
        self.stack.append(card)

        if len(self.stack) == 2:
            d = self.stack[0].value - card.value
            if d > 0:
                self.order = 'DESC'
            elif d < 0:
                self.order = 'ASC'
            else:
                raise ValueError("Two cards of same value can't be piled!")

    def can_add(self, card):

        if card.value in SPECIAL:
            return False

        ret_val = False
        if self.order is not None:
            d = self.stack[-1].value - card.value
            if self.order == 'DESC' and d != 0:
                ret_val = True if d > 0 else False
            elif self.order == 'ASC' and d != 0:
                ret_val = True if d < 0 else False
            else:
                ret_val = False
        else:
            ret_val = True

        return ret_val

    def reverse_order(self):
        self.order = 'ASC' if self.order == 'DESC' else 'DESC'

    def get_value(self):
        return sum(card.value for card in self.stack)

    def can_sell(self):
        val = self.get_value()
        return val > 20 and val < 27

    def apply_card(self, card, other_card):
        i = self.stack.index(other_card)
        self.stack[i].add_mod(card)

        val = card.value
        if val == 'J':
            self.stack.remove(other_card)
        elif val == 'K':
            self.stack[i].value *= 2
        elif val == 'Q':
            self.reverse_order()
        else:
            # Joker
            if other_card.display_value == 'A':
                # Remove all cards of the Ace's suit
                for caravan in Caravan.caravans:
                    caravan.stack = filter(lambda x:
                                           (x.suit != other_card.suit or
                                            x == other_card),
                                           caravan.stack)
            else:
                # Remove all cards of the card's value
                for caravan in Caravan.caravans:
                    caravan.stack = filter(lambda x:
                                           (x.display_value != other_card.display_value or
                                            x == other_card),
                                           caravan.stack)

    def reset(self):
        self.stack = []
        self.order = None
