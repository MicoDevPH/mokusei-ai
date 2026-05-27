# Changelog

## Ganymede 1.2 - 2026-05-27

### Added
- `search_portfolio` tool for on-demand portfolio detail lookup
- `summary` field for lightweight context injection (saves tokens on simple queries)
- Input moderation — regex-based off-topic detection with soft redirect
- Output moderation — code fence detection with polite replacement
- `docs/ganymede-api.md` — API reference documentation

### Changed
- Version bumped from 1.0 to 1.2
- System prompt updated with Knowledge Base section (summary + tool model) and Guardrails section
