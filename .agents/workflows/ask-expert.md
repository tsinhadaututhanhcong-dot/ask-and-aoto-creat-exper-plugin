---
description: Route một câu hỏi chuyên môn tới đúng expert skill, hoặc tạo expert mới từ trang docs chính thức nếu chưa có ai phù hợp
---

Người dùng (hoặc một agent khác) muốn được trả lời một câu hỏi chuyên môn.

Nếu chưa rõ câu hỏi cụ thể là gì, hỏi lại trước khi tiếp tục.

Đọc file `.agents/skills/ask-expert/SKILL.md` và làm theo đúng cây quyết định trong đó: tra registry (tĩnh + động) → route tới expert phù hợp nếu có → nếu chưa có, xác minh trang docs chính thức rồi điều phối skill `docs-to-expert` tạo expert mới → route sang expert vừa tạo để trả lời câu hỏi gốc.

Đây là lối vào tường minh (so với việc `ask-expert` tự trigger theo mô tả skill) — dùng khi cần chắc chắn logic router chạy, ví dụ khi một agent khác gọi workflow này để lấy ngữ cảnh chuyên môn một cách xác định (deterministic), thay vì trông chờ auto-trigger.
