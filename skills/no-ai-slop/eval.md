# No AI slop eval

Use this after the rewrite. Answer each check with pass or fail. If any check fails, fix the draft before returning it.

For detect requests, make sure the response names each pattern found with a quoted line and a short fix, without rewriting the draft.

## Editing principles

1. Does the edit preserve the user's point without adding claims, examples, stats, quotes, or opinions?
2. Does it preserve the writer's distinctive vocabulary, cadence, bluntness, humor, uncertainty, digressions, and level of polish?
3. Does it leave strong human sentences alone instead of rewriting them for consistency or making every paragraph equally tidy?
4. Is the amount of cutting proportional to the actual slop, with no aggressive compression that strips out character?
5. Does the draft lead with what the reader needs while keeping personal setup that adds context, tension, or character?
6. Are points front-loaded where that improves clarity without forcing every unit into the same structure?
7. Do sentences earn their place, with concrete facts, protected details, and direct verbs where the draft supports them?
8. Does the draft use active voice with human subjects where possible?
9. Does the edit keep useful edge and preserve structure unless the structure was hurting the piece?
10. Are genuinely tangled sentences fixed while clear spoken cadence, fragments, and changes in pace remain intact?

## Words to cut

1. Are banned words, filler phrases, often-empty adverbs, and inflated claims removed unless quoted as examples?

## Patterns to cut

1. Are binary contrasts, negative listings, rhetorical setups, and throat-clearing openers removed?
2. Are faux-insight setups, colon reveals, superficial analysis, fake-strong verbs, synonym cycling, dramatic fragments, and robotic rhythm fixed?
3. Are importance puffery and weasel attribution replaced with plain facts and named sources, or flagged for the user when no source exists?
4. Are fake-profound kicker lines deleted instead of rewritten into better metaphors?
5. Are summary-recap endings cut so the piece ends on a concrete point, takeaway, or next action?
6. Is formatting slop removed: Emoji headings, decorative bold, bullets that should be prose, headers over tiny sections?
7. Are colons sentence case unless grammar, a proper noun, a title, or code requires otherwise?
8. Are there zero em dashes, en dashes, spaced-hyphen dashes, and semicolons? (Drew's house rule. It overrides any "use sparingly" advice, including SlopMonster's.)

## Lint gate (slopmonster/tools/deslop.py)

1. Was the draft linted with `--house` before editing, and the final linted after the last edit?
2. Is the final 5/5, or is every remaining finding a quoted literal or necessary use named under What changed?
3. Is `--allow-proof` used only for numbers Drew supplied or that were checked, never to silence an invented one?
4. Was the final read beyond the score? 5/5 means no scored pattern matched, not that it is clear, true, or in Drew's voice.

## House rules (linted by `--house` unless marked manual)

1. Is the greeting fused to the first sentence on one line, with no sign-off, name, or signature block on Drew's own mail? (Templated and client-persona sequences keep their specified block: `--keep-signoff`.)
2. Is it first person singular in client messages, "I" and never "we"? (Manual.)
3. Are URLs bare, with no markdown link syntax, in plain-text channels?
4. Are "say the word", "where we landed", and "real" as a modifier absent?
5. Where SlopMonster guidance allows something Drew bans (em dashes, a closing summary, a sign-off), did Drew's rule win?

## Tells from SlopMonster

1. Are "whether you're X or Y", "that's where X comes in", "say goodbye to", "imagine a...", "more than just", "look no further", and "ready to get started" removed?
2. Are hedged benefits ("helps you to", "can help you") and stacked hedges ("may potentially") replaced by one verb at the certainty the facts support?
3. Is each three-item list ("faster, smarter, and better") kept only when all three items are real and distinct?
4. Are stacks of four or more hyphenated compounds in one sentence broken up?
5. Are process bleed ("I've analyzed your request and structured the following"), bold-lead bullets on every item, and equal-length paragraphs gone?
6. Is a caveat bolted onto every claim trimmed to the one that matters, with necessary qualifications kept?
7. Does the second sentence of a pair add something instead of relabeling the first, and does the opening answer the reader's first question?
8. Is every customer count, rating, testimonial, or result real and supplied, with `[needs number]` marking gaps instead of guesses?
9. Was each marketing-speak word (delve, tapestry, testament, myriad, plethora, holistic, synergy, unparalleled, bespoke, pivotal, showcase, compelling, intuitive, world-class, journey) replaced by a plainer word and not a synonym?

## Final read

1. Was the edit checked directly against this file without requiring separate editor and evaluator agents?
2. Does the draft avoid robotic symmetry, repeated sentence shapes, and stacked punchy fragments?
3. Would the writer recognize the edited draft as their own voice?
4. Would the edited draft sound natural if read to a sharp colleague?
5. Does the final output include the full edited draft and a short **What changed** section (final text only when running inline before a send)?
6. For detect requests, does the response name each pattern with a quoted line and a short fix, without rewriting or claiming AI authorship, and without presenting the lint score as an AI verdict?
