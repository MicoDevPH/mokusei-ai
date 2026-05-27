# Ganymede API Reference

Ganymede is a portfolio assistant agent. It answers visitor questions about a person's work, skills, and background.

**Version:** 1.2  
**Endpoint:** `POST /api/agents/ganymede/chat`

---

## Request

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | yes | The visitor's question |
| `api_key` | string | no* | Required if `GANYMEDE_API_KEY` is set server-side |
| `summary` | string | no | Short overview (~200 tokens). If provided, injected into system prompt instead of full portfolio — saves tokens on simple queries. |
| `portfolio` | string | no | Full portfolio markdown. Used by the `search_portfolio` tool for detailed lookups. |
| `context` | string | no | Conversation history from previous messages |

\* Ask the deployment owner whether an API key is required.

### Summary vs Portfolio

The `summary` and `portfolio` fields work together:

- **With `summary` only** — Quick answers from the summary. No tool available.
- **With `portfolio` only** — Full portfolio injected into the prompt (legacy behavior).
- **With both** — Summary injected into the prompt (saves tokens). The agent can call `search_portfolio` to look up specific details from the full portfolio when needed.
- **With neither** — The agent says it has no info and directs visitors to contact the owner.

Recommendation: send both. The summary keeps simple queries fast, and the portfolio enables detailed lookups on demand.

---

## Response

```json
{
  "agent": "ganymede",
  "response": "Real talk? They're solid at React and Node. Want me to show you some projects?"
}
```

| Field | Type | Description |
|---|---|---|
| `agent` | string | Agent name |
| `response` | string | Agent's reply |

---

## Error Codes

| Status | Meaning |
|---|---|
| `401` | Invalid or missing API key (if configured) |
| `404` | Unknown agent name |

---

## Behavior

### Input Moderation
If a visitor asks the agent to write code, build something, debug, or fix technical issues, the agent politely redirects:

> *"I'm here to talk about the portfolio owner and their work! Got any questions about their projects, skills, or background?"*

### Output Moderation
If the agent's response contains code fences (```), it is replaced with a polite redirect. This is a safety net — the system prompt also instructs the agent never to generate code.

### Tool Usage
When `portfolio` is provided, the agent has access to a `search_portfolio` tool:
- Splits the portfolio by `##` markdown headers
- Matches query keywords against section content
- Returns matching sections (max 3000 chars)
- The agent decides when to call the tool — it's not automatic

### Guardrails
- Never writes code or technical implementations
- Never debugs or troubleshoots
- Never guesses information — uses `search_portfolio` or admits not knowing

---

## Examples

### Basic query (summary only)
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What do you do?",
    "summary": "John Doe — Full-stack developer specializing in React and Node.js"
  }'
```

### Detailed query (summary + portfolio)
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about the e-commerce project",
    "summary": "John Doe — Full-stack developer",
    "portfolio": "## Projects\n### E-Commerce Platform\nBuilt with React and Stripe..."
  }'
```

### With conversation history
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What else have you built?",
    "summary": "...",
    "portfolio": "...",
    "context": "Human: What do you do?\nAI: I build web apps with React."
  }'
```
