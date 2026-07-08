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
effort: medium
---

# Ask Expert — Router chuyên gia đa domain

## Vai trò

`ask-expert` không tự biết bất kỳ tri thức chuyên môn nào. Việc duy nhất nó làm là: **tra cứu xem đã có expert skill phù hợp chưa rồi route sang đúng expert đó**, hoặc nếu chưa có ai phù hợp thì **xác minh nguồn tài liệu chính thức rồi điều phối `docs-to-expert` tạo expert mới rồi route sang expert vừa tạo**.

## Xác định thư mục gốc (Plugin Root)

Tệp SKILL.md này nằm tại `<plugin_root>/skills/ask-expert/SKILL.md`. Để xác định thư mục gốc chứa tất cả chuyên gia, lùi 2 cấp thư mục từ vị trí tệp đang đọc. Ví dụ: nếu tệp đang ở `E:\skills\expert-skills-plugin\.agents\skills\ask-expert\SKILL.md` thì thư mục gốc chuyên gia là `E:\skills\expert-skills-plugin\.agents\skills\`.

Ký hiệu `<skills_root>` trong tài liệu này luôn chỉ đến thư mục gốc đó. Mọi chuyên gia đều nằm trong `<skills_root>/<tên_expert>/`.

## Registry chuyên gia

Tệp `references/expert-registry.md` (nằm cạnh SKILL.md này) liệt kê toàn bộ chuyên gia đã có - kể cả chuyên gia đi kèm lúc cài đặt lẫn chuyên gia tạo thêm sau đó. Đây là nguồn tra cứu nhanh duy nhất. Mỗi khi tạo thêm chuyên gia mới, ghi bổ sung trực tiếp vào tệp này.

## Gotchas

| Cách làm sai | Cách làm đúng |
|---|---|
| Không tìm thấy expert phù hợp rồi tự trả lời bằng kiến thức pretrain. | Báo rõ "chưa có expert cho domain này", đề xuất tạo mới qua `docs-to-expert` (xin xác nhận nếu cần) thay vì bịa câu trả lời. |
| Tạo expert mới từ một trang không chính thức (blog cá nhân, tutorial bên thứ ba, Stack Overflow, Reddit, bài báo tin tức). | Chỉ tạo expert từ trang có domain thuộc chính nhà cung cấp/tổ chức của công nghệ đó (vd `docs.*`, `developer.*`, domain sản phẩm chính thức, `github.io` của chính tổ chức gốc, `readthedocs.io` chính chủ dự án). Nếu không chắc, hỏi người dùng xác nhận thay vì tự quyết. |
| Gọi lại `docs-to-expert` tạo một expert đã tồn tại (trùng domain, khác tên một chút). | Luôn đọc registry trước, so khớp domain/từ khoá kỹ trước khi kết luận "chưa có expert". |
| Route sang một expert có độ phủ mỏng rồi coi câu trả lời của nó là đầy đủ, không cảnh báo gì. | Đọc cột "Độ phủ" trong registry - nếu "Trung bình" và câu hỏi cần chi tiết sâu (API reference đầy đủ, edge case hiếm), nói rõ giới hạn và đề xuất `docs-to-expert --update` để đào sâu thêm. |

## Cây quyết định

**Bước 0 - Có thật sự cần một expert domain cụ thể không?** Câu hỏi lập trình chung chung, không gắn với một công nghệ/sản phẩm cụ thể nào thì không cần route, trả lời bình thường (không dùng skill này).

**Bước 1 - Tra registry:** Đọc tệp `references/expert-registry.md`, so khớp domain/từ khoá câu hỏi với cột "Domain / từ khoá" của từng expert.

**Bước 2 - Đã tìm thấy expert phù hợp:**
- Xác định đường dẫn thư mục chuyên gia: `<skills_root>/<tên_expert>/`.
- Đọc tệp `SKILL.md` của chuyên gia đó và làm theo đúng cây quyết định trong đó để trả lời câu hỏi gốc của người dùng.
- Mỗi expert tự đọc `references/index.md` rồi đọc tiếp các tệp concept tương ứng trong `references/concepts/` - không tự đọc thay nó vì mỗi expert có cây quyết định riêng, đã tối ưu cho domain của nó.
- Nếu expert trả về tín hiệu WIKI_NOT_FOUND/WIKI_INSUFFICIENT, hoặc độ phủ ghi "Trung bình" và câu hỏi rõ ràng cần sâu hơn, chuyển sang **chế độ cập nhật**: dùng luôn cột "Root URL gốc" đã có sẵn trong registry cho expert này rồi đọc tệp `<skills_root>/docs-to-expert/SKILL.md` và làm theo quy trình cập nhật kèm cờ `--update`.

**Bước 3 - Chưa có expert phù hợp (tạo mới):**
1. Tìm trang tài liệu liên quan bằng tìm kiếm web, ưu tiên kết quả có domain thuộc chính nhà cung cấp công nghệ đó.
2. Truy cập URL kết quả để xác minh: đây thật sự là trang tài liệu kỹ thuật chính thức (không phải trang marketing, blog cá nhân, diễn đàn, hay bài tổng hợp bên thứ ba). Kiểm tra domain khớp với sản phẩm/tổ chức đang hỏi.
3. Luôn hỏi xác nhận người dùng trước khi tạo: nêu rõ URL đã tìm thấy, tên skill dự kiến (kebab-case), và việc này sẽ tốn thời gian cùng cần mạng.
4. Sau khi được xác nhận: đọc tệp `<skills_root>/docs-to-expert/SKILL.md` và làm theo đúng quy trình trong đó với `<root_url>` + `<skill_name>`. Chuyên gia mới sẽ được tạo tại `<skills_root>/<skill_name>/`.
5. Sau khi `docs-to-expert` chạy xong: thêm một dòng vào `references/expert-registry.md` ghi tên skill, domain/từ khoá, root URL, số trang, ngày tạo.
6. Đọc SKILL.md của expert vừa tạo và làm theo để trả lời câu hỏi gốc của người dùng.

**Bước 4 - Agent khác hỏi để lấy ngữ cảnh:** Trả về đúng cấu trúc dữ liệu được yêu cầu, kèm tên expert đã dùng làm nguồn (để agent gọi có thể trích dẫn).

## Định dạng dòng registry

Khi thêm expert mới vào `references/expert-registry.md`, dùng đúng định dạng bảng markdown đã có sẵn:

```markdown
| <skill_name> | <mô tả ngắn domain> | <root_url> | <N> | <Độ phủ> | — |
```

## Triết lý cốt lõi

*Không tự bịa câu trả lời chuyên môn khi chưa xác định được nguồn. Không tạo expert từ nguồn không chính thức. Luôn kiểm tra registry trước khi tạo mới để tránh trùng lặp.*
