def combine_outcomes(outcomes1, outcomes2):
    if not outcomes1:
        return outcomes2
    new_outcomes = [0]*(len(outcomes1)+len(outcomes2)-1)
    for i in range(len(outcomes1)):
        for j in range(len(outcomes2)):
            new_outcomes[i+j] += outcomes1[i] * outcomes2[j]
    return new_outcomes

def outcomes(dice_powers):
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


        
        
