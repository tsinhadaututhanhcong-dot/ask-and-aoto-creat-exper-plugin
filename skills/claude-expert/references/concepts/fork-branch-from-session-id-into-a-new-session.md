---
title: Fork: branch from session_id into a new session
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: sdk
---

# Fork: branch from session_id into a new session
forked_id = None
async for message in query(
    prompt="Instead of JWT, outline how OAuth2 would work for the auth module",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=True,
        max_turns=5,
    ),
):
    if isinstance(message, ResultMessage):
        forked_id = message.session_id  # The fork's ID, distinct from session_id
        if message.subtype == "success":
            print(message.result)

print(f"Forked session: {forked_id}")