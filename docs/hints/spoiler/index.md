# Spoiler Hints

Spoiler Hints reveal every Important Check in a world by tracking a semi-transparent version of each item to the world.

## Settings

There are some seed generator settings specific to this hint system. 

### Report Reveal Mode

Configures how Ansem Reports reveal information.

#### Disabled

All worlds are revealed at the start.

![Spoiler Hint Example with Reports](spoiler_1.png)

#### Worlds
 
Each Ansem Report reveals the Important Checks in a specific world.

![Spoiler Hint Example with Reports](spoiler_2.png)

In this example, Ansem Report 1 is obtained and displays the text "Port Royal has been revealed!", after which it
displays all the Important Checks Port Royal has.

#### Randomized Bosses

Ansem Reports reveal what a boss has randomized into. Used when playing with randomized bosses only.

For example, consider getting Report 3 in Halloween Town as shown in the image below.

![KHTracker Boss Hint Example](../boss/DA_example.png)

The report reveals the boss replacement "Armor(ed) Xemnas I became Hostile Program". This means that if you walked into
Armored Xemnas I's arena, you would find that Hostile Program would be waiting there for you. Having 13 reports means
that you get 13 boss enemy replacement hints. If you want to see a specific report's hint in DA's tracker, you can hover
over it to reveal its contents.

<img src="https://user-images.githubusercontent.com/58533981/210922963-6b53aeef-fd8b-4266-8a6c-c2eb2068c56b.gif" width="480"/>

<!-- ![DA_animation](https://user-images.githubusercontent.com/58533981/210922963-6b53aeef-fd8b-4266-8a6c-c2eb2068c56b.gif) -->

Another way to get these hints visualized is via the Battleship Tracker. Anytime you find a hint about a boss
replacement, the arena in which you can find the boss will show up in the top right corner. So for example, because
Hostile Program is in Armored Xemnas I's arena, a small Armored Xemnas image appears above Hostile Program.

![Battleship Tracker Boss Hint Example](../boss/roro_example.png)

Note that if some of the bosses are absent from the card, so are their hints, so you may not actually see all 13 hints
on this tracker. If you want to see the hint for a boss not on the card, you can hover over reports in the main tracker
as demonstrated in the gif above.

### Reveal World Completion

If enabled, the tracker will indicate when all Important Checks in a world are found (with default settings, the world's
number will turn blue).

### Spoiled Items

Configures the type(s) of items that can be revealed by spoiler hints.
