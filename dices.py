"""outcomes is a list, with the list index indicating
the number of "wins" (or hits) and the value indicating the number
of possible outcomes with that number of wins.

examples:

[99, 1] - 1% probability for a win
[90, 9, 1] - 90% probability for 0 wins, 1% probability for 2 wins

"dice powers" is a list of how many dices should be thrown, ordered by
the number of winning outcomes.

For instance, in A&A an attack consisting of 6 troop army combined
with one tank and two bomber airplanes gives 6 dice rolls that will be
winning only if a 1 is thrown, one dice roll that will win on the
three lowest counts and two dice rolls that will win if the roll is
within 1,2,3,4.  Hence this attack can be denoted as [6, 0, 1, 2]
"""

def combine_outcomes(outcomes1, outcomes2):
    """
    Take two list of outcomes and combine them

    For instance, outcomes1 and outcomes2 may be the outcomes after
    throwing one and one dice, the return will be all possible
    outcomes after throwing two dices
    """
    if not outcomes1:
        return outcomes2

    if not outcomes2:
        return outcomes1

    new_outcomes = [0]*(len(outcomes1)+len(outcomes2)-1)
    for i in range(len(outcomes1)):
        for j in range(len(outcomes2)):
            new_outcomes[i+j] += outcomes1[i] * outcomes2[j]
    return new_outcomes

def outcomes(dice_powers):
    """
    Yields all the possible outcomes when rolling dice_powers dices
    """
    max_hits = sum(dice_powers)
    hit_outcomes = []
    for i in range(len(dice_powers)):
        if dice_powers[i]:
            local_outcome_first_dice = [6-i-1, i+1]
            hit_outcomes = combine_outcomes(hit_outcomes, local_outcome_first_dice)
            if dice_powers[i]>1:
                local_dice_powers = [0]*4
                local_dice_powers[i] = dice_powers[i]-1
                local_outcome_other_dices = outcomes(local_dice_powers)
                hit_outcomes = combine_outcomes(hit_outcomes, local_outcome_other_dices)
    return hit_outcomes
