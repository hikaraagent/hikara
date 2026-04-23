# contributing to hakiri

short version: ship code that passes ci, write a clear pr description, no llm-generated readmes.

## what we want

- new detection rules with on-chain evidence (tx hash + block number) in the pr
- new searcher / builder labels in `src/hakiri/enrich/`
- new dex decoders in `src/hakiri/decode/`
- new output sinks (slack, discord, prometheus, etc.)
- bug fixes with a regression test

## what we do not want

- "powered by ai" rewrites of existing logic
- vendor-specific plugins for paid mev infra (cowswap protect ok, paid bundle apis no)
- new heuristics without numbered evidence
- pull requests that touch unrelated files

## ground rules

1. read-only by design. no wallet, no signer, no trading code lands on main.
2. confidence cap stays at 0.95. anything that lifts it gets reverted.
3. four-author convention. each commit picks one author from the codeowners file. no committing across zones.
4. all heuristics carry an id (SAND-01, BACK-01, ...) referenced in `docs/heuristics.md`.
5. tests are required for new rules. the rule must have one positive fixture and one negative.

## dev loop

```sh
make install       # python package + dev deps
make fmt           # ruff fix + cargo fmt
make lint          # ruff + cargo fmt --check + clippy -D warnings
make test          # pytest + cargo test
```

ci runs the same three. red ci on main does not get advertised.

## opening a pr

- title: `feat(scope): one-line summary` or `fix(scope): one-line summary`
- body: what changed, why, on-chain evidence if applicable, test you wrote
- one logical change per pr. multi-rule prs get split

## reviewers

see [MAINTAINERS.md](MAINTAINERS.md) for the active maintainers and their zones.

a pr touching `src/hakiri/core/` always needs at least one core maintainer review. a pr touching `ingest-rs/` always needs `@0xnova`.

## reporting security issues

do not open a public issue. see [SECURITY.md](SECURITY.md).

## license

by contributing you agree your code is released under the [MIT license](LICENSE).
