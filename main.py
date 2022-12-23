import click
from dices import outcomes

@click.command()
@click.argument('dices', nargs=-1, type=int)
def main(dices):
    my_outcomes = outcomes(dices)
    tot_outcomes = sum(my_outcomes)
    print([x/tot_outcomes for x in my_outcomes])

if __name__ == '__main__':
    main()
