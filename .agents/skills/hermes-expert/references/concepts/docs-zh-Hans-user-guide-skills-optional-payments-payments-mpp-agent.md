# Mpp Agent — Pay HTTP 402 APIs via Machine Payments Protocol (MPP) | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/payments/payments-mpp-agent](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/payments/payments-mpp-agent)

本页总览

Pay HTTP 402 APIs via Machine Payments Protocol (MPP).

## Skill metadata[​](#skill-metadata "Skill metadata的直接链接")

|  |  |
| --- | --- |
| Source | Optional — install with `hermes skills install official/payments/mpp-agent` |
| Path | `optional-skills/payments/mpp-agent` |
| Version | `0.1.0` |
| Author | Teknium (teknium1), Hermes Agent |
| License | MIT |
| Platforms | linux, macos |
| Tags | `Payments`, `MPP`, `HTTP-402`, `Tempo`, `Stripe` |
| Related skills | [`stripe-link-cli`](/docs/zh-Hans/docs/user-guide/skills/optional/payments/payments-stripe-link-cli), [`stripe-projects`](/docs/zh-Hans/docs/user-guide/skills/optional/payments/payments-stripe-projects) |

## Reference: full SKILL.md[​](#reference-full-skillmd "Reference: full SKILL.md的直接链接")

信息

The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.

# MPP Agent Skill

Wraps the Machine Payments Protocol (MPP, <https://mpp.dev>) clients so Hermes can pay for per-request API access against servers that respond with `HTTP 402 Payment Required`.

Three client options, all distributed via npm. Pick the lightest one that solves the user's need. Gated `[linux, macos]` while the broader payments tooling matures on Windows.

## When to Use[​](#when-to-use "When to Use的直接链接")

* A merchant API returns `HTTP 402` with a `www-authenticate` header — and the user wants to actually pay it, not just log the response.
* The user asks to "pay per request", "set up an agent wallet", "use Tempo / Privy / AgentCash", or wants to discover MPP-priced services.
* A Stripe Link spend has produced a Shared Payment Token (SPT) and the agent needs to attach it to the 402 challenge — in that flow, prefer `link-cli mpp pay` (see the `stripe-link-cli` skill).

## Choosing a client[​](#choosing-a-client "Choosing a client的直接链接")

| Tool | When | Setup |
| --- | --- | --- |
| `link-cli` | User already has Stripe Link set up, or the 402 challenge advertises `method="stripe"` | see the `stripe-link-cli` skill |
| Tempo Wallet | MPP services with spend controls, service discovery | `tempo wallet login` |
| Privy Agent CLI | Multi-chain wallets, browser-based funding | `privy-agent-wallets login` |
| AgentCash | 300+ pre-priced APIs via one USDC.e balance | `npx agentcash onboard` |
| `mppx` | Dev + debugging, smallest dep surface | `npm install -g mppx` then `mppx account create` |

Default: if the user already has Stripe Link configured or the 402 challenge specifies `method="stripe"`, use `link-cli mpp pay` (the `stripe-link-cli` skill). Otherwise `mppx` for one-off paid calls and debugging, and Tempo Wallet when the user wants persistent spend controls.

## Prerequisites[​](#prerequisites "Prerequisites的直接链接")

* Node.js 20+ on `PATH`
* A funded wallet (Tempo / Privy / AgentCash) OR an `mppx` account
* For Tempo / Privy / AgentCash: follow their respective onboarding skills:
  + `https://tempo.xyz/SKILL.md`
  + `https://agents.privy.io/skill.md`
  + `https://agentcash.dev/skill.md`

Use `web_extract` to fetch any of those SKILL.md files if the user picks one.

## Procedure (mppx, fastest path)[​](#procedure-mppx-fastest-path "Procedure (mppx, fastest path)的直接链接")

Run all commands through the `terminal` tool.

### 1. Install + create an account[​](#1-install--create-an-account "1. Install + create an account的直接链接")

```
npm install -g mppx  
mppx account create
```

Store the resulting account credentials wherever the CLI tells you (the CLI writes them under its own config — do not paste them into the agent transcript).

### 2. Inspect the merchant's 402 challenge[​](#2-inspect-the-merchants-402-challenge "2. Inspect the merchant's 402 challenge的直接链接")

If the user gives you a URL, probe it first to confirm it actually speaks MPP:

```
curl -i <url>
```

A real MPP 402 looks like:

```
HTTP/1.1 402 Payment Required  
www-authenticate: tempo amount=0.1 currency=...
```

### 3. Pay the request[​](#3-pay-the-request "3. Pay the request的直接链接")

```
mppx <url>
```

For non-GET methods or request bodies:

```
mppx <url> --method POST --data '<json>'
```

`mppx` handles the 402 challenge/credential dance automatically and prints the merchant's actual response on success.

### 4. Verify the receipt[​](#4-verify-the-receipt "4. Verify the receipt的直接链接")

`mppx` attaches the receipt header automatically. To inspect:

```
mppx <url> -v
```

## Procedure (Tempo Wallet)[​](#procedure-tempo-wallet "Procedure (Tempo Wallet)的直接链接")

The Tempo Wallet skill at <https://tempo.xyz/SKILL.md> is the canonical reference; fetch it with `web_extract` and follow it. Headline:

```
tempo wallet login  
tempo wallet pay <url>
```

Spend controls and service discovery live in the wallet UI at <https://wallet.tempo.xyz>.

## Pitfalls[​](#pitfalls "Pitfalls的直接链接")

* **`HTTP 402` without `method="stripe"` cannot be paid by Stripe Link.** If the challenge advertises only Tempo / other methods, use `mppx` (or whichever wallet matches) — Link will reject it. Conversely, if it advertises `method="stripe"`, prefer Link via the `stripe-link-cli` skill so the spend goes through the user's approved card.
* **Multiple challenges in one header.** `www-authenticate` may list several methods (e.g. `tempo, stripe`). The Link CLI's `mpp decode` will pick the Stripe one; `mppx` will pick Tempo. There's no single "right" client — pick by which wallet the user has funded.
* **Zero-amount challenges.** Some MPP endpoints charge `$0.00` and just want a proof credential. These work without a funded wallet. Don't refuse them as "broken."
* **Wallet keys never enter agent context.** All four clients store keys under their own config dirs (or generate per-session ephemeral keypairs, in Privy's case). Do not `cat`/`read_file` them.
* **Server-side MPP is a different skill.** If the user wants to ADD 402 to their own API, this skill is wrong — point them at <https://mpp.dev/quickstart/server> and the `mppx/nextjs` / `mppx/hono` / `mppx/express` / `mppx/elysia` middlewares. A dedicated `mpp-server` skill may land later.

## Verification[​](#verification "Verification的直接链接")

```
mppx --version && mppx account list
```

Exit code 0 means installed and an account exists.

* [Skill metadata](#skill-metadata)
* [Reference: full SKILL.md](#reference-full-skillmd)
* [When to Use](#when-to-use)
* [Choosing a client](#choosing-a-client)
* [Prerequisites](#prerequisites)
* [Procedure (mppx, fastest path)](#procedure-mppx-fastest-path)
  + [1. Install + create an account](#1-install--create-an-account)
  + [2. Inspect the merchant's 402 challenge](#2-inspect-the-merchants-402-challenge)
  + [3. Pay the request](#3-pay-the-request)
  + [4. Verify the receipt](#4-verify-the-receipt)
* [Procedure (Tempo Wallet)](#procedure-tempo-wallet)
* [Pitfalls](#pitfalls)
* [Verification](#verification)