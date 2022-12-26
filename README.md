# Axis and Allies, battle probability calculator

During the yule holidays 2022, my sons and I were playing Axis and
Allies.  At some point we started wondering about the probabilities of
winning a battle, and in parallell we started implementing each our
algorithm for counting it.  This is my approach.

## Usage

So far it takes "dice powers" as inputs (i.e. one attacking troop
combined with one tank and one bomber airplane is `[1, 0, 1, 1]` -
main.py expects four numbers for the attacker and four numbers for the
defender, so if the units defending is one troop and one fighter -
`[0, 1, 0, 1]`, one can do like this:

    $ python ./main.py 1 0 1 1 0 1 0 1
    98.23% probability for a good outcome

Where a "good outcome" by default means the defending units will be
destroyed, and where it's assumed one will take out the weakest unit
first.  If we neither want to lose the tank nor the bomber, the option
`--max-losses` can be set:

    $ python ./main.py --max-losses=1 1 0 1 1 0 1 0 1
    57.83% probability for a good outcome

Consider another scenario, attacking with five bombers, defending with
one troop, one tank and one fighter, and it's paramount that the tank
is taken out.  We don't want to lose any bombers, and we're happy to
retreat as soon as the tank has been destroyed:

    $ python ./main.py --max-losses=0 --min-hits=2 0 0 0 5 0 1 1 1
    11.51% probability for a good outcome

It seems like one have to accepting to lose one or two bombers in this case:

    $ python ./main.py --max-losses=1 --min-hits=2 0 0 0 5 0 1 1 1
    47.95% probability for a good outcome

    $ python ./main.py --max-losses=2 --min-hits=2 0 0 0 5 0 1 1 1
    88.06% probability for a good outcome

## Possible future plans

### Packaging and renaming the files

I will consider to go through the python packaging process, possibly
move and rename the files a bit, and release this on pypi

### Refinements, documentation, cleanups and refactoring

I'm not much happy about the end result, I had hoped to make code that
was easy to read and understand as well as clean and nice test code,
but I already wasted quite much time on thinking and debugging - I
don't have time refining it further, but I may help answering
questions about the code if someone is interested in taking over.

### Extending the functionality

As said, the code only takes "dice powers" as inputs, but my idea was
to provide the possibility to send a unit list and let the script
handle all special cases (like naval bombardment, submarines having a
first shot unless there are destroyers in the other fleet, anti
aircraft guns, battleships taking one hit "for free", etc), as well as
the possibility to specify in what order units should be removed.
This will require quite much more work though.

Another possibly useful count would be the expected loss of material
(probably counted in "production points" - like, a troop being worth 3
points and a battle ship being worth 20 points) on both sides.

I'm unlikely to ever get time to pursue those plans myself, but if
anyone wants to take over the project I'm happy to hand it over.

## License

Latest GPL applies.

GPL does pose some license compatibility problems.  I haven't given it
much of a thought.  If all contributors agree, it may be dual licensed
(i.e. MIT or Apache).  As long as I'm the sole contributor it will be
easy to argue for a different license.  If you want to contribute and
you do care about licensing, please give me your penny about it.
