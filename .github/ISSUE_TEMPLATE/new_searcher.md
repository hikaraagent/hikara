---
name: new searcher / leader / program label
about: add a known address to the enrichment tables
labels: enrichment
---

**pubkey**

`<base58 pubkey>`

**proposed label**

<!-- short, lowercase, hyphenated. e.g. `jito-router-1`, `pump-arb-2`. -->

**evidence**

<!-- at least three signatures showing this address operating in mev. include
     slot numbers and a one-line description for each. -->

1. `<signature>` slot N — pattern observed
2. `<signature>` slot N — pattern observed
3. `<signature>` slot N — pattern observed

**type**

- [ ] searcher (writes mev-style txs)
- [ ] leader / validator (block producer)
- [ ] program / router / aggregator
