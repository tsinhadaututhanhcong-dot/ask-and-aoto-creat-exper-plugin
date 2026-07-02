# Expert Registry (bundled)

Danh sách expert skill đi kèm sẵn trong plugin `expert-skills` (nằm tại `${CLAUDE_PLUGIN_ROOT}/skills/<tên>/`). Đây là registry **tĩnh**, chỉ ghi các expert đóng gói cùng plugin lúc cài đặt — KHÔNG bao gồm expert được tạo mới sau này qua `docs-to-expert` (những expert đó nằm ở `~/.claude/skills/` và được track trong `~/.claude/expert-skills-registry.md`, xem skill `ask-expert`).

| Skill | Domain / từ khoá | Root URL gốc | Số trang | Độ phủ | Nguồn bổ sung |
|---|---|---|---|---|---|
| `claude-expert` | Toàn bộ hệ sinh thái Claude: CLI, Desktop, VS Code, JetBrains, Web, Agent SDK, Bedrock/Vertex AI/Foundry | code.claude.com/docs | 372 | Sâu | — |
| `antigravity-expert-claude` | Google Antigravity: 4 sản phẩm (2.0 desktop, IDE, CLI, SDK) | antigravity.google/docs/home | 88 | Sâu | — |
| `mineru-expert` | MinerU — công cụ phân tích tài liệu mã nguồn mở (PDF/ảnh scan/DOCX/PPTX/XLSX → Markdown/JSON, OCR, layout detection) | opendatalab.github.io/MinerU | 50 | Sâu | — |
| `google-document-ai-expert` | Google Document AI (Cloud) — số hóa & trích xuất dữ liệu có cấu trúc từ tài liệu (OCR, Form Parser, Layout Parser, Custom Extractor, processor huấn luyện sẵn) | docs.cloud.google.com/document-ai/docs | 30 | Trung bình | — |
| `notebooklm-expert` | Google NotebookLM — trợ lý nghiên cứu/tổng hợp tài liệu bằng AI (nạp nguồn, chat có trích dẫn, Audio/Video Overview, Mind Map, Slide Deck); kèm hướng dẫn dùng qua CLI/MCP server (`notebooklm-mcp-cli`) | support.google.com/notebooklm | 22 | Trung bình | repo `jacob-bd/notebooklm-mcp-cli` (17 file, cộng đồng — xem `references/INDEX.md` mục "Nguồn bổ sung") |

**Cách đọc cột "Độ phủ":**
- **Sâu** (≥50 trang): trả lời được câu hỏi chi tiết, API reference, cấu hình nâng cao.
- **Trung bình** (15-49 trang): trả lời tốt câu hỏi tổng quan/thường gặp; câu hỏi rất sâu (API reference đầy đủ, edge case hiếm) có thể thiếu — nếu không tìm thấy trong `references/`, đề xuất gọi lại `docs-to-expert --update` để đào sâu thêm thay vì suy đoán.

**Cách đọc cột "Nguồn bổ sung":** ngoài tài liệu chính thức, một expert có thể có thêm nguồn phi-chính-thức (thường là repo GitHub của một công cụ liên quan) do người dùng **chỉ định tường minh** khi thấy cần (không phải do `ask-expert`/`docs-to-expert` tự ý tìm — xem quy tắc tin cậy trong `docs-to-expert/SKILL.md` mục "Bổ sung nguồn từ GitHub repo"). Khi trả lời, luôn phân biệt rõ nguồn chính thức và nguồn bổ sung, không lẫn lộn.
