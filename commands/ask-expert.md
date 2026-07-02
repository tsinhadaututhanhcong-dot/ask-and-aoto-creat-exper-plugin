---
description: Route một câu hỏi chuyên môn tới đúng expert skill, hoặc tạo expert mới từ trang docs chính thức nếu chưa có ai phù hợp
argument-hint: [câu hỏi chuyên môn]
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Skill, Write, Edit
---

Người dùng (hoặc một agent khác) muốn được trả lời một câu hỏi chuyên môn: "$ARGUMENTS"

Nếu `$ARGUMENTS` rỗng, hỏi người dùng câu hỏi cụ thể là gì trước khi tiếp tục.

Dùng `Skill` tool để load skill `ask-expert` (cùng plugin), rồi làm theo đúng cây quyết định của nó: tra registry (tĩnh + cá nhân) → route tới expert phù hợp nếu có → nếu chưa có, xác minh trang docs chính thức rồi điều phối `docs-to-expert` tạo expert mới → route sang expert vừa tạo để trả lời câu hỏi gốc.

Đây là lối vào tường minh (so với việc `ask-expert` tự trigger theo mô tả) — dùng khi cần chắc chắn logic router chạy, ví dụ khi một agent khác gọi lệnh này để lấy ngữ cảnh chuyên môn một cách xác định (deterministic), thay vì trông chờ auto-trigger.
