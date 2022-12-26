import dices

class Outcomes:
    """
    Class to keep winning outcomes
    """
    def __init__(self, hits=None):
        if isinstance(hits, Outcomes):
            self.hits = hits.hits
        elif hits:
            self.hits = hits
        else:
            self.hits = []

    def combine(self, other):
        ret = Outcomes()
        ret.hits = dices.combine_outcomes(self.hits, other.hits)
        return ret

    def good(self, min_hits=1):
        return sum(self.hits[min_hits:])

    def bad(self, min_hits=1):
        return sum(self.hits[:min_hits])

    def all(self):
        return sum(self.hits)

class WinLoseOutcomes:
    """
    Class to keep winning and losing outcomes
    """
    def __init__(self, wins=None, losses=None, battlefronts=None, min_hits=None, max_losses=None):
        self._wins = Outcomes(wins)
        self._losses = Outcomes(losses)
        self._battlefronts = battlefronts
        self.min_hits = min_hits
        self.max_losses = max_losses
        self.reduced = False
        self._good = 0
        self._bad = 0

    def combine(self, other):
        if not other:
            return self
        ret = WinLoseOutcomes(battlefronts=self._battlefronts)
        ret._bad = self.bad()+other.bad()
        ret._good = self.good()+other.good()
        if self.num_wins_losses() or other.num_wins_losses():
            raise NotImplementedError()
        return ret

    def good(self):
        self.reduce()
        return self._good

    def bad(self):
        self.reduce()
        return self._bad

    def reduce(self):
        """We're usually not caring about the possibilities for
        specific outcomes, we usually want to reduce the data set into
        the possibilities for "good" and "bad" outcomes.  This method
        will aggregate the "good" and "bad" outcomes.
        """
        ## No need to reduce an object more than once
        if self.reduced:
            return

        all = self.all()
        all_d_outcomes = self._losses.all()
        all_a_outcomes = self._wins.all()
        
        ## self.max_losses defaults to "all units" unless specifically given
        if (self.max_losses is None or self.max_losses<0) and self._battlefronts:
            self.max_losses = sum(self._battlefronts.attacker.get_dice_powers())-1
        if (self.min_hits is None or self.min_hits<0) and self._battlefronts:
            self.min_hits = sum(self._battlefronts.defender.get_dice_powers())

        good_hit_outcomes = sum(self._wins.hits[self.min_hits:])
        bad_loss_outcomes = sum(self._losses.hits[self.max_losses+1:])
        remaining_hit_outcomes = sum(self._wins.hits[:self.min_hits])
        remaining_loss_outcomes = sum(self._losses.hits[:self.max_losses+1])
        self._wins.hits = self._wins.hits[:self.min_hits]
        self._losses.hits = self._losses.hits[:self.max_losses+1]
        
        assert remaining_hit_outcomes == sum(self._wins.hits)
        assert remaining_loss_outcomes == sum(self._losses.hits)
        
        assert good_hit_outcomes+remaining_hit_outcomes == all_a_outcomes
        assert bad_loss_outcomes+remaining_loss_outcomes == all_d_outcomes

        self._good += good_hit_outcomes*remaining_loss_outcomes
        self._bad += bad_loss_outcomes*(remaining_hit_outcomes+good_hit_outcomes)

        assert good_hit_outcomes*remaining_loss_outcomes + bad_loss_outcomes*(remaining_hit_outcomes+good_hit_outcomes) + remaining_hit_outcomes*remaining_loss_outcomes == all_d_outcomes*all_a_outcomes
        
        assert all == self.all()

        self.reduced = True
        return self

    def num_wins_losses(self):
        return sum(self._wins.hits[1:]) + sum(self._losses.hits[1:])

    def all(self):
        return self._wins.all()*self._losses.all() + self._bad + self._good

    def next_battlefronts(self):
        self.reduce()
        for i in range(len(self._losses.hits)):
            bf = self._battlefronts.remove_units(role='attack', number=i)
            for j in range(len(self._wins.hits)):
                if i == 0 and j == 0:
                    ## We'll ignore the cases where no units are to be removed.
                    ## (considered to be resolved as an instant reroll)
                    continue
                ret = bf.remove_units(role='defence', number=j)
                ret.units_removed=(i,j)
                ret.num_outcomes = self._losses.hits[i]*self._wins.hits[j]
                if ret.is_win() or ret.is_loss():
                    ## We should not be here.  Those outcomes should have been reduced.
                    assert(False)
                yield ret

class DicePowers:
    """
    In version 0.1 we do not care about the different units and unit
    types, only about "dice powers".
    """
    def __init__(self, dice_powers=None):
        """
        In v0.1, the dice powers should be given as a static list.
        """
        self._dice_powers = dice_powers

    def get_dice_powers(self, role='attack', battlefronts=None):
        """Decide what dices should be rolled and what is needed for a win.

        role and battlefronts ignored as for now - but will be needed
        in more advanced versions, as some special units change
        behaviour dependent on what other units are present in the
        battle, and as future versions will care about what units are
        actually present in the battle.
        """
        return self._dice_powers

    def remove_units(self, number, restrictions=None, remove_order=None):
        """
        Simple logic: just remove the lowest dice powers. Restrictions and remove_order will be needed in the future (i.e. AA-guns can only take out airplanes, one may want to take out fighters prior to the last infantery unit when doing a land battle, etc)
        """
        ret = DicePowers(list(self.get_dice_powers()))
        for i in range(len(ret._dice_powers)):
            removed = min(ret._dice_powers[i], number)
            ret._dice_powers[i] -= removed
            number -= removed
            if not number:
                break
        return ret

    def num_units(self):
        return sum(self.get_dice_powers())

    def roll_outcome(self, role='attack', battlefronts=None):
        ret = Outcomes()
        ret.hits = dices.outcomes(self.get_dice_powers())
        return ret

class BattleFront(DicePowers):
    """
    Class to keep the units of one of the participants.
    """
    ## TODO: let this class contain information on the actual units in the attack
    pass

class BattleFronts:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def remove_units(self, role, *largs, **kwargs):
        if role == 'attack':
            return BattleFronts(attacker = self.attacker.remove_units(*largs, **kwargs), defender = self.defender)
        else:
            return BattleFronts(attacker = self.attacker, defender = self.defender.remove_units(*largs, **kwargs))

    def is_win(self):
        return self.defender.num_units() == 0

    def is_loss(self):
        return self.attacker.num_units() == 0

    def simple_roll(self):
        """
        Rolls the dices for the attacker and defender.

        returns two Outcome objects representing wins and losses
        """
        ret = WinLoseOutcomes(battlefronts=self)
        ret._wins = self.attacker.roll_outcome(role='attack', battlefronts=self)
        ret._losses = self.defender.roll_outcome(role='defence', battlefronts=self)
        return ret

    def one_roll_statistics(self, min_hits=1, max_losses=None):
        """
        Returns the probability for a good roll
        """
        if not sum(self.attacker.get_dice_powers()):
            return 0
        if not sum(self.defender.get_dice_powers()):
            return 1
        outcomes = self.simple_roll()
        outcomes.max_losses = max_losses
        outcomes.min_hits = min_hits
        return outcomes.good() / outcomes.all()

    def multi_roll(self, max_rolls=10, min_hits=1, max_losses=None, multipler=1, divisor=1):
        """Returns the probability for a battle ending good

        max_rolls is to avoid too deep recursion

        min_hits is the minimum numbers of hits acceptable.  When
        min_hits is achieved, it's assumed the attack has succeeded
        and the attacker will retreat.

        max_losses is the maximum loss accepted.  If more than
        max_losses is lost during the battle, the result is considered
        to be bad.

        mutlipler and divisor is used internally when recursing - it's
        the probability that exactly this path is taken when
        recursing.
        """
        outcomes = self.simple_roll()
        outcomes.min_hits = min_hits
        outcomes.max_losses = max_losses
        outcomes.reduce()
        all_outcomes = outcomes.all()
        if max_rolls == 1:
            return outcomes
        if not outcomes.num_wins_losses():
            return outcomes

        ret = None
        tmp_debug = False
        for q in outcomes.next_battlefronts():
            tmp_debug = True
            ur = q.units_removed
            min_hits_ = min_hits-ur[1]
            max_losses_ = outcomes.max_losses-ur[0]
            next_outcomes = q.multi_roll(max_rolls-1, min_hits_, max_losses_, divisor=all_outcomes, multipler=q.num_outcomes)
            assert next_outcomes
            if next_outcomes:
                ret = next_outcomes.combine(ret)

        assert tmp_debug
        assert ret
        if not ret:
            ret = outcomes
        else:
            ret._good += outcomes._good
            ret._bad += outcomes._bad
        ret._good *= multipler
        ret._good /= divisor
        ret._bad *= multipler
        ret._bad /= divisor
        return ret


## TODO: work in progress - diversify unit types, consider all special attacks, etc
class Unit:
    """
    Basic unit - has static attack dice powers and defence dice powers
    """
    def __init__(self, attack, defence, pre_defence=0, pre_attack=0, name='basic unit'):
        self.attack = attack
        self.defence = defence
        self.pre_attack = 0
        self.pre_defence = 0
        self.name = name

    def dice_powers(self, number, battle_fronts=None, role='attack'):
        ret = DicePowers()
        ret.dice_powers = [0]*4
        power = getattr(self, role)
        if power:
            ret.dice_powers[power-1] = number
        return ret
    
