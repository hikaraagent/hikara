# maintainers

active maintainers and their zones. all pull requests need at least one approval from the relevant zone's maintainer.

## team

| handle           | zone                                          | timezone     |
|------------------|-----------------------------------------------|--------------|
| **hakiriagent**  | core, scoring, ci, docs, release coordination | utc          |
| **0xnova**       | ingest-rs, mempool, builder feeds, traces     | utc+1        |
| **mikrohash**    | classify, heuristics, ai filter               | utc+2        |
| **luka**         | decode, output sinks, cli surface             | utc+1        |

## review policy

- two-review minimum for changes to `src/hakiri/core/`. one must be `@hakiriagent`.
- one review for changes to a single zone, by the zone owner.
- changes that span zones get one review from each affected zone.
- ci must be green on the head commit before merge.

## release coordination

`@hakiriagent` cuts releases. cadence is best-effort, not calendar-driven. each release follows the format used in `CHANGELOG.md` and `docs/release-template.md`.

## becoming a maintainer

three ways in:

1. ship a new detection rule end to end with fixtures and docs
2. own a new chain or dex integration through ci-green
3. write a new output sink that someone else can deploy

after three landed prs in one zone, the zone owner can nominate. consensus among the existing maintainers required.
