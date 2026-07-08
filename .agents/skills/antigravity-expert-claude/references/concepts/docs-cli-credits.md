---
type: Reference
title: CLI Credits
date_created: 2026-07-01
source_url: https://antigravity.google/docs/cli/credits
description: Tracking billing and token quotas.
tags: [concept, llms-txt, js-rendered]
platform: cli
---

* side\_navigation
* Antigravity CLI
>* AI Credits

# Managing AI Credits & Quotas[link](#managing-ai-credits-quotas)

The Antigravity CLI integrates with your subscription to monitor and manage your AI Premium credits and usage quotas.

For a detailed explanation of baseline quotas, how credits are consumed, and plan eligibility, please refer to the main **[Plans](/docs/plans)** page.

## Quota Tracking[link](#quota-tracking)

You can monitor your active quota and credit consumption directly inside the CLI:

* **Statusline Indicator**: The right side of the CLI statusline displays your remaining credit count (e.g., `AI Credits: 42`).
* **Low Quota Alert**: When your remaining AI credits drop below the warning threshold, the statusline indicator highlights to warn you that your limits are near.

## Slash Commands & Managing Balance[link](#slash-commands-managing-balance)

You can query your credits or buy additional quota directly from the CLI:

* **Query Balance**: Type `/credits` in the prompt to open the dedicated credits panel. This panel displays your detailed credit usage statistics.
* **Managing Credits**: You can easily purchase AI credits or upgrade your subscription, which opens a panel containing direct pricing and subscription portal links.

## Settings Configuration[link](#settings-configuration)

To control when and how your AI credits are used, you can toggle credit settings:

* **Use AI Credits Option**: Run `/config` or `/settings` to open the CLI settings panel. Set the **Use G1 Credits** field to **on** to allow the CLI to use your personal credits when plan quotas are exhausted, or set it to **off** to restrict fallback billing. (To learn more, see the **[Plans](/docs/plans#overages)** overages section).

On this Page