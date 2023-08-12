# JSmartee Hints

## Basics

Once your seed is loaded into the tracker, each location will start with a question mark next to it.

![Empty Tracker](jsmartee_tracker_empty.png)

As you find Ansem Reports in the game, each report will tell you how many
[Important Checks](../../glossary/index.md#important-check) are in a specific location, and a number will replace the
question mark in that location.

![Tracker with Report](jsmartee_tracker_report.png)

## Hint Logic

Hint logic dictates which locations must be hinted based on where proofs are located. The hint logic is
detailed [here](https://jsmartee.github.io/kh2fm-hints-demo/info.html#logic).

### What are "hinted hints"? Why do they matter?

_(Taken from the hint logic page linked above, but also included here for additional emphasis)_

> Reports pointing to proofs will be hinted. As an example:
>
> There's a proof in Port Royal. Report 4 points to Port Royal. Report 4 is in Halloween Town. Halloween Town must be
> hinted by another report. If the priority items above (proofs, forms, pages, and magic) are already taking up all 13
> hints, they will be prioritized over these reports. Note: If the reports are on drive forms or in 100 Acre Wood, there
> is no logic to hint forms or pages as of now.

A "hinted hint" is represented in the tracker by the location's number turning a different color (by default, yellow).

![Tracker with Hinted Hint](jsmartee_tracker_hinted_hint.png)

In the screenshot above, Ansem Report 9 (found in Pride Lands) hints Halloween Town. Halloween Town gets a white
number because Pride Lands has not been hinted (yet). Ansem Report 11 hints Beast's Castle. Because there is already a
hint pointing to Halloween Town (where Ansem Report 11 is located), Ansem Report 11 becomes a "hinted hint" which turns
the number for Beast's Castle the hinted hint color.

Based on this information, it could be inferred that Beast's Castle _may_ have a slightly higher chance of having a
proof than Halloween Town would, since its hint is hinted. _HOWEVER_, being a hinted hint location does not guarantee a
proof. Only once all 13 Ansem Reports are found is it guaranteed that a proof will be in a location pointed to by a
hinted hint.

A general rule of thumb is to not get too caught up in hinted hints early in a seed, unless using them as a tiebreaker
in an otherwise 50/50 decision of where to go next. As you get closer to having all 13 Ansem Reports, the more likely it
becomes that a location pointed to by a hinted hint has a proof.
