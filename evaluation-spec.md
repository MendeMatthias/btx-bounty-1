# Evaluation specification: BTX Explainer, bounty 1

Version 1, 2026-10-13. The SHA-384 of this file is the terms'
`evaluation_spec_id`. Changing a byte here changes the id, so a revision is a
new file and new terms.

## The deliverable

One open-weight language model, as a single GGUF file of at most
4,000,000,000 bytes, under Apache-2.0 or MIT, that answers questions about
BTX and its model network correctly from the two public sources below. The
submission is the model's `btx://` link (the exact bytes) plus a text file
naming the base model, the licence, and how it was made. Nothing else is
required; training data and code are welcome but not scored.

## The sources

Every question is answerable from these two documents as they stood on
2026-10-13:

1. **The btx repository at tag v0.34.15** (github.com/btxchain/btx):
   `README.md`, `HUMANS.md`, `doc/modelnet/README.md`,
   `doc/modelnet/economics.md`, `doc/bounties.md`, `doc/pay-with-compute.md`,
   and the GitHub release notes of 0.34.12 to 0.34.15.
2. **The BTX Handbook, English second edition** (easybtx.com/handbook; the
   source is `site/handbook/btx-handbook.en.md` in github.com/MendeMatthias/EasyBTX).

Where the two disagree on a number that changed with time (a block height,
a count of miners), the question says which source and date it means.

## The questions

Sixty questions, each with one to four **required facts** (a number, a
name, a height, a yes or no with its reason). An answer passes a question
when every required fact appears in it, case-insensitively, numbers with or
without separators, and no fact in the question's **forbidden** list appears
(forbidden facts catch the usual confusions: Bitcore, a token sale, remote
inference for pay).

- `questions-public.json`: 20 questions, published with the terms, so a
  submitter knows the form.
- The held-out 40: same form, not published until submissions close.
  SHA-384 of the file is in the terms, so the set cannot change afterwards.
  The score counts **all 60**.

## The harness

Evaluators run the model with llama.cpp's `llama-server` (release b11559 or
later), CPU or GPU, these settings and nothing else:

```
temperature 0, top_p 1, max 200 tokens, context 4096, one question per
request, no system prompt, no retrieval, no network, the chat template the
GGUF carries
```

The prompt is the question text alone. The grader is `lab/bounty/grade.py`
in the ainode repository: it asks every question once, applies the rule
above, and writes a report with every answer, so anyone can re-run it and
compare. A model that fails to load, needs more than 16 GB of RAM, or
answers in a language other than English fails.

## The score and the award

- Score = questions passed out of 60. **Passing is 48 or more (80%).**
- Among passing submissions the highest score wins; a tie goes to the
  earlier submission commit (`commitbountysubmission` order).
- If no submission passes by the evaluation close height, nothing is
  awarded and the lot refunds to its contributor after the refund height.
- Evaluators publish their report (`publishbountyevaluation`) with the full
  answer log. The council authorizes the award after `earliest_award_height`
  and before `last_safe_award_height`; the chain enforces the timelock.

## What this bounty does not claim

Passing 48 questions means the model knows these two documents. It does
not mean the model is safe, useful for anything else, or free of mistakes
on questions outside the set. The award is for a model that meets the stated
test, which is what a creation bounty pays for.
