# Points Hints

Each Important Check is given a category, and each category is given a value for each item in it. Point values for each
category can be customized when generating a randomizer seed.

Once your seed is loaded into the tracker, each location is given a score based on how many of each of these it
contains. You are able to see the score for each location right from the start.

* As an example, if Pride Lands has a score of 12 that means it can have any combination of Important Checks whose point
  values add up to 12.
* Any location with a zero has no Important Checks (though there still may be useful items/tools there). The tracker
  also indicates the world's completion (with default settings, the world's number turns blue).

![Empty Tracker](points_tracker_empty.png)

As you find Important Checks in the game, the numbers for each location will decrease by the appropriate point values
until eventually reaching zero, at which time the world will be marked as complete.

![Tracker with Items](points_tracker_some_items.png)

In the screenshot above, 2 Important Checks were found in Land of Dragons but there are still one or more Important
Checks there with a combined value of 15 points. Additionally, 3 Important Checks were found on Sora's Levels, and since
the number is now zero and the world is indicated as complete, no more Important Checks are located there.

## Settings

There are some seed generator settings specific to this hint system. 

## Reports Reveal Items

In this hint system, each Ansem Report can give information on the location of a single Important Check. This setting
controls the types of items that can be revealed.

![Tracker with Hint](points_tracker_hint.png)

In the screenshot above, Ansem Report 3 (found in Twilight Town) reveals that Hundred Acre Wood has Wisdom Form.

* The tracker can optionally be configured to show a semi-transparent "ghost item" indicating that an item was hinted in
  a specific location. 
* The tracker can optionally be configured to perform "auto-math" to update the world's score to account for the hinted
  item. When this occurs, the tracker updates the world's number to indicate such (with default settings, the world's
  number turns green).
