# Progression Hints

## Summary

Progression Hints is a hint system modification for all currently existing hint systems. The main goal of Progression
Hints is simply defined as "Do Game Content, Get Game Info".

Progress in a world is defined on the tracker as the small icons next to a world's main icon. For instance, when you
first enter a world, a chest icon will appear. If you go into Pride Lands and talk to Simba in the Oasis, the icon
changes to a Simba one. Each of these progress points for each world is given a point value (that you can change), then
every set amount of points information about the seed is revealed.

The cost to reveal the next hint for the seed can also be adjusted per hint, so difficulty to unlock more hints can
scale depending on how you want to play it. For races and those interested in racing with Progression Hints, the order
of hints will be the same for all racers. If players are clearing content at all throughout the game, initially hints
will be given at roughly the same time for each player. The information received from hints is the same, what players do
with that information will be the only difference.

Points can be modified so that certain goals and fights are incentivized to route around as well to gain more info.

Here is a more detailed breakdown of how each current hint system behaves with Progression Hints:

## All Hint Systems

### Report Bonus

For any seed where reports are enabled on the tracker, getting a report in a world will give a Progression Point. This
Report Bonus can be set to 0 to "disable" it.

### Leveling Bonus

Leveling Sora and each Drive Form also gives extra progression points which be can defined in the seed generator as
well.

For Sora, this is defined for every 10 level-ups from 10 to 50 (10, 20, 30, 40, 50).

For Drive Forms, this is defined for each form for every level-up from 2 to 7 (2, 3, 4, 5, 6, 7).

### World Completion Point Bonus

A complicated but fun addition, if you make progress in a world that is already confirmed done/finished, you get an
additional bonus point in addition to what you would normally get.

For example, let's say that TWTNW is complete at the start of a seed and that the World Complete Progression Bonus is
set to "2". If you defeat Roxas, you will get the progression points for defeating Roxas (2 points) AND the World
Complete Progression Bonus (2 points) as well, giving you 4 points total.

These bonuses are also "banked" in all worlds where you don't immediately know if a world is complete or not. For
example, let's say that TWTNW is still hidden/not revealed and you defeat Roxas. You will receive the normal point
amount for defeating Roxas (2 points). If you find out later from a Progression Hint that TWTNW was complete before you
defeated Roxas, then you will recieve the "banked" 2 points immediately.

## Shananas Hints

At the beginning of the seed, all worlds will start off as "?". Every time a hint is revealed with Progression Hints, a
world's current Important Check count is revealed changing the "?" to the current amount.

For example, let's say you go into Twilight Town and find a Fire and a Torn Page. If the first hint you reveal is
"Twilight Town is now unhidden!", the "?" in Twilight Town will become a "2". The tracker does not indicate the world as
complete, meaning Twilight Town still contains more important checks.

Let's say you go into Agrabah and find a Torn Page. If the next hint you reveal is "Agrabah is now unhidden!", the "?"
in Agrabah will become a "1". The tracker does indicate the world as complete, meaning Agrabah contains no more
important checks.

## JSmartee Hints

At the beginning of the seed, all worlds will start off as "?". Every time a hint is revealed with Progression Hints, a
world's Important Check count is revealed changing the "?" to the correct amount.

For example, if the first hint you reveal is "Twilight Town has 3 Important Checks", the "?" in TT will become a "3".

Because logic is no longer tied to where reports belong, the Hinted Hint logic has been removed. This also means
Ansem Reports no longer provide information towards the seed. This can be addressed by either disabling Ansem Reports or
letting Ansem Reports give Progression Points.

## Points Hints

At the beginning of the seed, all worlds will start off as "?". Every time a hint is revealed with Progression Hints, a
world's remaining point total is revealed changing the "?" to the remaining amount.

For example, let's say we're using the Spring League 2022 Points distribution. We go to Twilight Town and find only a
Blizzard. If the first hint you reveal is "Twilight Town is now unhidden!", the "?" in TT becomes a "10", meaning that
there are 10 points of remaining items left.

If you go to Twilight Town later and find a Fire, then the point total will go down to "3".

For this hint system, Ansem Reports will still tell you where a single important check is.

## Path Hints

At the beginning of the seed, all worlds will have their current Important Check counts shown. Every time a hint is
revealed with Progression Hints, a Path Hint is revealed.

For example, let's say you get the last progression point for the next hint by beating Bailey, the hint might say
"Twilight Town is on the path to Peace".

This means Ansem Reports no longer provide information towards the seed. This can be addressed by either disabling
Ansem Reports or letting Ansem Reports give Progression Points.

## Spoiler Hints

At the beginning of the seed, all worlds will start off as "?". Every time a hint is revealed with Progression Hints, a
world's current Important Check count is revealed changing the "?" to the current amount. In addition, all the items in
that world (as designated by the seed generator to be hinted) are revealed as well as ghost checks.

For example, let's say you go into Twilight Town and find a Reflect. If the first hint you reveal is "Twilight Town is
now unhidden!", the "?" in TT will become a "1". Then say a Fire, Final Form, and Proof of Peace are hinted there as
ghost checks.

This means Ansem Reports no longer provide information towards the seed. This can be addressed by either disabling
Ansem Reports or letting Ansem Reports give Progression Points.

### Boss Replacement Hints (to be supported in the future)

This hint system variation only appears when reports in Spoiler Hints are set to "Reveal Boss Replacements".

At the beginning of the seed, all worlds will have their important checks ghost-hinted. Every time a hint is revealed
with Progression Hints, a Boss Replacement hint will be given.

For example, the Progression Hint would say "Thresholder replaced Prison Keeper".

For this variation, the Hint Costs may be static.
