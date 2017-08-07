#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

SUITS = ["Hearts", "Diamonds", "Clovers", "Spades"]
NUMBERS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
SPECIAL = ['J', 'K', 'Q', 'JOKER']


class Card(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.display_value = value
        self.value = value
        self.modifiers = []

    def add_mod(self, card):
        self.modifiers.append(card)


class Caravan(object):

    def __init__(self):
        self.stack = []
        self.order = None

    def add_card(self, card):
        self.stack.append(card)

    def can_add(self, card):
        if self.order is not None:
            d = self.stack[-1].value - card.value
            if self.order == 'DESC':
                return True if d > 0 else False
            else:
                return True if d < 0 else False
        else:
            # The stack's not empty
            if len(self.stack > 0):
                d = self.stack[0].value - card.value
                if d == 0:
                    return False
                elif d > 0:
                    self.order = 'DESC'
                    return True
                else:
                    self.order = 'ASC'
                    return True
            else:
                return True

    def reverse_order(self):
        self.order = 'ASC' if self.order == 'DESC' else 'DESC'

    def apply_card(self, card, other_card):
        i = self.stack.index(other_card)
        self.stack[i].add_mod(card)

        val = card.value
        if val in SPECIAL:
            if val == 'J':
                self.stack.remove(other_card)
            elif val == 'K':
                self.stack[i].value *= 2
            elif val == 'Q':
                self.reverse_order()
            else:
                # Joker
                # TODO: Global game object?
                pass
