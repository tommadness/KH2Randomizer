# Hint Systems

The randomizer community has come up with three different hint systems.

* [JSmartee](#jsmartee)
  * [Hint logic](#hint-logic)
* [Shananas](#shananas)
* [Points](#points)

## How do I use hints?

When choosing options for generating a seed, choose which hint system to use on the Hints tab. Once generated, your seed
zip file can be loaded into the [Item Tracker](https://github.com/Dee-Ayy/KH2Tracker) either by dragging the zip file
onto the tracker window, or by choosing `Options > Hint Mode > Load OpenKH Seed` and browsing to the seed zip file.

## JSmartee

In the JSmartee hint system, there are 50 items in the game designated as Important Checks.

* 13 Secret Ansem Reports
* 3 levels of each of the 6 Magic spells (18 total)
* 5 Drive Forms
* Once More
* Second Chance
* 5 Torn Pages
* 4 Summons
* 3 Proofs

If the Promise Charm is enabled for the seed, it is also considered an Important Check, bringing the total to 51.

Once your seed is loaded into the tracker, each location will start with a question mark next to it.

![Empty Tracker](jsmartee/jsmartee_tracker_empty.png)

As you find Secret Ansem Reports in the game, each report will tell you how many Important Checks are in a specific
location, and a number will replace the question mark in that location.

![Tracker with Report](jsmartee/jsmartee_tracker_report.png)

### Hint Logic

Hint logic dictates which locations must be hinted based on where proofs are located. The hint logic is
detailed [here](https://jsmartee.github.io/kh2fm-hints-demo/info.html#logic).

#### What are "hinted hints"? Why do they matter?

_(Taken from the hint logic page linked above, but also included here for additional emphasis)_

> Reports pointing to proofs will be hinted. As an example:
>
> There's a proof in Port Royal. Report 4 points to Port Royal. Report 4 is in Halloween Town. Halloween Town must be hinted by another report.
> If the priority items above (proofs, forms, pages, and magic) are already taking up all 13 hints, they will be prioritized over these reports.
> Note: If the reports are on drive forms or in 100 Acre Wood, there is no logic to hint forms or pages as of now.

A "hinted hint" is represented in the tracker by the location's number turning blue.

![Tracker with Hinted Hint](jsmartee/jsmartee_tracker_hinted_hint.png)

In the screenshot above, Secret Ansem Report 6 (found in Olympus Coliseum) hints Pride Lands. Pride Lands gets a yellow
number because Olympus Coliseum has not been hinted (yet). Secret Ansem Report 13 hints The World That Never Was.
Because there is already a hint pointing to Pride Lands (where Report 13 is located), Report 13 becomes a "hinted hint"
which turns the number for The World That Never Was blue.

Based on this information, it could be inferred that The World That Never Was _may_ have a slightly higher chance of
having a proof than Pride Lands would, since its hint is hinted and its number is blue. _HOWEVER_, being a blue location
does not guarantee a proof. Only once all 13 Secret Ansem Reports are found is it guaranteed that a proof will be in a
location with a blue number.

A general rule of thumb is to not get too caught up in blue numbers early in a seed unless using them as a tiebreaker in
an otherwise 50/50 decision of where to go next. As you get closer to having all 13 Secret Ansem Reports, the more
likely it becomes that a location with a blue number has a proof.

## Shananas

In the Shananas hint system, there are 37 items in the game designated as Important Checks.

* 3 levels of each of the 6 Magic spells (18 total)
* 5 Drive Forms
* Once More
* Second Chance
* 5 Torn Pages
* 4 Summons
* 3 Proofs

If the Promise Charm is enabled for the seed, it is also considered an Important Check, bringing the total to 38.

Once your seed is loaded into the tracker, each location will start with a zero indicating you have not obtained any
Important Checks from any of the locations. Any location with a blue zero means there are no Important Checks there.

![Empty Tracker](shananas/shananas_tracker_empty.png)

As you find Important Checks in the game, the numbers for each location will track the number of Important Checks found
there. Once the number for a location turns blue, all Important Checks there have been found.

![Tracker with Items](shananas/shananas_tracker_some_items.png)

In the screenshot above, 3 Important Checks were found in Olympus Coliseum and the number is now blue, meaning no more
Important Checks are located there (though there still may be useful items/tools there). Additionally, 4 Important
Checks were found in Twilight Town, and since the number is still yellow, Twilight Town must contain at least one more
Important Check.

## Points

In the Points hint system, there are 50 items in the game designated as Important Checks.

* 13 Secret Ansem Reports
* 3 levels of each of the 6 Magic spells (18 total)
* 5 Drive Forms
* Once More
* Second Chance
* 5 Torn Pages
* 4 Summons
* 3 Proofs

If the Promise Charm is enabled for the seed, it is also considered an Important Check, bringing the total to 51.

Each Important Check is given a category, and each category is given a value for each item in it. The default values for
each category are as follows, but the point values can be customized when generating a seed.

* Proofs and Promise Charm = 12 points each
* Drive Forms = 10 points each
* Magic Elements = 8 points each
* Summon Charms = 6 points each
* Second Chance and Once More = 4 points each
* Torn Pages and Ansem Reports = 2 points each

Once your seed is loaded into the tracker, each location is given a Score based on how many of each of these it
contains. You are able to see the Score for each location right from the start.

* Ex. If Agrabah has a Score of 12 that may mean is has a Proof, a Drive Form and a Torn Page (or it could have any
  other combination of Important Checks whose point values add up to 12)
* Any location with a blue zero has no Important Checks (though there still may be useful items/tools there)

![Empty Tracker](points/points_tracker_empty.png)

As you find Important Checks in the game, the numbers for each location will decrease by the appropriate point values
until eventually reaching zero, at which time the number turns blue indicating no more Important Checks are there.

![Tracker with Items](points/points_tracker_some_items.png)

In the screenshot above, 3 Important Checks were found in Land of Dragons but there are still Important Checks there
with a combined value of 10 points. Additionally, a Magnet Element was found in Disney Castle, and since its number is
now a blue zero, no more Important Checks are located there.

### Reports As Hints

In this hint system, each Secret Ansem Report gives information on the location of a single Important Check.

![Tracker with Hint](points/points_tracker_hint.png)

In the screenshot above, Secret Ansem Report 7 (found in Twilight Town) hints that Port Royal has a Torn Page.

### Options

If Proof-hinting reports is turned on, then reports also have a chance of directly telling you which location a proof is
in. Note: Even with this setting on, reports are not _guaranteed_ to hint all or even any Proofs.
