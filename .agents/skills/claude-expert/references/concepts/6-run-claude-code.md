---
type: Reference
title: 6. Run Claude Code
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# 6. Run Claude Code
claude
```

The default export intervals are 60 seconds for metrics and 5 seconds for logs. During setup, you may want to use shorter intervals for debugging purposes. Remember to reset these for production use.

For full configuration options, see the [OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## [​](#administrator-configuration) Administrator configuration

Administrators can configure OpenTelemetry settings for all users through the [managed settings file](/docs/en/settings#settings-files). This allows for centralized control of telemetry settings across an organization. See the [settings precedence](/docs/en/settings#settings-precedence) for more information about how settings are applied.
Example managed settings configuration:

```
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

Managed settings can be distributed via MDM (Mobile Device Management) or other device management solutions. Environment variables defined in the managed settings file have high precedence and can’t be overridden by users.

Claude Code doesn’t pass `OTEL_*` environment variables to the subprocesses it spawns, including the Bash tool, hooks, MCP servers, and language servers. An OpenTelemetry-instrumented application that you run through the Bash tool doesn’t inherit Claude Code’s exporter endpoint or headers, so set those variables directly in the command if that application needs to export its own telemetry.

## [​](#configuration-details) Configuration details

### [​](#common-configuration-variables) Common configuration variables

| Environment Variable | Description | Example Values |
| --- | --- | --- |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enables telemetry collection (required) | `1` |
| `OTEL_METRICS_EXPORTER` | Metrics exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `prometheus`, `none` |
| `OTEL_LOGS_EXPORTER` | Logs/events exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `none` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Protocol for OTLP exporter, applies to all signals | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint for all signals | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` | Protocol for metrics, overrides general setting | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | OTLP metrics endpoint, overrides general setting | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` | Protocol for logs, overrides general setting | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | OTLP logs endpoint, overrides general setting | `http://localhost:4318/v1/logs` |
| `OTEL_EXPORTER_OTLP_HEADERS` | Authentication headers for OTLP | `Authorization=Bearer token` |
| `OTEL_METRIC_EXPORT_INTERVAL` | Export interval in milliseconds (default: 60000) | `5000`, `60000` |
| `OTEL_LOGS_EXPORT_INTERVAL` | Logs export interval in milliseconds (default: 5000) | `1000`, `10000` |
| `OTEL_LOG_USER_PROMPTS` | Enable logging of user prompt content (default: disabled) | `1` to enable |
| `OTEL_LOG_TOOL_DETAILS` | Enable logging of tool parameters and input arguments in tool events and trace span attributes: Bash commands, MCP server and tool names, skill names, and tool input. Also enables custom, plugin, and MCP command names on `user_prompt` events (default: disabled) | `1` to enable |
| `OTEL_LOG_TOOL_CONTENT` | Enable logging of tool input and output content in span events (default: disabled). Requires [tracing](#traces-beta). Content is truncated at 60 KB | `1` to enable |
| `OTEL_LOG_RAW_API_BODIES` | Emit the full Anthropic Messages API request and response JSON as `api_request_body` / `api_response_body` log events (default: disabled). Bodies include the entire conversation history. Enabling this implies consent to everything `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, and `OTEL_LOG_TOOL_CONTENT` would reveal | `1` for inline bodies truncated at 60 KB, or `file:<dir>` for untruncated bodies on disk with a `body_ref` pointer in the event |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Metrics temporality preference (default: `delta`). Set to `cumulative` if your backend expects cumulative temporality | `delta`, `cumulative` |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | Interval for refreshing dynamic headers (default: 1740000ms / 29 minutes) | `900000` |

### [​](#mtls-authentication) mTLS authentication

How you configure client certificates for the OTLP exporter depends on the OTLP protocol in use for that signal, set via `OTEL_EXPORTER_OTLP_PROTOCOL` or the per-signal override. The same configuration applies to metrics, logs, and traces.

| Protocol | Client certificate variables | Trust the collector’s CA with |
| --- | --- | --- |
| `http/protobuf`, `http/json` | `CLAUDE_CODE_CLIENT_CERT`, `CLAUDE_CODE_CLIENT_KEY`, and optionally `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`. See [Network configuration](/docs/en/network-config#mtls-authentication) | `NODE_EXTRA_CA_CERTS` |
| `grpc` | `OTEL_EXPORTER_OTLP_CLIENT_KEY` and `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`, or the per-signal variants such as `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` to use a different certificate per signal | `OTEL_EXPORTER_OTLP_CERTIFICATE` |

For `grpc`, the OpenTelemetry SDK reads the standard OTLP variables directly, so existing configurations that set the per-signal metrics variables continue to work.

### [​](#metrics-cardinality-control) Metrics cardinality control

The following environment variables control which attributes are included in metrics to manage cardinality:

| Environment Variable | Description | Default Value | Example to Disable |
| --- | --- | --- | --- |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | Include session.id attribute in metrics | `true` | `false` |
| `OTEL_METRICS_INCLUDE_VERSION` | Include app.version attribute in metrics | `false` | `true` |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Include user.account\_uuid and user.account\_id attributes in metrics | `true` | `false` |
| `OTEL_METRICS_INCLUDE_ENTRYPOINT` | Include app.entrypoint attribute in metrics | `false` | `true` |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | Include keys from `OTEL_RESOURCE_ATTRIBUTES` as attributes on metric datapoints | `true` | `false` |

These variables help control the cardinality of metrics, which affects storage requirements and query performance in your metrics backend. Lower cardinality generally means better performance and lower storage costs but less granular data for analysis.

### [​](#traces-beta) Traces (beta)

Distributed tracing exports spans that link each user prompt to the API requests and tool executions it triggers, so you can view a full request as a single trace in your tracing backend.
Tracing is off by default. To enable it, set both `CLAUDE_CODE_ENABLE_TELEMETRY=1` and `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, then set `OTEL_TRACES_EXPORTER` to choose where spans are sent. Traces reuse the [common OTLP configuration](#common-configuration-variables) for endpoint, protocol, headers, and [mTLS](#mtls-authentication).

| Environment Variable | Description | Example Values |
| --- | --- | --- |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Enable span tracing (required). `ENABLE_ENHANCED_TELEMETRY_BETA` is also accepted | `1` |
| `OTEL_TRACES_EXPORTER` | Traces exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `none` |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | Protocol for traces, overrides `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | OTLP traces endpoint, overrides `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318/v1/traces` |
| `OTEL_TRACES_EXPORT_INTERVAL` | Span batch export interval in milliseconds (default: 5000) | `1000`, `10000` |

Spans redact user prompt text, tool input details, and tool content by default. Set `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1`, and `OTEL_LOG_TOOL_CONTENT=1` to include them.
When tracing is active, Bash and PowerShell subprocesses automatically inherit a `TRACEPARENT` environment variable containing the W3C trace context of the active tool execution span. This lets any subprocess that reads `TRACEPARENT` parent its own spans under the same trace, enabling end-to-end distributed tracing through scripts and commands that Claude runs.
When tracing is active and Claude Code is connected directly to the Anthropic API, each model request carries a W3C `traceparent` header set to the `claude_code.llm_request` span’s context, and the API’s `traceresponse` header is recorded as a span link. Together these connect Claude Code’s client-side spans to the server-side trace through any compliant intermediary. Outbound HTTP MCP requests carry `traceparent` the same way. The header is not sent to third-party providers.
By default, the `traceparent` header on model and HTTP MCP requests is sent only when `ANTHROPIC_BASE_URL` is unset or points at the Anthropic API, since some proxies reject unrecognized headers. The subprocess `TRACEPARENT` variable is controlled by the same switch for consistency. If you run Claude Code through a custom `ANTHROPIC_BASE_URL` proxy and want trace context propagated, set `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1`.
In Agent SDK and non-interactive sessions started with `-p`, Claude Code also reads `TRACEPARENT` and `TRACESTATE` from its own environment when starting each interaction span. This lets an embedding process pass its active W3C trace context into the subprocess so Claude Code’s spans appear as children of the caller’s distributed trace. Interactive sessions ignore inbound `TRACEPARENT` to avoid accidentally inheriting ambient values from CI or container environments.

#### [​](#span-hierarchy) Span hierarchy

Each user prompt starts a `claude_code.interaction` root span. API calls, tool calls, and hook executions are recorded as its children. Tool spans have two child spans of their own: one for the time spent waiting on a permission decision and one for the execution itself. When the Agent tool, or legacy Task tool, spawns a subagent, the subagent’s API and tool spans nest under the parent’s `claude_code.tool` span.

```
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requires detailed beta tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Agent tool) subagent claude_code.llm_request / claude_code.tool spans
```

In Agent SDK and `claude -p` sessions, `claude_code.interaction` itself becomes a child of the caller’s span when `TRACEPARENT` is set in the environment.

#### [​](#span-attributes) Span attributes

Every span carries the [standard attributes](#standard-attributes) plus a `span.type` attribute matching its name. The tables below list the additional attributes set on each span. The `llm_request`, `tool.execution`, and `hook` spans set OpenTelemetry status `ERROR` when they record a failure; the other spans always end with status `UNSET`.
**`claude_code.interaction`**

| Attribute | Description | Gated by |
| --- | --- | --- |
| `user_prompt` | Prompt text. Value is `<REDACTED>` unless the gate is set | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length` | Prompt length in characters |  |
| `interaction.sequence` | 1-based counter of interactions in this session |  |
| `interaction.duration_ms` | Wall-clock duration of the turn |  |

**`claude_code.llm_request`**

| Attribute | Description | Gated by |
| --- | --- | --- |
| `model` | Model identifier |  |
| `gen_ai.system` | Always `anthropic`. OpenTelemetry GenAI semantic convention |  |
| `gen_ai.request.model` | Same value as `model`. OpenTelemetry GenAI semantic convention |  |
| `query_source` | Subsystem that issued the request, such as `repl_main_thread` or a subagent name |  |
| `agent_id` | Identifier of the subagent or teammate that issued the request. Absent on the main session |  |
| `parent_agent_id` | Identifier of the agent that spawned this one. Absent for the main session and for agents spawned directly from it |  |
| `speed` | `fast` or `normal` |  |
| `llm_request.context` | `interaction`, `tool`, or `standalone` depending on the parent span |  |
| `duration_ms` | Wall-clock duration including retries |  |
| `ttft_ms` | Time to first token in milliseconds |  |
| `input_tokens` | Input token count from the API usage block |  |
| `output_tokens` | Output token count |  |
| `cache_read_tokens` | Tokens read from prompt cache |  |
| `cache_creation_tokens` | Tokens written to prompt cache |  |
| `request_id` | Anthropic API request ID from the `request-id` response header |  |
| `gen_ai.response.id` | Same value as `request_id`. OpenTelemetry GenAI semantic convention |  |
| `client_request_id` | Client-generated `x-client-request-id` of the final attempt |  |
| `attempt` | Total attempts made for this request |  |
| `success` | `true` or `false` |  |
| `status_code` | HTTP status code when the request failed |  |
| `error` | Error message when the request failed |  |
| `response.has_tool_call` | `true` when the response contained tool-use blocks |  |
| `stop_reason` | API response `stop_reason`, such as `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn`, or `refusal` |  |
| `gen_ai.response.finish_reasons` | Same value as `stop_reason`, wrapped in a string array. OpenTelemetry GenAI semantic convention |  |

Each retry attempt is also recorded as a `gen_ai.request.attempt` span event with `attempt` and `client_request_id` attributes.
**`claude_code.tool`**

| Attribute | Description | Gated by |
| --- | --- | --- |
| `tool_name` | Tool name |  |
| `duration_ms` | Wall-clock duration including permission wait and execution |  |
| `result_tokens` | Approximate token size of the tool result |  |
| `agent_id` | Identifier of the subagent or teammate that ran the tool. Absent on the main session |  |
| `parent_agent_id` | Identifier of the agent that spawned this one. Absent for the main session and for agents spawned directly from it |  |
| `tool_use_id` | The model’s `tool_use` block id for this call. Matches the `tool_use_id` on the [tool\_result](#tool-result-event) and [tool\_decision](#tool-decision-event) events and in hook payloads, so you can join the span to those records |  |
| `gen_ai.tool.call.id` | Same value as `tool_use_id`. OpenTelemetry GenAI semantic convention |  |
| `file_path` | Target file path for Read, Edit, and Write tools | `OTEL_LOG_TOOL_DETAILS` |
| `full_command` | Command string for the Bash tool | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name` | Skill name for the Skill tool | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Subagent type for the Agent tool or legacy Task tool | `OTEL_LOG_TOOL_DETAILS` |

When `OTEL_LOG_TOOL_CONTENT=1`, this span also records a `tool.output` span event whose attributes contain the tool’s input and output bodies, truncated at 60 KB per attribute.
**`claude_code.tool.blocked_on_user`**

| Attribute | Description | Gated by |
| --- | --- | --- |
| `duration_ms` | Time spent waiting for the permission decision |  |
| `decision` | `accept` or `reject` |  |
| `source` | Decision source, matching the [Tool decision event](#tool-decision-event) |  |

**`claude_code.tool.execution`**

| Attribute | Description | Gated by |
| --- | --- | --- |
| `duration_ms` | Time spent running the tool body |  |
| `tool_use_id` | Same value as on the parent `claude_code.tool` span |  |
| `gen_ai.tool.call.id` | Same value as `tool_use_id`. OpenTelemetry GenAI semantic convention |  |
| `success` | `true` or `false` |  |
| `error` | Error category string when execution failed, such as `Error:ENOENT` or `ShellError`. Contains the full error message instead when the gate is set | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**
This span is emitted only when detailed beta tracing is active, which requires `ENABLE_BETA_TRACING_DETAILED=1` and `BETA_TRACING_ENDPOINT` in addition to the trace exporter configuration above. In interactive CLI sessions, this also requires your organization to be allowlisted for the feature. Agent SDK and non-interactive `-p` sessions are not gated. It is not emitted when only `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` is set.

| Attribute | Description | Gated by |
| --- | --- | --- |
| `hook_event` | Hook event type, such as `PreToolUse` |  |
| `hook_name` | Full hook name, such as `PreToolUse:Write` |  |
| `num_hooks` | Number of matching hook commands executed |  |
| `hook_definitions` | JSON-serialized hook configuration | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms` | Wall-clock duration of all matching hooks |  |
| `num_success` | Count of hooks that completed successfully |  |
| `num_blocking` | Count of hooks that returned a blocking decision |  |
| `num_non_blocking_error` | Count of hooks that failed without blocking |  |
| `num_cancelled` | Count of hooks cancelled before completion |  |

Additional content-bearing attributes such as `new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input`, and `response.model_output` are emitted only when detailed beta tracing is active. They are not part of the stable span schema. `user_system_prompt` additionally requires `OTEL_LOG_USER_PROMPTS=1`. It carries only the system prompt text you provide via the `systemPrompt` SDK option or `--system-prompt` and `--append-system-prompt` flags, truncated at 60 KB, and is emitted once per session rather than per request.

### [​](#dynamic-headers) Dynamic headers

For enterprise environments that require dynamic authentication, you can configure a script to generate headers dynamically. Dynamic headers apply only to the `http/protobuf` and `http/json` protocols. The `grpc` exporter uses only the static `OTEL_EXPORTER_OTLP_HEADERS` value.

#### [​](#settings-configuration) Settings configuration

Add to your `.claude/settings.json`:

```
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

The value can be the path to an executable file, including a path that contains spaces, or a shell command line with arguments. On Windows, the value always runs through the shell, so quote a path that contains spaces inside the JSON value.

#### [​](#script-requirements) Script requirements

The script must output valid JSON with string key-value pairs representing HTTP headers:

```
#!/bin/bash