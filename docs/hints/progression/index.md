# Glossary

* [Summary](#Summary)
* [Shananas Progression Hints](#Shananas-Progression-Hints)
* [JSmartee Progression Hints](#JSmartee-Progression-Hints)
* [Points Progression Hints](#Points-Progression-Hints)
* [Path Progression Hints](#Path-Progression-Hints)
* [Spoiler Progression Hints](#Spoiler-Progression-Hints)
* [Extra Progression Information](#Extra-Progression-Information)

# Progression Hints

## Summary

Progression Hints is a hint system modification for all hint systems. The main goal of Progression Hints is simply defined as "Do Content, Get Hint Info". Progression Hints serves as an alternative to Report-Based hint systems.

You can enable Progression Hints by going to the Hints Tab then clicking on the box:
![Enable Progression Hints](https://github.com/roromaniac/KH2Randomizer/assets/155425660/4c82b2d3-6ed9-49a2-bec3-994cc90018ac)


World Progression is represented on the Tracker by the Icon located to the top-right above a World Icon.
![Prog Example](https://github.com/roromaniac/KH2Randomizer/assets/155425660/58b24cd8-91f9-4390-882e-466b7a16cfd4)

Each world has a predetermined list of World Progression which is typically dictated by updates within the Story. Whenever you reach one of the moments that updates this icon, you will receive between 0-7 Progression Points.
The amount of points given will vary between each kind of Story Progression and this is configurable within the seed generator.


When using Progression Hints, your Important Check Count/Current Points will be replaced with the Progression Points Tracker.
![Current Progression Points](https://github.com/roromaniac/KH2Randomizer/assets/155425660/85ad5d9a-c458-4c40-a479-c4807687b6bc)

The number to the left of the slash indicates how many current Progression Points you have.
The number to the right of the slash indicates how many Progression Points are required to reveal the next Hint(s) (referred to as a Hint Cost or Hint Threshold).
Whenever you reach/exceed the Hint Cost, a Hint will be displayed based upon the Hint System selected. You can read the sections below to see how a Hint Reveal is shown per each current hint system.
The amount of Hints and how much each Hint Cost requires is configurable within the seed generator.

The Hint Order is randomly determined per seed and is consistent per seed. For example, this means that if two people play the same seed but do different starting content, their first hint will be the same regardless of what either player did.


## Shananas Progression Hints

At the beginning of the seed, all worlds will start off as question marks. When you reach the Hint Threshold, the hinted world's Important Check Count will change from a question mark to the current amount.
![Shananas Prog Update](https://github.com/roromaniac/KH2Randomizer/assets/155425660/da315643-7bcb-4787-aead-e31f651c04bd)

After a world is hinted, its Important Check Count will turn from White to Blue when the world's last Important Check is found (like in a non-Progression Shananas Hints seed).

## JSmartee Progression Hints

At the beginning of the seed, all worlds will start off as question marks. When you reach the Hint Threshold, the hinted world's Important Check Count will change from a question mark to the total amount of Important Checks the world has.
![Jsmartee Prog Update](https://github.com/roromaniac/KH2Randomizer/assets/155425660/2af54788-9651-45ad-a7ee-9ae2d922344a)

Because Progression Hints is not Report-Based, JSmartee Progression Hints does not have Hinted Hint logic. It is recommended that you disable Ansem Reports from being Trackable (this can be done in the Hints tab of the seed generator).

## Points Progression Hints

At the beginning of the seed, all worlds will start off as question marks. When you reach the Hint Threshold, the hinted world's Point Total will change from a question mark to the actual Point Total/Remainer the world has.
![Points Prog Update](https://github.com/roromaniac/KH2Randomizer/assets/155425660/68a9fffa-4814-406c-853a-aa75903cb218)

For Points Progression Hints, Reports still retain their secondary function of hinting random Important Checks from worlds.
![Points Prog Report Example](https://github.com/roromaniac/KH2Randomizer/assets/155425660/c71fc48c-d2d2-4a83-8696-7eb6d81e2bc5)

After a world is hinted, its Important Check Count will turn from White/Green to Blue when the world's last Important Check is found (like in a non-Progression Points Hints seed).

## Path Progression Hints

At the beginning of the seed, all worlds will have their current Important Check counts shown. When you reach the Hint Threshold, the hinted world will have its Path Hint revealed.
![Path Prog Update](https://github.com/roromaniac/KH2Randomizer/assets/155425660/5698d108-3571-4d03-971e-b762531e99a0)

After a world is hinted, its Important Check Count will turn from White to Blue when the world's last Important Check is found (like in a non-Progression Path Hints seed).

Because Progression Hints is not Report-Based, it is recommended that you disable Ansem Reports from being Trackable (this can be done in the Hints tab of the seed generator).

For Path Progression Hints specifically, worlds that are initially revealed to have no Important Checks (Blue "0" Worlds) will be hinted last in the Reveal Order.
If there are multiple, they will all be hinted last.

## Spoiler Progression Hints

At the beginning of the seed, all worlds will start off as question marks. When you reach the Hint Threshold, the hinted world's Important Check Count will change from a question mark to the current amount and all Items listed under "Reports Reveal Items" will be revealed.
![Spoiler Prog Update](https://github.com/roromaniac/KH2Randomizer/assets/155425660/6323b5a0-ce92-43b8-826c-d4e813004ac1)

After a world is hinted, its Important Check Count will turn from White/Green to Blue when the world's last Important Check is found (like in a non-Progression Spoiler Hints seed).

When setting up Spoiler Progression Hints, please ensure that you set the Report Reveal Mode to "Reports". The seed will not generate as intended if not done so.

![Report Reveal Mode](https://github.com/roromaniac/KH2Randomizer/assets/155425660/c73cc531-af98-4793-8836-f3a9e5fc1acc)

### Boss Replacement Hints (to be supported in the future)

This hint system variation only appears when reports in Spoiler Hints are set to "Reveal Boss Replacements".

At the beginning of the seed, all worlds will have their important checks ghost-hinted. Every time a hint is revealed
with Progression Hints, a Boss Replacement hint will be given.

For example, the Progression Hint would say "Thresholder replaced Prison Keeper".

For this variation, the Hint Costs may be static.

## Extra Progression Information

Here are some extra options and details related to Progression Hints.

### Auto-Tracking Requirement

Unlike Report-Based hint system which allow you to place items manually on the tracker and place reports for hints,
Progression Hints relies on the Auto-Tracking functionality to update the World Progression and track Progression Points.
Please ensure that you are auto-tracking before playing a seed. If you make progress in a world but are not auto-tracking,
then you will not be able to claim any missed Progression Points.

### Progression World Complete Reward

When you get a Progression Point(s) in a world that is completed (the last important check is found/the world's Important Check Count is Blue), you will gain bonus Progression Point(s) based on the value set.

For example, let's say that TWTNW is complete at the start of a seed and that the World Complete Progression Bonus is set to "2".
If you defeat Roxas, you will get the progression points for defeating him (for example, 3 points) and the Progression World Complete Reward (2 points) as well, giving you 5 points total.

Note: if you were to get 0 points normally from World Progression, you will still gain 0 Progression Points even with the Progression World Complete Reward configured.

These bonuses are "banked" in worlds where you don't immediately know if a world is complete or not.
For example, let's say that the current Hint System is Progression Points Hints and TWTNW is still hidden/not revealed and you defeat Roxas then leave the world immediately after.
You will receive the normal point amount for defeating Roxas (for example, 3 points). If you later reveal from a Progression Hint that TWTNW was complete before you had defeated Roxas,
then you will recieve the "banked" 2 points when TWTNW is hinted by Progression Hints.

### Report Bonus

For any seed where reports are listed as Trackable, obtaining a report will give you a Progression Point(s) based on the set amount. If you do not want Reports to give Progression Points, leave the value as "0".

### Leveling Bonus

For Progression Hints, leveling up Sora and Drives will allow you to gain Progression Points.

For Sora Levels, Progression is set every 10 Levels from level 10 to 50 (Level 10, Level 20, Level 30, Level 40, & Level 50)

For Drive Forms, Progression is set every level-up from drive level 2 to 7 (2, 3, 4, 5, 6, 7).

### Starting With Hints

When setting up the Hint Thresholds/Hint Costs list, if you set the first threshold to 0, upon auto-tracking you will be given the first Progression Hint right away.
If you set multiple 0's, then you will get multiple initial hints.

### Revealing Multiple Hints

When setting up the Hint Thresholds/Hint Costs list, if you set a hint threshold to 0, then that hint will be revealed at the same time as the previous hint.
This allows you you get multiple hints from a single Hint Threshold.
