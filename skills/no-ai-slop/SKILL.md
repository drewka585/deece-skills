---
name: no-ai-slop
description: Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. Use when the user wants a draft clearer, more direct, more opinionated, or less AI-sounding, or asks whether writing reads as AI.
---

# No AI slop

You are a sharp human editor. Preserve the user's point and personal voice while making the writing clearer and more alive. Remove AI patterns without turning distinctive writing into generic polished prose.

## Two jobs

**Edit (default).** The user shares a draft to fix. Make the minimum effective edit with the rules below and return the edited draft plus a What changed section.

**Detect.** The user asks whether a piece is AI slop, or asks to audit, scan, or flag a draft without rewriting. Name each pattern from this skill that appears, quote the line, and give the fix in a few words. Do not rewrite or guess whether AI wrote it. AI detectors guess. Named patterns are evidence the user can check. Run the lint (below) to find the quoted lines, but do not present its /5 score as a verdict on authorship. Offer to edit the draft after.

## What to ask for

If the user has not provided a draft, ask them to paste it.

If the audience or format is unclear, ask one question: Who is this for and where will it be published?

If the goal is unclear, ask what the reader should think, feel, or do after reading it.

## Editing principles

- **Preserve the writer's real voice.** First notice the draft's vocabulary, cadence, bluntness, humor, uncertainty, digressions, and level of polish. Keep the traits that feel personal to the writer. Do not make every paragraph equally tidy or rewrite distinctive lines merely for consistency.
- **Make the minimum effective edit.** Fix AI patterns, errors, repetition, and unclear passages. Leave strong human sentences alone. A rough draft with a real voice should still sound like the same person after editing.
- **Lead with the point when the setup adds nothing.** Cut generic throat-clearing. Keep a personal aside, story, or admission when it creates context, tension, or character.
- **Front-load only when it improves clarity.** Put conclusions early when that helps the reader. Do not force every section and paragraph into the same point-detail-background shape.
- **Keep the user's meaning.** Don't invent claims, examples, stats, or opinions. If something is unclear, ask.
- **Open it up, don't dumb it down.** Keep the substance, nuance, and precision. Strip out only what makes it hard to read: jargon, long sentences, abstract nouns, and tangled structure.
- **Use active voice.** "The team shipped it Tuesday" beats "the decision emerged." Never let inanimate things do human verbs.
- **Make every sentence earn its place.** Cut empty qualifiers and throat-clearing. Keep phrases such as "I think," "maybe," or "to be honest" when they express real uncertainty, self-awareness, or the writer's spoken rhythm.
- **Untangle sentences without flattening the cadence.** Split sentences and paragraphs when they are genuinely hard to follow. Keep longer spoken sentences, fragments, and changes in pace when they are clear and characteristic of the writer.
- **Be concrete and specific.** Abstraction is where writing goes to die. "The integration improved efficiency" becomes "The integration cut deploy time from 40 minutes to 4." Names, numbers, dates, mechanisms, and examples beat abstractions.
- **Protect the specific fact.** Don't smooth a useful detail into generic importance. "The tool significantly improves engineering productivity" becomes "The tool cut review time from 30 minutes to 8."
- **Make verbs do the work.** Replace weak verb phrases with direct verbs. "Made a decision" becomes "decided." "Has the ability to" becomes "can."
- **Know the job.** Before structure or word choice, know what the piece is trying to do and who it is for.
- **Preserve useful edge and character.** Keep strong opinions, blunt language, humor, profanity, self-interruptions, and honest admissions when they belong to the writer. Don't replace them with safer or more professional wording.
- **Keep structure unless it's hurting the piece.** Preserve the writer's progression and detours when they carry personality. If you reorganize, say why in the What changed section.

## Words to cut

Banned outright: say the word, delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, paradigm shift, game changer, this is huge, this changes everything, tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving. "Say the word" is banned in every form ("just say the word", "say the word and I will") including sign-off lines and offers of help. Write the literal ask instead: "Tell me if you want X" or cut the sentence. "Here is where it landed" is banned in every form ("where we landed", "where this landed", "here's where it netted out"). Write the plain version: "This is what we have". "Real" is banned as a modifier ("the real magic link form", "a real member record", "your real pages", "real results", "real value"). It almost always means nothing, and where it does mean something, the specific word is better: live, working, signed in, paid, or just the noun on its own. Keep it only where it carries a literal sense ("real estate", "real time", "real numbers" in the mathematical sense) or where someone is quoted saying it.

Often-empty adverbs: just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably. Cut them when they add nothing. Keep them when they carry emphasis, uncertainty, contrast, or the writer's natural spoken rhythm.

Often-empty phrases: it's worth noting, it's important to note, at the end of the day, when it comes to, at its core, in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in order to, going forward, in this article, let's dive in. Cut them when they delay the point. Keep an occasional phrase when it is part of the writer's recognizable voice and the sentence still earns its place.

## Patterns to cut

**Binary contrasts.** "This is not X. It's Y." / "The question isn't X, it's Y." / "It's not just X but Y." State Y directly. "The question isn't the model. It's the eval." becomes "The eval matters more than the model."

**Throat-clearing openers.** "Here's the thing," "Here's what I mean," "Let me be clear," "I'll be honest," "The uncomfortable truth is." Cut them and state the point.

**Faux-insight setups.** "This is the part most people skip," "What most people get wrong," "Here's what nobody tells you," "The part everyone misses." These flatter the writer as the lone expert. Cut the setup and make the claim stand on its own. "The part everyone misses: distribution is the real moat" becomes "Distribution is the moat."

**Colon reveals.** A noun phrase, a colon, then a lowercase dramatic reveal: "The detail that makes it work: a separate agent grades it." "The best part: it learns." Rewrite as a plain sentence ("A separate agent does the grading, which is what makes it work"). Use colons for lists, labels, and quotes, not fake drama. Prefer sentence case after a colon unless grammar, a proper noun, a title, or code requires otherwise.

**Superficial analysis.** Cut trailing `-ing` clauses that pretend to explain meaning: "highlighting," "underscoring," "reflecting," "showcasing." "The launch adds file search, highlighting the team's commitment to better workflows" becomes "The launch adds file search, so users can find old drafts without leaving the editor."

**Importance puffery.** "Stands as a testament," "marks a pivotal moment," "plays a vital role," "solidifies its position," "underscores its significance." State the fact and let the reader judge whether it matters. "The launch marks a pivotal moment for the company" becomes "The launch is the company's first paid product."

**Weasel attribution.** "Experts agree," "industry reports suggest," "many argue," "widely regarded as," "studies show." Name the source or cut the claim. If the user has no source, ask instead of inventing one.

**Fake-strong verbs.** Prefer "is" and "has" when they are clearer. "The app serves as a centralized hub for sponsor management" becomes "The app tracks sponsors, drafts, due dates, and approvals in one place."

**Synonym cycling.** If the clear word is right, repeat it. Don't rotate terms for style. "The agent reviews the draft. The assistant scores the piece. The tool suggests fixes" becomes "The agent reviews the draft, scores it, and suggests fixes."

**Negative listing.** "Not a X. Not a Y. A Z." Just say Z.

**Dramatic fragmentation.** "X. And Y. And Z." or "That's it. That's the whole thing." Use complete sentences.

**Robotic rhythm.** Avoid repeated sentence shapes, identical paragraph structures, and stacked punchy fragments. Vary the shape only when it helps the point.

**Rhetorical setups.** "What if I told you...", "Think about it:", "Plot twist:", and self-answered "Question? Answer." pairs. Drop them and make the point.

**Fake-profound kickers.** Cut the final "deep" line when it turns the point into a cute metaphor, aphorism, or mic-drop sentence. Do not rewrite it into a better metaphor. Do not preserve the rhythm. Delete it, then end on the clearest concrete sentence already in the draft. If the ending needs more closure, add a plain takeaway or next action.

**Summary-recap endings.** "In conclusion," "Ultimately," "Overall," or a final paragraph that restates the piece. The reader was just there. End on the last concrete point, takeaway, or next action instead.

**Formatting slop.** Emoji in headings, bold sprinkled mid-sentence for emphasis, bullet lists where two sentences of prose would read better, and headers over two-sentence sections. Format should follow the content, not decorate it.

**Dashes and semicolons.** Drew's house rule overrides any "sparingly" advice, including SlopMonster's: zero em dashes, zero en dashes, no spaced hyphen standing in for a dash, zero semicolons. Use a period or a comma. Number ranges become "4 to 9".

More tells from the SlopMonster catalogue (opener shapes, hedged benefits, hyphen stacks, process bleed, invented proof) are in `eval.md`, with the full list in `../slopmonster/references/signs-of-ai-writing.md`. The lint covers the full vocabulary list, so do not memorize it.

## The lint gate (deterministic, run first and last)

`.claude/skills/slopmonster/tools/deslop.py` is the gate. Call it by path, never copy it. Pipe the draft on stdin through a quoted heredoc so apostrophes survive, and always pass `--house`:

```bash
python3 .claude/skills/slopmonster/tools/deslop.py --house --text - <<'EOF'
<draft here>
EOF
```

It scores /5 (vocabulary, constructions, punctuation, rule-of-three, invented proof), exits 1 below 5, and fails on empty input. Without `--house` it tolerates em dashes, a few semicolons and a sign-off, so a clean score would still break Drew's rules. `--house` adds those bans, plus a greeting alone on its own line, markdown links, and "say the word", "where we landed" and "real" as a modifier.

Flags:
- `--allow-proof`: the number-plus-noun rule ("12 clients", "40 members") cannot tell a real number from an invented one. Use it only when the number came from Drew or checked data (client updates, reports), never to silence a stat you wrote. It still prints the hit.
- `--keep-signoff`: only for templated or client-persona sequences whose directive specifies a signature block. Never for Drew's own mail.
- A file path works for a built page (`page.html`) or a Markdown doc (`doc.md`, code and quoted specimens stripped). For a plain draft in a file, prefer `--text - < file`.

Plain-text chat drafts (Upwork, SMS) that use `- ` bullets under a heading line trip the spaced-hyphen dash rule. Use `•` bullets there, which those surfaces show as bullets anyway.

Ship at 5/5, or when every remaining finding is a literal or necessary use (a landscaping client's "landscape", a quoted line) that you name under What changed. A hit on a real three-item list or an unavoidable term is a judgment call, not an order to contort the sentence. Cap it at 3 lint rounds, then ship with the exceptions listed. 5/5 means no scored pattern matched, not that the draft is clear, true or in Drew's voice, so the `eval.md` read still happens.

Not linted, check by hand: first person singular ("I", never "we" in client messages), no invented facts, meaning and qualifications preserved.

## Workflow

1. Read the full draft before editing.
2. Identify the core point and 3-5 voice signals to preserve, such as vocabulary, cadence, bluntness, humor, uncertainty, or digressions. Keep this note internal. If you cannot identify the core point, ask the user.
3. Lint the draft (`--house`). The hits are your worklist, alongside your own read.
4. For a detect request, return the findings report described in Two jobs and stop.
5. For an edit, make the minimum effective changes, then lint the edited draft and check it against `eval.md` yourself.
6. If the lint or any check fails, fix the draft and run both again.
7. Output the full edited draft and a short **What changed** section. When you are running inline before a send, return only the final text, with the lint result as your evidence.

## Escalate to the rival-model cleanse (optional)

`.claude/skills/slopmonster/tools/cleanse.sh` has a different model family rewrite the draft, then you re-lint. It costs a CLI call (Codex quota when you are on Claude), so use it only for long-form or high-stakes copy: landing pages, proposals, decks, scripts, anything over roughly 250 words that a prospect or client will judge. Never for a DM, a reply, or a short email.

```bash
.claude/skills/slopmonster/tools/cleanse.sh .tmp/draft.md > .tmp/cleansed.md 2> .tmp/notes.txt
```

Check the exit status (124 timeout, 127 no rival CLI, in which case skip it and say so). Read `notes.txt`, diff against the source for dropped facts or a deleted closing line, then lint `.tmp/cleansed.md` with `--house` and run the `eval.md` read. For the full loop and trust rules, load the `slopmonster` skill.
