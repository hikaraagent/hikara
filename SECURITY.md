# security policy

## scope

hakiri is a read-only forensics tool. it does not sign transactions, hold keys, or move funds. the entire attack surface is:

- the rpc credentials in your `.env` (your responsibility, never read by hakiri except as configured)
- the webhook url you configure (outbound POST, never inbound)
- the local jsonl output file (ordinary file io)

what hakiri does not do:

- never connects to a wallet
- never asks for a private key
- never broadcasts a transaction
- never holds funds of any kind

## reporting a vulnerability

do not open a public github issue.

email the disclosure to: `security@hakiri.xyz`. include:

- a clear description of the issue
- a tx hash or block number reproducing the bug if applicable
- your timeline expectations

initial response within 72 hours. coordinated disclosure preferred. no bounty, but credit in the changelog if you want it.

## what counts as a vulnerability

- code that exfiltrates env vars, .env contents, or rpc credentials
- code that writes outside the configured jsonl path or output dir
- arbitrary code execution via crafted log payloads
- denial of service via mempool flood (we accept this is bounded by the rpc provider)

what does not:

- false positives or false negatives in classification (open a normal issue with evidence)
- requests for paid features
- "you should have caught this private bundle" — hakiri only sees public mempool and post-inclusion data

## supported versions

| version | supported |
|---------|:---------:|
| 0.1.x   |     🟢    |
| < 0.1   |     ⚪    |
