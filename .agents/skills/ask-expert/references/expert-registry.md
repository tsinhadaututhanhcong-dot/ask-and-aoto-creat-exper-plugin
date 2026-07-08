# Expert Registry

Danh sách toàn bộ expert skill trong plugin `expert-skills`. Mỗi expert nằm tại `<skills_root>/<tên>/`. Registry này là nguồn tra cứu nhanh duy nhất - khi tạo thêm chuyên gia mới qua `docs-to-expert`, ghi bổ sung trực tiếp vào bảng bên dưới.

| Skill | Domain / từ khoá | Root URL gốc | Số trang | Độ phủ | Nguồn bổ sung |
|---|---|---|---|---|---|
| `claude-expert` | Toàn bộ hệ sinh thái Claude: CLI, Desktop, VS Code, JetBrains, Web, Agent SDK, Bedrock/Vertex AI/Foundry | code.claude.com/docs | 372 | Sâu | — |
| `antigravity-expert-claude` | Google Antigravity: 4 sản phẩm (2.0 desktop, IDE, CLI, SDK) | antigravity.google/docs/home | 88 | Sâu | — |
| `antigravity-expert` | Google Antigravity: hướng dẫn tổng quan, cài đặt, cấu hình, debug; kèm nghiên cứu gói cước AI Ultra | Tài liệu nội bộ | 56 | Trung bình | Báo cáo nghiên cứu Google AI Ultra (2026-07-06) |
| `mineru-expert` | MinerU - công cụ phân tích tài liệu mã nguồn mở (PDF/ảnh scan/DOCX/PPTX/XLSX sang Markdown/JSON, OCR, layout detection) | opendatalab.github.io/MinerU | 50 | Sâu | — |
| `google-document-ai-expert` | Google Document AI (Cloud) - số hóa và trích xuất dữ liệu có cấu trúc từ tài liệu (OCR, Form Parser, Layout Parser, Custom Extractor, processor huấn luyện sẵn) | docs.cloud.google.com/document-ai/docs | 30 | Trung bình | — |
| `notebooklm-expert` | Google NotebookLM - trợ lý nghiên cứu/tổng hợp tài liệu bằng AI (nạp nguồn, chat có trích dẫn, Audio/Video Overview, Mind Map, Slide Deck); kèm hướng dẫn dùng qua CLI/MCP server (`notebooklm-mcp-cli`) | support.google.com/notebooklm | 22 | Trung bình | repo `jacob-bd/notebooklm-mcp-cli` (17 file, cộng đồng) |
| `nlm-mcp-expert` | notebooklm-mcp-cli - công cụ CLI/MCP điều khiển Google NotebookLM (upload, query, tạo audio/video studio) | repo jacob-bd/notebooklm-mcp-cli | 17 | Trung bình | — |
| `okf-llm-wiki-expert` | OKF (Open Knowledge Format) của Google và mẫu hình LLM-wiki của Karpathy - kiến trúc ba lớp, ba thao tác ingest/query/lint, đối chiếu RAG/GraphRAG | Tài liệu nội bộ | 15 | Trung bình | — |
| `hermes-expert` | Hermes Agent - framework xây dựng agent đa nền tảng, quản lý bộ nhớ, công cụ, MCP, tích hợp Telegram/Discord, lập lịch, sandbox | hermes-agent.nousresearch.com | 366 | Sâu | — |

**Cách đọc cột "Độ phủ":**
- **Sâu** (50 trang trở lên): trả lời được câu hỏi chi tiết, API reference, cấu hình nâng cao.
- **Trung bình** (15-49 trang): trả lời tốt câu hỏi tổng quan/thường gặp; câu hỏi rất sâu (API reference đầy đủ, edge case hiếm) có thể thiếu - nếu không tìm thấy trong `references/`, đề xuất gọi lại `docs-to-expert --update` để đào sâu thêm thay vì suy đoán.

**Cách đọc cột "Nguồn bổ sung":** ngoài tài liệu chính thức, một expert có thể có thêm nguồn phi-chính-thức (thường là repo GitHub của một công cụ liên quan) do người dùng **chỉ định tường minh** khi thấy cần (không phải do `ask-expert`/`docs-to-expert` tự ý tìm - xem quy tắc tin cậy trong `docs-to-expert/SKILL.md` mục "Bổ sung nguồn từ GitHub repo"). Khi trả lời, luôn phân biệt rõ nguồn chính thức và nguồn bổ sung, không lẫn lộn.
