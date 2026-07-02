---
title: Collision log (filename overwrite investigation)
date_created: 2026-07-01
---

# Collision log

Khi crawl tài liệu gốc thành `references/concepts/*.md`, nhiều mục trong cùng một trang tài liệu dùng chung một tiêu đề (ví dụ "Basic syntax" xuất hiện ở nhiều tab ví dụ khác nhau trên cùng một trang). Vì tên file được suy ra từ tiêu đề, các mục trùng tiêu đề bị ghi đè lên nhau trên đĩa — chỉ bản ghi cuối cùng còn tồn tại.

`INDEX.md` cũ tham chiếu tới cùng một filename từ nhiều dòng khác nhau. Đã quét toàn bộ `INDEX.md` (401 dòng, 395 link, 360 filename khác nhau) để tìm mọi trường hợp trùng, rồi kiểm tra thủ công (đọc lại nội dung sống trên `code.claude.com` qua WebFetch) xem nội dung có thực sự khác nhau hay chỉ là liên kết trùng lặp vô hại.

## Đã tách thành file riêng (nội dung thực sự khác nhau, khôi phục được từ nguồn sống)

| Slug gốc bị trùng | Tách thành |
|---|---|
| `basic-syntax.md` (5 lần, trang "Connect Claude Code to tools via MCP") | `basic-syntax--http-transport.md`, `basic-syntax--sse-transport.md`, `basic-syntax--stdio-transport.md`, `basic-syntax--add-json.md`, `basic-syntax--add-from-claude-desktop.md`, `basic-syntax--serve.md` |
| `enable-bedrock.md` (2 lần, trang "Enterprise deployment overview") | `enable-bedrock--corporate-proxy.md`, `enable-bedrock--llm-gateway.md` |
| `enable-microsoft-foundry.md` (2 lần, cùng trang) | `enable-microsoft-foundry--corporate-proxy.md`, `enable-microsoft-foundry--llm-gateway.md` |
| `enable-vertex.md` (2 lần, cùng trang) | `enable-vertex--corporate-proxy.md`, `enable-vertex--llm-gateway.md` |
| `configure-llm-gateway.md` (3 lần, cùng trang, mỗi nhà cung cấp một biến thể) | `configure-llm-gateway--bedrock.md`, `configure-llm-gateway--foundry.md`, `configure-llm-gateway--vertex.md` |
| `remove-user-settings-and-state.md` (2 lần, trang "Advanced setup") | `remove-user-settings-and-state--windows.md`, `remove-user-settings-and-state--macos-linux-wsl.md` |
| `remove-project-specific-settings-run-from-your-project-directory.md` (2 lần, cùng trang) | `remove-project-specific-settings--windows.md`, `remove-project-specific-settings--macos-linux-wsl.md` |

7 file gốc bị trùng đã bị xóa sau khi tách; nội dung của cả hai/ba biến thể đều được giữ lại đầy đủ trong các file mới, lấy trực tiếp từ trang tài liệu sống (không suy đoán).

## Đã kiểm tra, xác nhận an toàn (nội dung giống hệt nhau hoặc chỉ là liên kết trùng lặp — không cần tách)

- `overview-claude-code-docs.md`, `configure-permissions-claude-code-docs.md`, `quickstart-claude-code-docs.md`, `claude-code-on-microsoft-foundry-claude-code-docs.md` (+ 4 fragment con), `extend-claude-with-skills-claude-code-docs.md` (+ 4 fragment con): cùng một trang được liệt kê 2 lần trong INDEX.md (do xuất hiện ở 2 vị trí điều hướng khác nhau trên trang gốc), nội dung y hệt nhau cả 2 lần.
- `optional-disable-prompt-caching-if-needed.md`, `optional-request-1-hour-prompt-cache-ttl-instead-of-the-5-minute-default.md`: xuất hiện trên cả trang Bedrock lẫn trang Vertex AI, nhưng đã đối chiếu nội dung sống — cả hai nhà cung cấp dùng đúng cùng một biến môi trường (`DISABLE_PROMPT_CACHING=1` / `ENABLE_PROMPT_CACHING_1H=1`), không có khác biệt.
- `additional-instructions.md`: xuất hiện trên cả trang "Best practices" lẫn trang "How Claude remembers your project", cả hai đều là ví dụ minh họa cú pháp `@import` gần như giống hệt nhau trong khối code mẫu — không phải nội dung thực chất khác nhau, không đáng để tách.
- `required-workaround-dummy-hook-keeps-the-stream-open-for-can-use-tool.md`: xuất hiện 2 lần trên trang "Handle approvals and user input" (một lần trong ví dụ cơ bản, một lần trong "Complete example"), cả hai đều là cùng một đoạn code Python `dummy_hook` giống hệt nhau.

Không còn trường hợp nào chưa xử lý được (không có mục nào phải bỏ dở do WebFetch thất bại).
