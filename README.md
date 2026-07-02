# expert-skills

Plugin điều phối chuyên gia tra cứu tài liệu chuyên môn cho Claude Code (và Google Antigravity 2.0). Route câu hỏi kỹ thuật tới đúng "expert skill" đã có; nếu chưa có ai phù hợp, tự tìm và xác minh trang tài liệu chính thức rồi tạo expert mới.

## Cách hoạt động

```
Câu hỏi chuyên môn
      │
      ▼
  ask-expert (skill tự trigger, hoặc /ask-expert tường minh)
      │
      ├── Có expert phù hợp trong registry? ──► route sang đúng expert (Skill tool)
      │                                          expert tự đọc references/ của nó và trả lời
      │
      └── Chưa có expert nào phù hợp?
                │
                ▼
          WebSearch + WebFetch tìm & xác minh trang docs CHÍNH THỨC
                │
                ▼
          Hỏi xác nhận người dùng (trừ khi auto_create_expert: true)
                │
                ▼
          docs-to-expert tạo expert mới tại ~/.claude/skills/<tên>/
                │
                ▼
          Ghi vào ~/.claude/expert-skills-registry.md, rồi route sang expert vừa tạo
```

## Thành phần

| Loại | Tên | Vai trò |
|---|---|---|
| Skill | `ask-expert` | Router: tra registry, route sang expert phù hợp hoặc điều phối tạo mới |
| Skill | `docs-to-expert` | Orchestrator tạo/cập nhật một expert skill từ URL trang docs (llms.txt ưu tiên, cào HTML/JS-rendered dự phòng) |
| Skill | `claude-expert` | Wiki 372 trang: hệ sinh thái Claude (CLI/Desktop/VS Code/JetBrains/Web/Agent SDK/enterprise providers) |
| Skill | `antigravity-expert-claude` | Wiki 88 trang: Google Antigravity (2.0 desktop/IDE/CLI/SDK) |
| Skill | `mineru-expert` | Wiki 50 trang: MinerU — công cụ phân tích tài liệu/OCR mã nguồn mở |
| Skill | `google-document-ai-expert` | Wiki 30 trang: Google Document AI (Cloud) |
| Skill | `notebooklm-expert` | Wiki 22 trang: Google NotebookLM + 17 file từ repo cộng đồng `notebooklm-mcp-cli` (cài đặt/dùng NotebookLM qua CLI/MCP server) |
| Command | `/ask-expert [câu hỏi]` | Lối vào tường minh cho router — dùng khi cần chắc chắn logic route chạy (vd agent khác gọi để lấy ngữ cảnh) |

Chi tiết từng expert (domain, độ phủ, root URL gốc) xem `skills/ask-expert/references/expert-registry.md`.

### Bổ sung nguồn từ repo GitHub

Một expert có thể cần cả tài liệu chính thức lẫn tài liệu của một công cụ liên quan chỉ tồn tại ở dạng repo (vd MCP server/CLI cộng đồng). `docs-to-expert` hỗ trợ ingest thêm nguồn này bằng `fetch_repo_docs.py` (README + `docs/` + file gợi ý là định nghĩa tool/schema) — nhưng **chỉ khi người dùng chỉ định đích danh URL repo**, không bao giờ tự động tìm/chọn repo (khác với việc tự tìm trang docs chính thức). Xem mục "Bổ sung nguồn từ GitHub repo" trong `skills/docs-to-expert/SKILL.md`.

## Cài đặt

```bash
/plugin install expert-skills@expert-skills
```

Hoặc dùng trực tiếp để phát triển/thử nghiệm:

```bash
claude --plugin-dir /path/to/expert-skills-plugin
```

## Cấu hình (tuỳ chọn)

Tạo `.claude/expert-skills.local.md` trong project để tuỳ chỉnh hành vi router:

```markdown
---
auto_create_expert: false
---
```

- `auto_create_expert: false` (mặc định nếu không có file) — `ask-expert` luôn hỏi xác nhận trước khi tạo expert mới (nêu rõ URL, tên skill dự kiến).
- `auto_create_expert: true` — tự động tạo expert mới ngay khi xác minh được nguồn chính thức, không cần hỏi thêm. Bước xác minh "trang docs chính thức" luôn bắt buộc dù bật cờ này hay không.

Sau khi sửa, khởi động lại Claude Code (`claude`) để cấu hình có hiệu lực.

## Đa nền tảng (Claude Code + Google Antigravity 2.0)

Plugin này target cả hai nền tảng. Thư mục `.agents/` chứa bản dùng trên Antigravity 2.0 (skill portable nguyên trạng; `/ask-expert` trở thành workflow `.agents/workflows/ask-expert.md`; routing/enforcement chính nằm ở `GEMINI.md` Rule).

## Nguồn gốc

`docs-to-expert` và 5 expert ban đầu được phát triển tại `E:\skills\expert-skills` (máy cá nhân của tác giả) trước khi đóng gói thành plugin này; `docs-to-expert` có repo riêng tại `github.com/twainkhux-max/docs-to-expert`. Nội dung trong plugin là bản copy độc lập, đường dẫn đã sửa dùng `${CLAUDE_PLUGIN_ROOT}` để portable — không phụ thuộc vị trí máy cá nhân.

## License

MIT
