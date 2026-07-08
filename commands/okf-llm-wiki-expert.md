---
description: Chuyên gia tra cứu và hướng dẫn về OKF (Open Knowledge Format) của Google và mẫu hình LLM-wiki của Karpathy
argument-hint: [câu hỏi chuyên môn về OKF hoặc LLM-wiki]
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Skill, Write, Edit
---

Người dùng (hoặc một agent khác) muốn được trả lời một câu hỏi chuyên môn liên quan đến OKF hoặc mẫu hình LLM-wiki: "$ARGUMENTS"

Nếu `$ARGUMENTS` rỗng, hỏi người dùng câu hỏi cụ thể là gì trước khi tiếp tục.

Dùng `Skill` tool để load skill `okf-llm-wiki-expert` (cùng plugin), rồi làm theo hướng dẫn của nó để tra cứu tài liệu tham khảo và trả lời câu hỏi gốc.
