# IRC | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/irc](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/messaging/irc)

本页总览

The IRC adapter connects Hermes to any IRC server and relays messages between an IRC channel (or direct messages) and the agent. It speaks the IRC protocol over Python's stdlib `asyncio` — **no external dependencies, no SDK, no daemon**. It works with public networks like [Libera.Chat](https://libera.chat/) and any self-hosted ircd.

IRC is plain text: there is no voice, image, file, thread, reaction, typing, or streaming support — replies are sent as `PRIVMSG` lines, with long messages split to fit the IRC line limit.

> Run `hermes gateway setup` and pick **IRC** for a guided walk-through.

## Prerequisites[​](#prerequisites "Prerequisites的直接链接")

* An IRC server to connect to (e.g. `irc.libera.chat`)
* A channel to join (e.g. `#hermes`) — comma-separate to join several
* A nickname for the bot (default: `hermes-bot`)
* Optional: a registered nick + NickServ password if your network requires identification

## Configure Hermes[​](#configure-hermes "Configure Hermes的直接链接")

You can configure IRC two ways — environment variables (for a quick env-only setup) or the `gateway` block in `~/.hermes/gateway-config.yaml`.

### Option A — gateway-config.yaml[​](#option-a--gateway-configyaml "Option A — gateway-config.yaml的直接链接")

```
gateway:  
  platforms:  
    irc:  
      enabled: true  
      extra:  
        server: irc.libera.chat  
        port: 6697  
        nickname: hermes-bot  
        channel: "#hermes"  
        use_tls: true  
        server_password: ""       # optional server password  
        nickserv_password: ""     # optional NickServ identification  
        allowed_users: []         # empty = allow all, or list of nicks  
        max_message_length: 450   # IRC line limit (safe default)
```

### Option B — environment variables[​](#option-b--environment-variables "Option B — environment variables的直接链接")

| Variable | Required | Description |
| --- | --- | --- |
| `IRC_SERVER` | ✅ | IRC server hostname (e.g. `irc.libera.chat`) |
| `IRC_CHANNEL` | ✅ | Channel(s) to join — comma-separate for multiple |
| `IRC_NICKNAME` | ✅ | Bot nickname (default: `hermes-bot`) |
| `IRC_PORT` | — | Server port (default: `6697` with TLS, `6667` without) |
| `IRC_USE_TLS` | — | Use TLS (`true`/`false`; default `true` on port 6697) |
| `IRC_SERVER_PASSWORD` | — | Server password for the `PASS` command |
| `IRC_NICKSERV_PASSWORD` | — | NickServ password for automatic IDENTIFY on connect |
| `IRC_ALLOWED_USERS` | — | Comma-separated nicks allowed to talk to the bot |
| `IRC_ALLOW_ALL_USERS` | — | Allow anyone in the channel to talk to the bot (dev only) |
| `IRC_HOME_CHANNEL` | — | Channel for cron / notification delivery (defaults to `IRC_CHANNEL`) |

## Access control[​](#access-control "Access control的直接链接")

By default, only nicks listed in `allowed_users` (or `IRC_ALLOWED_USERS`) may talk to the bot. Leave the list empty **and** set `IRC_ALLOW_ALL_USERS=true` to let anyone in the channel chat with Hermes — useful for testing, but not recommended on public networks since IRC nicks are not authenticated unless the network enforces NickServ.

If your network registers nicks, set `IRC_NICKSERV_PASSWORD` (or `nickserv_password`) so the bot identifies to NickServ on connect and keeps its registered nick.

## Channels vs. DMs[​](#channels-vs-dms "Channels vs. DMs的直接链接")

* Messages in a joined channel are treated as a **group** conversation.
* Private messages to the bot are treated as **direct messages**.

Cron jobs and notifications are delivered to the **home channel** — `IRC_HOME_CHANNEL` if set, otherwise the first `IRC_CHANNEL`.

## Run the gateway[​](#run-the-gateway "Run the gateway的直接链接")

```
hermes gateway start
```

Check status with `hermes gateway status` — IRC connection state is reported there, including for env-only setups.

## Notes[​](#notes "Notes的直接链接")

* Long agent replies are automatically split into multiple `PRIVMSG` lines to stay within the IRC line limit (`max_message_length`, default 450 bytes after protocol overhead).
* The adapter acquires a scoped credential lock per server+nick, so two Hermes profiles won't fight over the same IRC identity.

* [Prerequisites](#prerequisites)
* [Configure Hermes](#configure-hermes)
  + [Option A — gateway-config.yaml](#option-a--gateway-configyaml)
  + [Option B — environment variables](#option-b--environment-variables)
* [Access control](#access-control)
* [Channels vs. DMs](#channels-vs-dms)
* [Run the gateway](#run-the-gateway)
* [Notes](#notes)