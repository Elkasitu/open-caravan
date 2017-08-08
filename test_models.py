#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import unittest
import models


class TestCard(unittest.TestCase):

    def test_card_init(self):
        card = models.Card('Spades', 'A')

        self.assertEqual(card.suit, 'Spades')
        self.assertEqual(card.display_value, 'A')

    def test_card_val_change(self):
        card = models.Card('Hearts', 10)
        card.value += 5

        self.assertEqual(card.display_value, 10)
        self.assertEqual(card.value, 15)

    def test_card_str(self):
        card1 = models.Card('Diamonds', 'A')
        card2 = models.Card('Hearts', 'J')
        card3 = models.Card('Spades', 5)

        self.assertEqual(card1.__str__(), "Ace of Diamonds")
        self.assertEqual(card2.__str__(), "Jack of Hearts")
        self.assertEqual(card3.__str__(), "5 of Spades")

    def test_card_eq(self):
        card1 = models.Card('Diamonds', 'A')
        card2 = models.Card('Diamonds', 'A')

        self.assertEqual(card1, card2)


class TestDeck(unittest.TestCase):

    def test_deck_gen(self):
        deck = models.Deck()

        card_first = models.Card("Hearts", 'A')
        card_last = models.Card(None, 'JOKER')

        self.assertEqual(len(deck.stack), 54)
        self.assertEqual(deck.stack[0], card_first)
        self.assertEqual(deck.stack[-1], card_last)

    def test_deck_shuffle(self):
        deck1 = models.Deck()
        deck2 = models.Deck()

        self.assertEqual(deck1, deck2)

        deck2.shuffle()

        self.assertNotEqual(deck1, deck2)

    def test_deck_draw(self):
        deck = models.Deck()
        card = models.Card(None, 'JOKER')

        self.assertEqual(card, deck.draw())


class TestCaravan(unittest.TestCase):

    def setUp(self):
        self.deck = models.Deck()
        self.caravan = models.Caravan()

    def test_caravan_pool(self):
        l_caravan = models.Caravan()

        self.assertEqual(self.caravan, models.Caravan.caravans[0])
        self.assertEqual(l_caravan, models.Caravan.caravans[1])

    def test_can_add(self):
        card = self.deck.draw()
        card2 = self.deck.stack[0]

        self.assertFalse(self.caravan.can_add(card))
        self.assertTrue(self.caravan.can_add(card2))

    def test_add(self):
        card = self.deck.stack[0]
        self.caravan.add_card(card)

        self.assertEqual(len(self.caravan.stack), 1)

    def test_order_asc(self):
        card1 = self.deck.stack[0]
        card2 = self.deck.stack[1]

        self.caravan.add_card(card1)
        self.caravan.add_card(card2)

        self.assertTrue(self.caravan.order, 'ASC')

    def test_order_desc(self):
        card1 = self.deck.stack[0]
        card2 = self.deck.stack[1]

        self.caravan.add_card(card2)
        self.caravan.add_card(card1)

        self.assertTrue(self.caravan.order, 'DESC')

    def test_reverse_order(self):
        card1 = self.deck.stack[0]
        card2 = self.deck.stack[1]

        self.caravan.add_card(card1)
        self.caravan.add_card(card2)
        self.caravan.reverse_order()

        self.assertTrue(self.caravan.order, 'DESC')

    def test_add_and_can_add(self):
        card1 = self.deck.stack[0]
        card2 = self.deck.stack[1]
        card3 = self.deck.stack[2]
        card4 = self.deck.stack[3]

        self.caravan.add_card(card1)
        self.caravan.add_card(card3)

        self.assertFalse(self.caravan.can_add(card2))
        self.assertFalse(self.caravan.can_add(card3))
        self.assertTrue(self.caravan.can_add(card4))

    def test_bad_add_card(self):
        card = self.deck.stack[0]

        self.caravan.add_card(card)

        with self.assertRaises(ValueError) as context:
            self.caravan.add_card(card)

        self.assertEqual(str(context.exception),
                         "Two cards of same value can't be piled!")

    def test_get_value(self):
        card1 = self.deck.stack[4]
        card2 = self.deck.stack[9]

        self.caravan.add_card(card1)
        self.caravan.add_card(card2)

        self.assertEqual(self.caravan.get_value(), 15)

    def tearDown(self):
        models.Caravan.caravans = []


if __name__ == '__main__':
    unittest.main()
