---
trigger: always_on
---
# GEMINI.md — expert-skills

## 0. Ngôn ngữ
User dùng tiếng Việt → trả lời tiếng Việt; code/định danh/tên file = English.

## 1. ROUTING (ưu tiên tuyệt đối: lệnh `/…` và `@…` thắng khớp từ khoá)

| Tín hiệu | Kích hoạt |
|---|---|
| `/ask-expert <câu hỏi>` | Đọc `.agents/workflows/ask-expert.md`, làm theo đúng quy trình trong đó |
| `/okf-llm-wiki-expert <câu hỏi>` | Đọc `.agents/workflows/okf-llm-wiki-expert.md`, làm theo đúng quy trình trong đó |
| Câu hỏi chuyên môn về một domain cụ thể (framework/SDK/API/sản phẩm...), không rõ có expert phù hợp hay chưa | Đọc `.agents/skills/ask-expert/SKILL.md`, áp dụng cây quyết định của nó (tra registry → route hoặc tạo mới) |
| Claude Code / CLI / Desktop / VS Code / JetBrains / Agent SDK / Bedrock / Vertex AI / Foundry | `.agents/skills/claude-expert/SKILL.md` |
| Google Antigravity / Antigravity 2.0 / Antigravity IDE / Antigravity CLI / `agy` / Antigravity SDK | `.agents/skills/antigravity-expert-claude/SKILL.md` |
| MinerU / trích xuất PDF-ảnh-DOCX-PPTX-XLSX sang Markdown/JSON / OCR / layout detection mã nguồn mở | `.agents/skills/mineru-expert/SKILL.md` |
| Google Document AI / Document AI Cloud / Form Parser / Layout Parser / Custom Extractor (Google) | `.agents/skills/google-document-ai-expert/SKILL.md` |
| Google NotebookLM / Audio Overview / Mind Map / Slide Deck (NotebookLM) | `.agents/skills/notebooklm-expert/SKILL.md` |
| Tạo/cập nhật một expert skill từ URL trang docs bất kỳ | `.agents/skills/docs-to-expert/SKILL.md` |

## 2. ENFORCEMENT (thay hook — các ràng buộc bắt buộc của kit này)

- **Không tự bịa câu trả lời chuyên môn.** Nếu không tìm thấy expert phù hợp và không có trang docs chính thức nào xác minh được, phải nói rõ giới hạn thay vì suy đoán từ pretrain.
- **Không tạo expert mới từ nguồn không chính thức.** Chỉ tạo qua `docs-to-expert` khi domain trang nguồn thuộc chính nhà cung cấp/tổ chức của công nghệ đó (không phải blog cá nhân, diễn đàn, tutorial bên thứ ba).
- **Luôn kiểm tra CẢ HAI registry** (`.agents/skills/ask-expert/references/expert-registry.md` tĩnh + `.agents/expert-skills-registry.md` động) trước khi kết luận "chưa có expert", tránh tạo trùng.
- **`auto_create_expert: false`** (mặc định). Khi `false`, luôn hỏi xác nhận người dùng trước khi điều phối `docs-to-expert` tạo expert mới (nêu URL + tên skill dự kiến). Đổi thành `true` ở dòng này nếu muốn tự động tạo không cần hỏi — bước xác minh nguồn chính thức ở trên vẫn luôn bắt buộc dù cờ này là gì.

## 3. CHECKLIST trước khi trả lời

1. Câu hỏi có thuộc một domain chuyên môn cụ thể không? Nếu không, trả lời bình thường, bỏ qua checklist này.
2. Đã tra cả hai registry (tĩnh + động) chưa?
3. Nếu route sang một expert: đã để expert đó tự đọc `references/` của chính nó chưa (không tự đọc thay)?
4. Nếu tạo expert mới: đã xác minh domain nguồn là tài liệu chính thức, và đã tuân thủ `auto_create_expert` (hỏi xác nhận nếu `false`) chưa?
