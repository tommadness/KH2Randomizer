# JSmartee Hints

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

![Empty Tracker](jsmartee_tracker_empty.png)

As you find Secret Ansem Reports in the game, each report will tell you how many Important Checks are in a specific
location, and a number will replace the question mark in that location.

![Tracker with Report](jsmartee_tracker_report.png)

## Hint Logic

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

![Tracker with Hinted Hint](jsmartee_tracker_hinted_hint.png)

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
