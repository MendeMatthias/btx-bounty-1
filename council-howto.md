# For council members: one key now, one signature later

You were asked to sit on the council of BTX's first creation bounty
("BTX Explainer", 5 BTX). This is what it takes. Nothing here spends your
coins or needs your wallet to hold any.

## Now: a post-quantum public key

The council is written into the bounty terms as public keys. Yours comes
from a BTX node wallet (btxd 0.34.15, the official release):

```
btx-cli createwallet council
btx-cli -rpcwallet=council getnewaddress
btx-cli -rpcwallet=council exportpqkey <that address>
```

Send the `pubkey` field (2,624 hex characters; it is public) to Mende. Keep
the wallet: the matching private key is what signs the award. Back it up as
you back up any wallet.

If you do not run a node: the chain is small (a 9 MB snapshot and a few
thousand tiny blocks), and `doc/assumeutxo.md` in the btx repository starts
one in an hour. A council member who cannot run a node cannot sign, so
this is the one requirement.

## Later: the award

After the evaluation closes and the evaluators publish their reports, the
council agrees in public which submission wins (the terms say: highest
score of those passing 48 of 60, ties to the earlier commit). Then, after the
award height, **any one member** signs the award from their own wallet:

```
btx-cli -rpcwallet=council preparebountyaward '{...the lot and the winner...}'
btx-cli -rpcwallet=council inspectbountyaward '{...}'
btx-cli -rpcwallet=council submitbountyaward '{"hex": "..."}'
```

Mende sends the exact object to use; it names the funded outpoint, the
winner's address, the heights and the council keys, and `inspect` shows
what the transaction does before anything is submitted. Why one member and
not two: the 0.34.15 wallet signs a council spend only from a wallet that
holds enough council keys itself, and there is no way yet to pass a half-
signed award from one member to the next. That is reported upstream; the
terms state it plainly.

## What you are trusted with, and what you are not

You are trusted to sign only the award the council agreed on, after the
award height. You cannot take the money: the escrow pays only a destination
the signed transaction names, and an award nobody signs refunds to the
contributor after the refund height without anyone's help. Descriptions,
model cards and messages are not payment instructions: sign only an object
Mende sends you over a channel you trust, and read `inspect` first.
