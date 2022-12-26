from dices_oo import Outcomes, WinLoseOutcomes, DicePowers, BattleFront, BattleFronts

def testOutcomes():
    single_dice = Outcomes([5,1])
    double_dice = single_dice.combine(single_dice)
    assert double_dice.hits == [25, 10, 1]
    assert double_dice.good() == 11
    assert double_dice.bad() == 25
    assert double_dice.good(min_hits=2) == 1
    assert double_dice.bad(min_hits=2) == 35
    assert double_dice.all() == 36

def testWinLoseOutcomes():
    single_dice = Outcomes([5,1])
    double_dice = single_dice.combine(single_dice)

    single2 = Outcomes([4,2])
    combo = double_dice.combine(single2)

    win_lose_outcomes = WinLoseOutcomes(combo, single2)
    ## TODO ...

def testReduce1():
    battlefront1 = BattleFront([1,0,3,2])
    battlefront2 = BattleFront([0,5,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    some_outcomes = battlefronts.simple_roll()

    some_outcomes.min_hits = 3
    some_outcomes.max_losses = 2
    num_outcomes = some_outcomes.all()
    assert some_outcomes.good() > 0
    assert num_outcomes == some_outcomes.all()
    assert some_outcomes.good() < num_outcomes
    assert some_outcomes.bad() > 0
    assert some_outcomes.bad() < num_outcomes
    assert some_outcomes._wins.hits[0] > 0
    assert some_outcomes._wins.hits[1] > 0
    assert some_outcomes._wins.hits[2] > 0
    assert len(some_outcomes._wins.hits) < 4 or some_outcomes._wins.hits[3] == 0
    assert some_outcomes._losses.hits[0] > 0
    assert some_outcomes._losses.hits[1] > 0
    assert some_outcomes._losses.hits[2] > 0
    assert len(some_outcomes._losses.hits) < 4 or some_outcomes._losses.hits[3] == 0

def testReduce2():
    battlefront1 = BattleFront([1,0,3,2])
    battlefront2 = BattleFront([0,5,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    some_outcomes = battlefronts.simple_roll()
    
    some_outcomes.min_hits = 3
    some_outcomes.max_losses = 6
    num_outcomes = some_outcomes.all()
    assert some_outcomes.good() > 0
    assert some_outcomes.good() < num_outcomes
    assert some_outcomes.bad() == 0
    assert some_outcomes._wins.hits[0] > 0
    assert some_outcomes._wins.hits[1] > 0
    assert some_outcomes._wins.hits[2] > 0
    assert len(some_outcomes._wins.hits) < 4 or some_outcomes._wins.hits[3] == 0

    assert some_outcomes._losses.hits[0] > 0
    assert some_outcomes._losses.hits[1] > 0
    assert some_outcomes._losses.hits[5] > 0
    assert len(some_outcomes._losses.hits) < 8 or some_outcomes._losses.hits[7] == 0
    
def testReduce3():
    battlefront1 = BattleFront([1,0,3,2])
    battlefront2 = BattleFront([0,6,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    some_outcomes = battlefronts.simple_roll()
    
    some_outcomes.min_hits = 3
    some_outcomes.max_losses = 6
    num_outcomes = some_outcomes.all()
    assert some_outcomes.bad() == 0
    assert some_outcomes.good() > 0
    assert some_outcomes.good() < num_outcomes
    assert some_outcomes._wins.hits[0] > 0
    assert some_outcomes._wins.hits[1] > 0
    assert some_outcomes._wins.hits[2] > 0
    assert len(some_outcomes._wins.hits) < 4 or some_outcomes._wins.hits[3] == 0

    assert some_outcomes._losses.hits[0] > 0
    assert some_outcomes._losses.hits[1] > 0
    assert some_outcomes._losses.hits[6] > 0
    assert len(some_outcomes._losses.hits) < 8 or some_outcomes._losses.hits[7] == 0
    
def testReduce4():
    battlefront1 = BattleFront([1,0,3,2])
    battlefront2 = BattleFront([0,6,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    some_outcomes = battlefronts.simple_roll()
    some_outcomes.min_hits = 1
    num_outcomes = some_outcomes.all()
    assert some_outcomes.bad() > 0
    assert some_outcomes.good() > 0
    assert some_outcomes.good() < num_outcomes
    good_bad_ratio = some_outcomes.good() / some_outcomes.bad()
    assert some_outcomes._wins.hits[0] > 0
    assert len(some_outcomes._wins.hits) < 2 or some_outcomes._wins.hits[1] == 0

    assert some_outcomes._losses.hits[0] > 0
    assert some_outcomes._losses.hits[1] > 0
    assert some_outcomes._losses.hits[5] > 0
    assert len(some_outcomes._losses.hits) < 7 or some_outcomes._losses.hits[6] == 0

    battlefronts = BattleFronts(battlefront1, battlefront2)
    some_outcomes = battlefronts.simple_roll()
    some_outcomes.min_hits = 3
    num_outcomes = some_outcomes.all()
    assert some_outcomes.bad() > 0
    assert some_outcomes.good() > 0
    assert some_outcomes.good() < num_outcomes
    assert good_bad_ratio > some_outcomes.good() / some_outcomes.bad()
    assert some_outcomes._wins.hits[0] > 0
    assert some_outcomes._wins.hits[1] > 0
    assert some_outcomes._wins.hits[2] > 0
    assert len(some_outcomes._wins.hits) < 4 or some_outcomes._wins.hits[3] == 0

    assert some_outcomes._losses.hits[0] > 0
    assert some_outcomes._losses.hits[1] > 0
    assert some_outcomes._losses.hits[5] > 0
    assert len(some_outcomes._losses.hits) < 7 or some_outcomes._losses.hits[6] == 0
    
def testMultiRoll0():
    battlefront1 = BattleFront([1,0,0,0])
    battlefront2 = BattleFront([1,0,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    outcomes = battlefronts.multi_roll()
    assert outcomes.good()>0
    assert outcomes.bad()>0
    
def testMultiRoll1():
    battlefront1 = BattleFront([1,0,0,0])
    battlefront2 = BattleFront([2,0,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    outcomes = battlefronts.multi_roll()
    assert outcomes.good()>0
    assert outcomes.bad()>0
    
def testMultiRoll2():
    battlefront1 = BattleFront([2,0,0,0])
    battlefront2 = BattleFront([2,0,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    outcomes = battlefronts.multi_roll()
    assert outcomes.good()>0
    assert outcomes.bad()>0
    
def testMultiRoll3():
    battlefront1 = BattleFront([1,0,3,0])
    battlefront2 = BattleFront([3,1,0,0])
    battlefronts = BattleFronts(battlefront1, battlefront2)
    
    outcomes = battlefronts.multi_roll(min_hits=1, max_losses=1)
    assert outcomes.good()>0
    assert outcomes.bad()>0
    
    outcomes2 = battlefronts.multi_roll(min_hits=2, max_losses=1)
    assert outcomes2.good()>0
    assert outcomes2.bad()>0
    assert outcomes2.good()/outcomes2.bad() < outcomes.good()/outcomes.bad()
    
    outcomes3 = battlefronts.multi_roll(min_hits=3, max_losses=1)
    assert outcomes3.good()>0
    assert outcomes3.bad()>0
    assert outcomes3.good()/outcomes3.bad() < outcomes2.good()/outcomes2.bad()

def testBattleFronts():
    battlefront1 = BattleFront([1,0,3,2])
    battlefront2 = BattleFront([0,5,0,0])
    battlefronts_heavy = BattleFronts(battlefront1, battlefront2)
    foo = battlefronts_heavy.one_roll_statistics()
    assert foo>0
    assert foo<1
    
    battlefront3 = BattleFront([0,0,0,0])
    battlefronts_instawin = BattleFronts(battlefront1, battlefront3)
    foo = battlefronts_instawin.one_roll_statistics()
    assert foo==1
    battlefronts_instaloss = BattleFronts(battlefront3, battlefront2)
    foo = battlefronts_instaloss.one_roll_statistics()
    assert foo==0

    outcomes = battlefronts_heavy.multi_roll()
    pass
