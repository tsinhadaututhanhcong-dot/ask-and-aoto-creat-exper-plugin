---
name: ask-expert
description: >
  Điều phối viên (router) cho các câu hỏi chuyên môn/kỹ thuật thuộc một domain cụ thể (framework, SDK, API, sản phẩm...).
  Tra registry expert đã có để route đúng chuyên gia trả lời; nếu chưa có expert nào phù hợp, tìm và xác minh trang
  tài liệu chính thức của domain đó rồi điều phối skill docs-to-expert tạo expert mới. Dùng cho cả người dùng lẫn agent khác.
when_to_use: >
  - Khi người dùng hỏi một câu hỏi kỹ thuật chuyên sâu về một công nghệ/framework/sản phẩm cụ thể mà không rõ có
    expert skill nào trả lời được hay chưa.
  - Khi một agent khác cần tra cứu thông tin chuyên môn về một domain cụ thể để lấy ngữ cảnh trước khi hành động.
  - Khi người dùng hỏi "ai biết về X", "có chuyên gia nào về X không", "tạo chuyên gia cho X đi".
  - Khi câu trả lời từ một expert đã có tỏ ra thiếu (expert báo WIKI_NOT_FOUND/WIKI_INSUFFICIENT, hoặc độ phủ trong
    registry ghi "Trung bình"/"Mỏng" và câu hỏi cần chi tiết sâu hơn mức đó).
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Skill, Write, Edit
effort: medium
---

# Ask Expert — Router chuyên gia đa domain

## Vai trò

`ask-expert` không tự biết bất kỳ tri thức chuyên môn nào. Việc duy nhất nó làm là: **tra cứu xem đã có expert skill phù hợp chưa → route sang đúng expert đó**, hoặc nếu chưa có ai phù hợp → **xác minh nguồn tài liệu chính thức → điều phối `docs-to-expert` tạo expert mới → route sang expert vừa tạo**.

## Hai lớp registry

1. **Registry đóng gói sẵn (tĩnh)** — `${CLAUDE_PLUGIN_ROOT}/skills/ask-expert/references/expert-registry.md`. Liệt kê các expert đi kèm plugin lúc cài đặt (claude-expert, antigravity-expert-claude, mineru-expert, google-document-ai-expert, notebooklm-expert). Không tự sửa file này lúc runtime — đây là nội dung do plugin author kiểm soát.
2. **Registry cá nhân (động)** — `~/.claude/expert-skills-registry.md` (đường dẫn tuyệt đối: `$env:USERPROFILE\.claude\expert-skills-registry.md` trên Windows, `~/.claude/expert-skills-registry.md` trên macOS/Linux). Ghi các expert được `docs-to-expert` tạo thêm SAU khi cài plugin — các expert này nằm ở `~/.claude/skills/<tên>/`, KHÔNG nằm trong `${CLAUDE_PLUGIN_ROOT}` (vì thư mục plugin cài đặt có thể bị ghi đè khi cập nhật plugin, không an toàn để ghi dữ liệu runtime vào đó). Nếu file chưa tồn tại, coi như registry cá nhân rỗng — không có gì phải đọc thêm.

## Gotchas

| CÁCH LÀM SAI | CÁCH LÀM ĐÚNG |
|---|---|
| Không tìm thấy expert phù hợp rồi tự trả lời bằng kiến thức pretrain. | Báo rõ "chưa có expert cho domain này", đề xuất tạo mới qua `docs-to-expert` (xin xác nhận nếu cần) thay vì bịa câu trả lời. |
| Tạo expert mới từ một trang không chính thức (blog cá nhân, tutorial bên thứ ba, Stack Overflow, Reddit, bài báo tin tức). | Chỉ tạo expert từ trang có domain thuộc chính nhà cung cấp/tổ chức của công nghệ đó (vd `docs.*`, `developer.*`, domain sản phẩm chính thức, `github.io` của chính tổ chức gốc, `readthedocs.io` chính chủ dự án). Nếu không chắc, hỏi người dùng xác nhận thay vì tự quyết. |
| Gọi lại `docs-to-expert` tạo một expert đã tồn tại (trùng domain, khác tên một chút). | Luôn đọc CẢ HAI registry (tĩnh + cá nhân) trước, so khớp domain/từ khoá kỹ trước khi kết luận "chưa có expert". |
| Route sang một expert có độ phủ mỏng rồi coi câu trả lời của nó là đầy đủ, không cảnh báo gì. | Đọc cột "Độ phủ" trong registry tĩnh — nếu "Trung bình" và câu hỏi cần chi tiết sâu (API reference đầy đủ, edge case hiếm), nói rõ giới hạn và đề xuất `docs-to-expert --update` để đào sâu thêm. |

## Cây quyết định

**Bước 0 — Có thật sự cần một expert domain cụ thể không?** Câu hỏi lập trình chung chung, không gắn với một công nghệ/sản phẩm cụ thể nào → không cần route, trả lời bình thường (không dùng skill này).

**Bước 1 — Tra registry tĩnh:** Đọc `${CLAUDE_PLUGIN_ROOT}/skills/ask-expert/references/expert-registry.md`, so khớp domain/từ khoá câu hỏi với cột "Domain / từ khoá" của từng expert.

**Bước 2 — Tra registry cá nhân:** Nếu Bước 1 không khớp, kiểm tra `~/.claude/expert-skills-registry.md` có tồn tại không (dùng `Glob` hoặc thử `Read`). Nếu có, so khớp tương tự. Nếu vẫn không khớp, coi như chưa có expert nào phù hợp.

**Bước 3 — Đã tìm thấy expert phù hợp:**
- Dùng `Skill` tool load đúng expert đó (tên skill lấy từ cột "Skill" trong registry) với câu hỏi gốc của người dùng.
- Để expert đó tự đọc `INDEX.md`/`concepts/` của chính nó và trả lời (không tự đọc thay nó — mỗi expert có cây quyết định riêng, đã tối ưu cho domain của nó).
- Nếu expert trả về tín hiệu `WIKI_NOT_FOUND`/`WIKI_INSUFFICIENT`, hoặc độ phủ ghi "Trung bình" và câu hỏi rõ ràng cần sâu hơn → chuyển sang **chế độ cập nhật**: làm theo các bước 3-6 của Bước 4 bên dưới, nhưng bỏ qua bước 1-2 (tìm/xác minh URL mới) — dùng luôn cột "Root URL gốc" đã có sẵn trong registry cho expert này (expert đã tồn tại nghĩa là nguồn đã được xác minh từ trước), và ở bước 4 gọi `docs-to-expert` kèm `--update` thay vì tạo mới.

**Bước 4 — Chưa có expert phù hợp (tạo mới):**
1. Tìm trang tài liệu liên quan bằng `WebSearch`, ưu tiên kết quả có domain thuộc chính nhà cung cấp công nghệ đó.
2. Dùng `WebFetch` xác minh: đây thật sự là trang tài liệu kỹ thuật chính thức (không phải trang marketing, blog cá nhân, diễn đàn, hay bài tổng hợp bên thứ ba). Kiểm tra domain khớp với sản phẩm/tổ chức đang hỏi.
3. Đọc `.claude/expert-skills.local.md` (nếu có) lấy field `auto_create_expert`:
   - Không có file, hoặc `auto_create_expert: false` (mặc định) → **luôn hỏi xác nhận người dùng** trước khi tạo: nêu rõ URL đã tìm thấy, tên skill dự kiến (kebab-case), và việc này sẽ tốn thời gian + cần mạng.
   - `auto_create_expert: true` → có thể tạo luôn không cần hỏi thêm, NHƯNG bước xác minh domain chính thức ở trên vẫn bắt buộc, không được bỏ qua.
4. Sau khi được xác nhận (hoặc auto_create_expert bật): dùng `Skill` tool load `docs-to-expert`, cung cấp `<root_url>` + `<skill_name>`.
5. Sau khi `docs-to-expert` chạy xong: nếu là **tạo mới** (expert mới tại `~/.claude/skills/<skill_name>/`), thêm một dòng vào `~/.claude/expert-skills-registry.md` (tạo file mới với header bảng nếu chưa tồn tại) ghi tên skill, domain/từ khoá, root URL, số trang, ngày tạo. Nếu là **cập nhật** một expert đã có sẵn trong registry tĩnh, không cần thêm dòng nào (registry tĩnh do plugin author kiểm soát, không tự sửa) — chỉ cần biết số trang mới đã tăng để trả lời chính xác hơn.
6. Dùng `Skill` tool load expert vừa tạo để trả lời câu hỏi gốc của người dùng.

**Bước 5 — Agent khác hỏi để lấy ngữ cảnh:** Trả về đúng cấu trúc dữ liệu được yêu cầu, kèm tên expert đã dùng làm nguồn (để agent gọi có thể trích dẫn).

## Định dạng dòng registry cá nhân

Khi thêm expert mới vào `~/.claude/expert-skills-registry.md`, dùng đúng định dạng bảng markdown giống registry tĩnh để dễ đọc lẫn nhau:

```markdown
# Expert Registry (cá nhân — tạo bởi ask-expert / docs-to-expert)

| Skill | Domain / từ khoá | Root URL gốc | Số trang | Ngày tạo |
|---|---|---|---|---|
| <skill_name> | <mô tả ngắn domain> | <root_url> | <N> | <YYYY-MM-DD> |
```

## Triết lý cốt lõi

*Không tự bịa câu trả lời chuyên môn khi chưa xác định được nguồn. Không tạo expert từ nguồn không chính thức. Luôn kiểm tra registry trước khi tạo mới để tránh trùng lặp.*
