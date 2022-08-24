from itertools import combinations
from random import randint

# ----------------------------------------------------

def roll_N_dice(N):
    return [randint(1,6) for _ in range(N)]

# ----------------------------------------------------

NUM_TRIALS = 10**5
TARGET_SUM = 5
MAX_NUM_DICE = 10

def compute_chance_of_at_least_one_pair_summing_to_target(
    target_sum,
    num_dice,
    num_trials,
):
    success_count = 0

    for _ in range(num_trials):
        dice = roll_N_dice(num_dice)

        for pair in combinations(dice, 2):
            if sum(pair) == target_sum:
                success_count += 1
                break

    return success_count / (num_trials * 1.0)

print(f'Target sum = {TARGET_SUM}. Number of trials = {NUM_TRIALS}.')
print(f'Running monte carlo for up to {MAX_NUM_DICE} dice...')

results = [
    (
        num,
        compute_chance_of_at_least_one_pair_summing_to_target(
            target_sum=TARGET_SUM,
            num_dice=num,
            num_trials=NUM_TRIALS,
        )
    )
    for num in range(2, MAX_NUM_DICE+1)
]

print()
for num_dice, prob in results:
    print(f'{num_dice}\t|  {prob:.3f}')
print()
