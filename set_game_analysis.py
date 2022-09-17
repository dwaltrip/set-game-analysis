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
  if not len(cards) == 3:
    raise Exception(f'cards should have length 3, got {len(cards)}')
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


def sample_N_cards(deck, N):
  return random.sample(deck, N)

def draw_N_cards(deck, N):
  if len(deck) < N:
    raise ValueError(f'There are less than {N} cards.')
  if N <= 0:
    raise ValueError(f'Invalid number {N} of cards to draw')

  cards = deck[-N:]
  del deck[-N:]
  return cards

def monte_carlo_for_chance_of_at_least_1_set(num_cards, num_trials):
  success_count = 0

  for _ in range(num_trials):
    cards = sample_N_cards(DECK, num_cards)

    for candidate in itertools.combinations(cards, 3):
      if is_valid_set(candidate):
        success_count += 1
        break

  return success_count / num_trials

SET_SIZE = 3

def monte_carlo_for_chance_of_at_least_1_set_V2(hand_size, num_games):
  success_count = 0
  num_trials = 0

  for _ in range(num_games):
    deck = DECK[:]
    random.shuffle(deck)

    current_game_is_done = False
    hand = draw_N_cards(deck, hand_size)

    def remove_from_hand(cards):
      for card in cards:
        hand.remove(card)

    def add_more_cards_if_set_not_found():
      # TODO: Can this ever fail?
      # I think the number of cards remaining in the deck is always a multiple
      # of 3 (SET_SIZE). So it should be fine.
      hand.extend(draw_N_cards(deck, SET_SIZE))

    while not current_game_is_done:
      did_find_set = False

      is_valid_trial = False

      if len(hand) == hand_size:
        is_valid_trial = True
        num_trials += 1

      for candidate_set in itertools.combinations(hand, SET_SIZE):
        if is_valid_set(candidate_set):
          if is_valid_trial:
            success_count += 1
          did_find_set = True
          remove_from_hand(candidate_set)
          break

      if not did_find_set:
        if len(deck) == 0:
          current_game_is_done = True
        else:
          add_more_cards_if_set_not_found()

  print('#### Games:', num_games)
  print('#### Trials:', num_trials)
  print('#### Sucesses:', success_count)
  print('#### Percent:', success_count / num_trials)
  return success_count / num_trials


# ---------------------------------------------------------

if __name__ == '__main__':
  NUM_TRIALS = 10**3


  print('Number of trials:', NUM_TRIALS)
  print('Monte carlo simulation of odds to get at least one set out of N cards')
  print()
  print(f'Num cards  \t|  Probability')
  print(f'-------------------------------')

  # for num_cards in range(3, 13):
  #     chance = monte_carlo_for_chance_of_at_least_1_set(num_cards, NUM_TRIALS)
  #     print(f'{num_cards}\t\t|  {chance:.3f}')

  chance = monte_carlo_for_chance_of_at_least_1_set_V2(12, 100)
  print(f'{chance:.3f}')

  print()

