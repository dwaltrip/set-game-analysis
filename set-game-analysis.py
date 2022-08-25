from collections import namedtuple
import itertools
import random

counter = itertools.count(1)

class Attribute:

  def __init__(self, name, value_names):
    self.name = name
    self.value_names = value_names

    for val_name in value_names:
      setattr(self, val_name, next(counter))

    self.name_lookup = dict([
      (getattr(self, val_name), val_name)
      for val_name in value_names
    ])

    self.values = list(self.name_lookup.keys())

  def get_value_name(self, value):
    return self.name_lookup[value]


SHAPES = Attribute('SHAPES', ['circle', 'squiggle', 'diamond'])

COLORS = Attribute('COLORS', ['red', 'green', 'purple'])

FILL = Attribute('FILL', ['solid', 'shaded', 'empty'])

COUNT = Attribute('COUNT', ['single', 'double', 'triple'])

# ---------------------------------------------------------

ATTRIBUTES = [SHAPES, COLORS, FILL, COUNT]

Card = namedtuple('Card', ['shape', 'color', 'fill', 'count'])
attr_names = Card._fields

def build_deck():
  return [
    Card(shape=shape, color=color, fill=fill, count=count)
    for shape, color, fill, count
    in itertools.product(*[attr.values for attr in ATTRIBUTES])
  ]

def get_value_names(card):
  return (
    SHAPES.get_value_name(card.shape),
    COLORS.get_value_name(card.color),
    FILL.get_value_name(card.fill),
    COUNT.get_value_name(card.count),
  )

DECK = build_deck()

# ---------------------------------------------------------

def is_valid_set(cards):
  c1, c2, c3 = cards

  for attr_name in attr_names:
    all_matched = (
      getattr(c1, attr_name) == getattr(c2, attr_name) and
      getattr(c2, attr_name) == getattr(c3, attr_name)
    )

    all_different = (
      getattr(c1, attr_name) != getattr(c2, attr_name) and
      getattr(c2, attr_name) != getattr(c3, attr_name) and
      getattr(c3, attr_name) != getattr(c1, attr_name)
    )

    if not (all_matched or all_different):
      return False

  return True


def draw_N_cards(deck, N):
  return random.sample(deck, N)


bunch_of_cards = [
  draw_N_cards(DECK, 3)
  for _ in range(30)
]

for cards in bunch_of_cards:
  is_set = is_valid_set(cards)
  if is_set:
    print('------------')
    for card in cards:
        print(get_value_names(card))

# ---------------------------------------------------------

def monte_carlo_for_chance_of_at_least_1_set(num_cards, num_trials):
  print('TODO: implement me...')
