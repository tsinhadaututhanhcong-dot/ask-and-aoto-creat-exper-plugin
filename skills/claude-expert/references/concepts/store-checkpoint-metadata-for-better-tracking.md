---
title: Store checkpoint metadata for better tracking
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Store checkpoint metadata for better tracking
@dataclass
class Checkpoint:
    id: str
    description: str
    timestamp: datetime


async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    checkpoints = []
    session_id = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        async for message in client.receive_response():
            if isinstance(message, UserMessage) and message.uuid:
                checkpoints.append(
                    Checkpoint(
                        id=message.uuid,
                        description=f"After turn {len(checkpoints) + 1}",
                        timestamp=datetime.now(),
                    )
                )
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    # Later: rewind to any checkpoint by resuming the session
    if checkpoints and session_id:
        target = checkpoints[0]  # Pick any checkpoint
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")  # Empty prompt to open the connection
            async for message in client.receive_response():
                await client.rewind_files(target.id)
                break
        print(f"Rewound to: {target.description}")


asyncio.run(main())
```

## [​](#try-it-out) Try it out

This complete example creates a small utility file, has the agent add documentation comments, shows you the changes, then asks if you want to rewind.
Before you begin, make sure you have the [Claude Agent SDK installed](/docs/en/agent-sdk/quickstart).

1

Create a test file

Create a new file called `utils.py` (Python) or `utils.ts` (TypeScript) and paste the following code:

utils.py

utils.ts

```
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

2

Run the interactive example

Create a new file called `try_checkpointing.py` (Python) or `try_checkpointing.ts` (TypeScript) in the same directory as your utility file, and paste the following code.This script asks Claude to add doc comments to your utility file, then gives you the option to rewind and restore the original.

try\_checkpointing.py

try\_checkpointing.ts

```
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


async def main():
    # Configure the SDK with checkpointing enabled
    # - enable_file_checkpointing: Track file changes for rewinding
    # - permission_mode: Auto-accept file edits without prompting
    # - extra_args: Required to receive user message UUIDs in the stream
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    checkpoint_id = None  # Store the user message UUID for rewinding
    session_id = None  # Store the session ID for resuming

    print("Running agent to add doc comments to utils.py...\n")

    # Run the agent and capture checkpoint data from the response stream
    async with ClaudeSDKClient(options) as client:
        await client.query("Add doc comments to utils.py")

        async for message in client.receive_response():
            # Capture the first user message UUID - this is our restore point
            if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
                checkpoint_id = message.uuid
            # Capture the session ID so we can resume later
            if isinstance(message, ResultMessage):
                session_id = message.session_id

    print("Done! Open utils.py to see the added doc comments.\n")

    # Ask the user if they want to rewind the changes
    if checkpoint_id and session_id:
        response = input("Rewind to remove the doc comments? (y/n): ")

        if response.lower() == "y":
            # Resume the session with an empty prompt, then rewind
            async with ClaudeSDKClient(
                ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
            ) as client:
                await client.query("")  # Empty prompt opens the connection
                async for message in client.receive_response():
                    await client.rewind_files(checkpoint_id)  # Restore files
                    break

            print(
                "\n✓ File restored! Open utils.py to verify the doc comments are gone."
            )
        else:
            print("\nKept the modified file.")


asyncio.run(main())
```

This example demonstrates the complete checkpointing workflow:

1. **Enable checkpointing**: configure the SDK with `enable_file_checkpointing=True` and `permission_mode="acceptEdits"` to auto-approve file edits
2. **Capture checkpoint data**: as the agent runs, store the first user message UUID (your restore point) and the session ID
3. **Prompt for rewind**: after the agent finishes, check your utility file to see the doc comments, then decide if you want to undo the changes
4. **Resume and rewind**: if yes, resume the session with an empty prompt and call `rewind_files()` to restore the original file

3

Run the example

Run the script from the same directory as your utility file.

Open your utility file (`utils.py` or `utils.ts`) in your IDE or editor before running the script. You’ll see the file update in real-time as the agent adds doc comments, then revert back to the original when you choose to rewind.

* Python
* TypeScript

```
python try_checkpointing.py
```

```
npx tsx try_checkpointing.ts
```

You’ll see the agent add doc comments, then a prompt asking if you want to rewind. If you choose yes, the file is restored to its original state.

## [​](#limitations) Limitations

File checkpointing has the following limitations:

| Limitation | Description |
| --- | --- |
| Write/Edit/NotebookEdit tools only | Changes made through Bash commands are not tracked |
| Same session | Checkpoints are tied to the session that created them |
| File content only | Creating, moving, or deleting directories is not undone by rewinding |
| Local files | Remote or network files are not tracked |

## [​](#troubleshooting) Troubleshooting

### [​](#checkpointing-options-not-recognized) Checkpointing options not recognized

If `enableFileCheckpointing` or `rewindFiles()` isn’t available, you may be on an older SDK version.
**Solution**: Update to the latest SDK version:

* **Python**: `pip install --upgrade claude-agent-sdk`
* **TypeScript**: `npm install @anthropic-ai/claude-agent-sdk@latest`

### [​](#user-messages-don’t-have-uuids) User messages don’t have UUIDs

If `message.uuid` is `undefined` or missing, you’re not receiving checkpoint UUIDs.
**Cause**: The `replay-user-messages` option isn’t set.
**Solution**: Add `extra_args={"replay-user-messages": None}` (Python) or `extraArgs: { 'replay-user-messages': null }` (TypeScript) to your options.

### [​](#”no-file-checkpoint-found-for-message”-error) ”No file checkpoint found for message” error

This error occurs when the checkpoint data doesn’t exist for the specified user message UUID.
**Common causes**:

* File checkpointing was not enabled on the original session (`enable_file_checkpointing` or `enableFileCheckpointing` was not set to `true`)
* The session wasn’t properly completed before attempting to resume and rewind

**Solution**: Ensure `enable_file_checkpointing=True` (Python) or `enableFileCheckpointing: true` (TypeScript) was set on the original session, then use the pattern shown in the examples: capture the first user message UUID, complete the session fully, then resume with an empty prompt and call `rewindFiles()` once.

### [​](#”processtransport-is-not-ready-for-writing”-error) ”ProcessTransport is not ready for writing” error

This error occurs when you call `rewindFiles()` or `rewind_files()` after you’ve finished iterating through the response. The connection to the CLI process closes when the loop completes.
**Solution**: Resume the session with an empty prompt, then call rewind on the new query:

Python

TypeScript

```