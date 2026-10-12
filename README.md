# BTX creation bounty 1: "BTX Explainer"

The first creation bounty on BTX's model plane, requested by easyBTX
(Mende): **5 BTX** for an open-weight language model (one GGUF of at most
4 GB, Apache-2.0 or MIT) that answers questions about BTX and its model
network correctly from two public sources, the btx repository at tag
v0.34.15 and the BTX Handbook (easybtx.com/handbook).

| File | What |
|---|---|
| `evaluation-spec.md` | the deliverable, the sources, the test, the score, the harness |
| `questions-public.json` | 20 of the 60 questions, with their required facts; the other 40 are held out until submissions close, their SHA-384 is in the terms |
| `grade.py` | the grader: asks a llama.cpp server every question at temperature 0 and checks the facts |
| `make-terms.py` | writes the BountyTerms from the current tip, the council keys and the spec's hash |
| `council-howto.md` | what a council member does: one post-quantum key now, one signature after the award height |

Status, 2026-10-13: the lifecycle (publish, fund into the two-leaf escrow,
award, refund) is rehearsed on regtest with the 0.34.15 release binaries.
The council is being formed; the terms are published when it is. Anyone
may fund a further lot from their own node wallet with their own refund
key (`preparebountyfunding`); an unawarded lot refunds to its contributor
after the refund height.

Baseline: a stock Granite 4.2 3B answers 0 of 60.
