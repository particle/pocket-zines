---
name: pocket-zine-story
description: Use first whenever starting or revising a pocket zine (Jerry's 8-page fold-and-cut mini-zines). Covers finding the story, the page-by-page beat sheet, and the storytelling rules. Building and printing are in pocket-zine-build.
---

# pocket zine: the story

pocket zines are hand-drawn, 8-page mini-zines for geeks of all ages. a kid gets the story; an adult gets the wink. each one teaches one idea from software or ai **through a story, never a lecture**. the drawings and layout are the easy part. the story is what makes or breaks a zine, so it comes first and gets agreed before anything is built.

## read the existing zines first

read at least two finished ones page by page before pitching anything. sources are in `sources/*.dc.html`, pdfs in `pdfs/`, live at https://particle.github.io/pocket-zines/. the best models:
- **the little packet**: a journey. a packet wants to see the world, and each stop teaches one idea through a character it meets.
- **the genie in the light switch**: a fable. something good arrives, takes over, goes wrong, and a small hero restores the balance.

## the collections

every zine sits on a named shelf, numbered within it. the cover footer reads `<collection> · no. N`.

| collection | what goes here | so far |
|---|---|---|
| field guides to the digital wild | a naturalist's field guide to a family of things | wild bugs, wild errors |
| true-ish tales of the internet | a protocol or standard told as a character's journey | the little packet, from the very beginning |
| tales of software gone sideways | a classic tale retold as an engineering cautionary tale | frankenstein ships it, the tuesday ghost |
| once upon a model | an old fable retold for the age of ai | genie, golem, mirror, library |

ask which shelf if it isn't obvious. a new collection is fine if nothing fits. field guides don't follow the story shape below; they have their own format (see the end of this file).

## how the work goes

**do not build anything until the story is agreed.** the failure to avoid is a well-drawn sheet with a weak story.

1. **pitch, in chat.** offer 2 or 3 story concepts. for each: the protagonist, what it wants, what goes wrong, how it ends, and any borrowed frame (fable, fairy tale, myth, detective story, classic novel). recommend one. no files.
2. **beat sheet, in chat.** for the chosen concept, write all 8 pages: heading, the 1 to 3 lines of text, and what the drawing shows. jerry reviews it page by page and it takes several rounds. when he flags something, talk it through and agree the fix before changing it. he may take it apart line by line; that's the process working.
3. **then build**, using pocket-zine-build. keep the agreed text exactly.

## the rules

**a protagonist who wants something.** the packet wants to see the world. the golem wants to help. the mirror wants to be liked. a topic ("dates", "time zones") is not a protagonist. give the idea a body, a face and a goal.

**every page is an event, not a fact.** something happens, someone meets someone, something goes wrong. if a page could be a bullet point in documentation, it isn't a story page. the packet learns DNS by asking an owl for directions, and TTL by watching its counter tick down at each router.

**teach through encounters.** each technical idea becomes a character or place the protagonist meets: the DNS owl, the very confident routers, the shark on the undersea cable. one idea per encounter.

**one idea per page.** if a page makes two points, cut one or move it. (genie page 6 got stronger when "the kids had never seen a switch" moved to page 7, where it explains why the cat, not the girl, knows what a switch is.)

**the shape:**
- **cover:** small lead-in ("the"), big title in caps, a subtitle line, a drawing of the protagonist, a tagline ("a fable about asking nicely"), the collection footer
- **p2:** once upon a time. the normal world, the protagonist, what it wants
- **p3 to p5:** the journey or the rise. exciting, then starting to go wrong
- **p6:** the low point or twist. the cost becomes clear
- **p7:** the fix, as a **scene a character acts out**: someone does something and we watch it work. never a bullet list of rules, and never a narrator explaining. (the cat flips the switch; the grandkid adds the zeros.) if the fix has several parts, show the one that matters and let the moral carry the rest.
- **p8 (back):** "the moral" heading, the moral as one big line, one or two plain sentences, a callout box with a question or habit the reader can take away, a parenthetical callback to an earlier joke ("(the baker bought a mop.)"), and the credit line `after <source>, <year> · by jerry gay`. the credit line **always has a year**, even for a legend (use the year of the best-known telling or first publication). with two sources, each gets its year: `after RFC 9110, 2022 & RFC 2324, 1998`.

a tiny glossary on the back is fine only when the story already taught every term in it (the little packet). it never replaces story.

**the logic has to hold.** the events must show exactly what the story claims. "the golem did exactly what you said" broke when the order was "fill the barrel" and it flooded the bakery anyway, because a full barrel is a stopping point. the fix was an open-ended order, "carry water from the river", with nobody saying when to stop. check every cause and effect.

**setups pay off, and nothing appears from nowhere.** if the cat can work the switch on p2, the cat flips the old switch on p7. a specific detail with no reason to be specific raises questions: "tuesday? wednesday?" became "one day … the next day", because no other days mattered.

**whoever resolves the story is set up before they act.** the hero of p7 has to be on the page at least once earlier, even in one line or a corner of a drawing: the cat works the switch on p2 before it saves the day on p7. an apprentice, a girl or a team of librarians who first appear at the moment they fix everything feels like a cheat. the same goes for anyone who sets the plot moving (a king with a decree): give them a line first.

**two levels in every line.** test lines on an imagined 10-year-old and an imagined staff engineer. "screenshots. in comic sans." works for both. "meetings got very short" only works for adults (kids don't go to meetings); "nobody ever had to change their mind again" works for any tween with a group chat.

**the voice.** all lowercase, except real emphasis or a shouted title. short sentences, plain words. small dry asides in parentheses: "(servers are like that.)", "(the cat agrees.)". a few lines per page, never a wall of text. end pages on a punchy line, set in the display font.

**don't reuse motifs across the series.** the genie owns the cat, so the library's copy-of-a-copy got a hand with eleven fingers instead of a seven-legged cat. check the motif register below before pitching, and add the new zine's motifs to it once its beat sheet is agreed.

**every drawing must be drawable and readable at pocket size.** when writing beats, describe pictures that a few hand-drawn lines can carry: one character, one prop, one situation.

## what a weak draft looks like

the first rfc 3339 / iso 8601 attempt failed this way. it was an explainer dressed as a story: no one wanted anything, the pages delivered facts ("add a T, then the hours", "Z means UTC", week dates, durations), the cover character (a calendar with a face) never did anything, and the back page leaned on a glossary.

a stronger version gives something a goal and a journey where ambiguity causes real trouble, with each rule arriving as the answer to a problem it hits. for example: a birthday invitation that has to reach a friend overseas, delivered on the wrong day because "03/04" means different things in different towns, until a tidy clerk rewrites it biggest-part-first.

## motif register

who owns what. a motif belongs to one zine; nobody else uses it, in the text or in a drawing. this covers characters, props, settings and signature phrases.

| zine | owns |
|---|---|
| the genie in the light switch | the cat, the light switch, the king and his decree, the attic tinkerer, smoke, the phrase "very helpful" |
| the golem | the bakery and bread, the baker (and his mop), the flood, clay, the slip of paper, the developer who goes for coffee |
| the mirror | the queen, the castle and its wall, the dragon, thumbs up / thumbs down, the court, the apprentice |
| the library | books and shelves, the printing press, the hand with too many fingers, the cellar, the librarians, the uncle's fishing map |
| the little packet | the DNS owl, the routers, the shark and the undersea cable, the handshake, the TTL countdown |
| from the very beginning | grandma (and grandpa), the birthday, the photo slideshow, the old dog and the puppy |
| frankenstein ships it | the lab, lightning, pitchforks and torches, comic sans, "you ghosted it", "isn't evil" (once, on p6) |
| the tuesday ghost | holmes, watson and lestrade, fog, tea, the ghost, keys that expire "like milk" |
| wild bugs | the moth in the logbook, the rubber duck |
| wild errors | the teapot, the migrating bird, the hairy cryptid and its crossing sign |

the field guides share their format (latin names, habitat, catch difficulty, the sightings checklist); that's the collection's, not a motif.

settled clashes (TODO.md, section 2): the golem no longer says "very helpful" or "wasn't wicked"; frankenstein says "isn't evil" once (p6); the library's girl looks for her uncle's map to the best fishing spot instead of her grandmother's bread recipe (that change lands with the library rebuild in section 6).

## the field-guide format

the field guides to the digital wild aren't fables. there's no protagonist with a goal: the reader is the naturalist, and each page is a sighting. the shape:

- **cover:** "a pocket field guide to", the big title in caps (WILD BUGS), a drawing of one of the creatures inside, a subtitle line ("how to spot, identify & (maybe) catch…"), the collection footer. the cover creature must appear inside.
- **p2:** how to use the guide: what to pack, or how to tell the families apart. one orienting idea, with a drawing.
- **p3 to p6: species pages**, one creature per page. each has its common name as the heading, a mock-latin binomial in italics (`Bugus reliabilis`, `Codus absens`), a drawing of the creature, two or three lines that give it a personality and show its behavior, then `habitat:` (where you meet it in real life) and `catch difficulty:` as stars out of five (★★★☆☆), with an optional dry aside in parentheses. order them so the wildest one lands on p6.
- **p7: field notes**, one true story from history with a real date ("sept 9, 1947…"), told plainly. it's the one page that's fact, not field-guide play, and it should still have an event in it.
- **p8 (back): my sightings.** a checklist of every species with boxes to tick, a blank line for a new one, short asides in parentheses, one practical tip for when you meet one in the wild, a "made with ink & <joke>" line, and the credit line.

the storytelling rules still apply where they can: every species page is an encounter, not a definition; one idea per page; two levels in every line; drawings that read without captions; no reused motifs.
