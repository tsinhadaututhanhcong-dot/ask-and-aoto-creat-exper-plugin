---
name: claude-expert
description: >
  Wiki nội bộ (Tier 1) về toàn bộ hệ sinh thái Claude: CLI, Desktop, VS Code, JetBrains, Web, Agent SDK,
  và các nhà cung cấp doanh nghiệp (Bedrock/Vertex AI/Foundry). Tra cứu tài liệu gốc Anthropic trước khi suy đoán.
  Dùng khi agent hoặc workflow cần hiểu: tính năng X là gì, thuộc nền tảng nào, dùng vào việc gì, khi nào dùng, cách cấu hình.
when_to_use: >
  - Khi agent cần hiểu một tính năng của Claude (CLI/Desktop/VS Code/JetBrains/Web/SDK) trước khi thao tác UI.
  - Khi cần xác định một tính năng có tồn tại trên một nền tảng cụ thể hay không, hoặc so sánh nền tảng này với nền tảng khác.
  - Khi workflow /autopilot-tune cần đối chiếu tính năng với tài liệu chính thức (chống ảo giác).
  - Khi phát hiện tính năng mới trên màn hình nhưng chưa biết mục đích.
  - Khi cần tra cứu cách cấu hình MCP, SDK, hooks, permissions, plugins.
allowed-tools: Read, Grep
effort: medium
---

# 🧠 Chuyên gia Claude — Wiki Nội bộ (Tier 1)

## Vai trò trong hệ thống

Skill này đóng vai trò **Bộ não tri thức** (Knowledge Oracle) của plugin `claude-autopilot`.
Nó chứa 372 bài viết gốc từ tài liệu chính thức Anthropic, được tổ chức thành thư mục `references/concepts/`.
`references/INDEX.md` được nhóm theo **nền tảng** (CLI / Desktop / VS Code / JetBrains / Web / Agent SDK / nhà cung cấp doanh nghiệp / tích hợp / dùng chung) — không còn là danh sách phẳng.

### Phân tầng tri thức (Knowledge Tiering)

```
┌─────────────────────────────────────────┐
│  Tier 1: claude-expert (BẠN)            │  ← Hỏi TRƯỚC, luôn luôn
│  Wiki nội bộ, 372 files, offline        │
├─────────────────────────────────────────┤
│  Tier 2: deep-research                  │  ← Hỏi SAU, chỉ khi Tier 1 thiếu
│  Web search, online, tốn thời gian      │
└─────────────────────────────────────────┘
```

**Quy tắc tuyệt đối:** Agent KHÔNG ĐƯỢC dựa vào trí nhớ pre-trained để trả lời về tính năng Claude. BẮT BUỘC đọc file trong thư mục `references/` bằng tool `Read`.

## 🛑 Những điểm dễ sai (Gotchas)

| ❌ CÁCH LÀM SAI (Ảo giác) | ✅ CÁCH LÀM ĐÚNG (Dựa trên tài liệu) |
|---|---|
| Dựa trên trí nhớ hoặc kiến thức pre-train có sẵn (dẫn đến ảo giác). | **BẮT BUỘC** dùng tool `Read` để đọc tệp `references/INDEX.md` TRƯỚC, sau đó đọc các file concept tương ứng trong thư mục `references/concepts/`. |
| Tìm thấy 1 file khớp từ khóa và kết luận ngay tính năng đó "cũng có" trên nền tảng đang được hỏi. | Kiểm tra trường `platform:` trong frontmatter của file đó (hoặc mục nó nằm trong INDEX.md). Nếu `platform` khác với nền tảng đang hỏi, KHÔNG được suy diễn — phải đối chiếu lại mục "Bảng đối chiếu nền tảng chính thức" rồi mới trả lời. Đây chính là lỗi khiến wiki từng bị lẫn giữa CLI và Desktop. |

## 🌳 Cây Quyết định (Decision Tree)

Mỗi khi nhận được yêu cầu:

0. **Bước 0 — Xác định nền tảng đang được hỏi (BẮT BUỘC, làm trước mọi bước khác):**
   - Phân loại câu hỏi vào một trong: `cli` · `desktop` · `vscode` · `jetbrains` · `web` · `sdk` · `enterprise-provider` (Bedrock/Vertex/Foundry) · `integration` (GitHub/GitLab/Slack/Chrome) · `shared` (dùng chung mọi nền tảng) · hoặc "so sánh giữa nhiều nền tảng".
   - **Nếu câu hỏi có dạng "nền tảng X có tính năng Y không" hoặc "X khác Y ở đâu":** đọc mục **"Bảng đối chiếu nền tảng chính thức (tra trước tiên)"** ở đầu `INDEX.md` (feature-availability, desktop feature-comparison, platforms-and-integrations) TRƯỚC KHI tra từ khóa. Ba file này là nguồn sự thật duy nhất cho câu hỏi có/không giữa các nền tảng.
   - Chỉ sau khi đã xác định nền tảng, mới tìm tiếp trong đúng mục nền tảng đó + mục "Dùng chung mọi nền tảng" của `INDEX.md`.

1. **NẾU agent/user hỏi nguyên lý, API, cách cấu hình, hoặc gỡ lỗi:**
   - **Bước 1:** Đọc file `references/INDEX.md` (đường dẫn tương đối từ thư mục skill này), tìm trong đúng mục nền tảng đã xác định ở Bước 0.
   - **Bước 2:** Dùng tool `Read` để đọc các tệp `.md` cụ thể trong thư mục `references/concepts/` mà INDEX trỏ tới.
   - **Bước 3:** Trích xuất thông tin liên quan trực tiếp đến câu hỏi và trả lời.

2. **NẾU workflow `/autopilot-tune` hỏi trong quá trình tự học:**
   - Đọc `INDEX.md`, tìm concept liên quan đến tính năng đang khám phá.
   - Trả về: **Tên tính năng**, **Nền tảng**, **Mục đích**, **Khi nào dùng**, **Cách hoạt động**.
   - Nếu INDEX không có mục nào liên quan → Trả về `WIKI_NOT_FOUND` để agent biết cần escalate sang `deep-research`.

3. **NẾU Agent khác hỏi để lấy ngữ cảnh:**
   - Đọc `INDEX.md` và các concept file liên quan, sau đó trả về đúng JSON / cấu trúc dữ liệu được yêu cầu.

## 🔍 Khi nào Wiki KHÔNG ĐỦ (Escalate sang Tier 2)

Trả về tín hiệu `WIKI_NOT_FOUND` hoặc `WIKI_INSUFFICIENT` khi:
- Tìm trong INDEX.md không thấy concept nào khớp với tính năng cần tra.
- Concept file tìm được nhưng nội dung quá cũ (nhắc đến phiên bản cũ hơn phiên bản hiện tại).
- Tính năng rõ ràng tồn tại trên UI (Vision xác nhận) nhưng wiki không có thông tin.

→ Lúc này, agent sẽ kích hoạt `deep-research` (Tier 2) để tìm kiếm trên web.

## 🔄 Tự Nhận Thức & Cập Nhật (Self-Update)
- URL nguồn: `https://code.claude.com/docs/en/desktop`, `https://code.claude.com/docs/en/feature-availability`, `https://code.claude.com/docs/en/platforms` (3 file đối chiếu nền tảng chính thức)
- Ngày thu thập: `2026-06-29`
- Khi phát hiện wiki quá cũ, ghi vào `knowledge_gaps.md` flag `WIKI_STALE` và đề xuất cập nhật.
- Lịch sử tinh chỉnh phân nền tảng + tách file trùng tên: xem `references/COLLISIONS.md` và `references/_tools/reorganize.py`.
