# Source Priority

Use sources in this order:

1. `arXiv`
2. `Crossref`
3. `OpenAlex`
4. `Semantic Scholar`
5. `Google Scholar`

Rules:

- Use `Google Scholar` for recall, especially when the claim is broad or when titles are only partially known.
- Do not accept a `Google Scholar` hit on its own unless the record carries a valid DOI or arXiv identifier that can be checked elsewhere.
- Prefer the metadata version with the strongest identifier coverage:
  - `DOI` beats URL-only metadata.
  - `arXiv ID` beats title-only metadata for preprints.
- If two authoritative sources disagree on title normalization, year, or first author, reject the candidate until the conflict is resolved manually.

