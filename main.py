import click
from dices_oo import BattleFront, BattleFronts

@click.command()
@click.option('--min-hits', type=int, default=-1)
@click.option('--max-losses', type=int, default=-1)
@click.argument('attacking_dices', nargs=4, type=int)
@click.argument('defending_dices', nargs=4, type=int)
def main(min_hits, max_losses, attacking_dices, defending_dices):
    attack = BattleFront(attacking_dices)
    defence = BattleFront(defending_dices)
    battle = BattleFronts(attack, defence)
    outcomes = battle.multi_roll(min_hits=min_hits, max_losses=max_losses)

    good_outcomes = outcomes.good()
    tot_outcomes = outcomes.all()
    print(f"{good_outcomes/tot_outcomes*100:5.2f}% probability for a good outcome")

if __name__ == '__main__':
    main()
