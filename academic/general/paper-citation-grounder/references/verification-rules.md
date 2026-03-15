# Verification Rules

A citation is eligible for automatic writeback only if all of the following hold:

- Title is present.
- At least one author is present.
- Year is present.
- One of these is true:
  - `DOI` is present
  - `arXiv ID` is present
  - The record is corroborated by at least two authoritative sources with matching normalized title and year

Reject automatically when:

- Title is missing
- Author list is empty
- Year is missing or non-numeric
- Corroborating records disagree on normalized title or year
- The only source is `Google Scholar` with no stable identifier

Optional semantic screening:

- Use abstract overlap as a weak signal, not a proof of support.
- If abstract evidence is too weak for a specific claim, prefer `skip` over `accept`.

Expected output classes:

- `accepted`: safe for placement and possible writeback
- `rejected`: not safe to cite automatically
- `skipped`: insufficient evidence or no match worth surfacing

