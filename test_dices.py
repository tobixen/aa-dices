from dices import combine_outcomes, outcomes

def test_combine_outcomes():
    ## One dice - five possibilities for 0 hits, 1 possibility for 1 hit
    outcomes1 = [5,1]

    ## Two such dices should give ... 1 combination giving two hits,
    ## ten combinations giving 1 hits and 25 combinations giving 0
    ## hits
    two_dice_outcomes = combine_outcomes(outcomes1, outcomes1)
    assert two_dice_outcomes == [25, 10, 1]
    
    ## Three such dices is more complicated ...
    three_dice_outcomes = combine_outcomes(outcomes1, two_dice_outcomes)
    
    ## Sum (total number of outcomes) should be 6**3 = 216
    assert sum(three_dice_outcomes) == 6**3

    ## Number of outcomes with three hits is 1
    assert three_dice_outcomes[3] == 1

    ## More complicated, one dice with two possibilities for hits
    outcomes2 = [4,2]
    two_dice_outcomes = combine_outcomes(outcomes2, outcomes2)
    assert sum(two_dice_outcomes) == 36
    assert two_dice_outcomes[2] == 4

def test_outcomes():
    ## dice powers
    one_soldier = [1,0,0,0]
    one_bomber = [0,0,0,1]
    two_soldiers = [2,0,0,0]
    combination = [1,1,0,0]

    ## one soldier - five possibilities for 0 hits, 1 possibility for 1 hits
    assert outcomes(one_soldier) == [5,1]
    
    ## one bomber - 2 possibilities for 0 hits, 4 possibility for 1 hits
    assert outcomes(one_bomber) == [2,4]
    
    ## two soliders - 36 possibilities
    assert outcomes(two_soldiers) == [25,10,1]

    ## combination
    assert outcomes(combination) == combine_outcomes([5,1], [4,2])
