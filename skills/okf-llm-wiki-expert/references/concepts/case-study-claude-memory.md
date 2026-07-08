---
type: Concept
title: Case study - hệ thống memory của Claude Code là một LLM-wiki sống
description: Đối chiếu hệ thống bộ nhớ của chính Claude Code (memory/ với MEMORY.md làm chỉ mục, mỗi ghi nhớ một file, liên kết [[tên]]) với mẫu hình OKF LLM-wiki, chứng minh mẫu hình chạy được trong sản xuất.
tags:
  - llm-wiki
  - claude-code
  - case-study
  - memory
timestamp: 2026-07-03T00:00:00Z
source: Quan sát trực tiếp thư mục memory của phiên làm việc Claude Code ngày 2026-07-03.
---

# Case study - hệ thống memory của Claude Code là một LLM-wiki sống

Đây là ví dụ dạy học rẻ nhất và thuyết phục nhất trong cả expert, vì nó là một hiện thân sống, kiểm tra được ngay trên đĩa, và bạn đang dùng nó lúc này. Hệ thống bộ nhớ bền vững của Claude Code chính là một hiện thực gần như trọn vẹn của mẫu hình [LLM-wiki](llm-wiki-concept.md).

## Bằng chứng trực tiếp từ phiên này

Thư mục memory của phiên hiện có bốn file:

```
memory/
├── MEMORY.md                      # chỉ mục
├── project_rag_research_start.md
├── okf-llm-wiki-expert.md
└── truy-vet-url-tan-cung.md
```

Ngay trong phiên làm việc này, hệ thống đã thực hiện đủ ba thao tác của một LLM-wiki: ghi hai ghi nhớ mới (okf-llm-wiki-expert và truy-vet-url-tan-cung), liên kết chúng bằng `[[tên]]`, cập nhật `MEMORY.md`, và sửa một dòng cũ đã lỗi thời cho khỏi sai lệch. Đó không phải mô phỏng; đó là mẫu hình đang chạy.

## Phép ánh xạ sang OKF LLM-wiki

| Bộ phận trong Claude Code memory | Tương ứng trong OKF LLM-wiki |
|---|---|
| Thư mục `memory/` | Bundle (kho tri thức) |
| `MEMORY.md` (một dòng mỗi ghi nhớ, có link) | `index.md` - mục lục, progressive disclosure |
| Mỗi file `<slug>.md` | Một concept (một file, một đơn vị tri thức) |
| Frontmatter `name`, `description`, `metadata.type` | Frontmatter OKF; `metadata.type` đóng vai trường `type` |
| Giá trị type `user`/`feedback`/`project`/`reference` | Từ vựng type tự chọn (giống Google chỉ dùng vài type) |
| Liên kết `[[tên]]` giữa các ghi nhớ | Cross-link giữa concept (quan hệ diễn đạt bằng văn cảnh) |
| Trường `description` dùng để chấm độ liên quan khi recall | Truy xuất index-first: đọc mục lục trước rồi khoan sâu |

## Ba thao tác ánh xạ trực tiếp

- Ingest: viết một ghi nhớ mới (một file, một fact) rồi thêm một dòng vào `MEMORY.md`. Đúng như một OKF concept mới cộng cập nhật index.
- Query: khi cần, hệ thống nạp `MEMORY.md` như ngữ cảnh nền, dùng `description` để tìm ghi nhớ liên quan rồi đọc file cụ thể. Đúng tinh thần progressive disclosure của [OKF spec](okf-spec-explained.md).
- Lint: quy tắc yêu cầu kiểm tra file đã có trước khi tạo trùng, cập nhật file thay vì nhân bản, và xóa ghi nhớ sai. Việc sửa một dòng lỗi thời trong phiên này chính là một thao tác lint thu nhỏ.

## Những chỗ chưa trọn vẹn OKF

Đây là một LLM-wiki đúng nghĩa nhưng chưa tuân thủ OKF một cách hình thức:

- Trường bắt buộc của OKF là `type` ở cấp cao nhất của frontmatter; Claude Code đặt nó ở `metadata.type`. Về mặt cấu trúc tương đương, nhưng không khớp §9 conformance của spec.
- `MEMORY.md` là chỉ mục nhưng dùng schema riêng, không phải đúng dạng `index.md` của OKF.
- Phạm vi là ca dùng personal (kho tri thức cá nhân do agent bảo trì xuyên phiên), đúng một trong các bối cảnh mà [llm-wiki-concept](llm-wiki-concept.md) liệt kê.

Những khác biệt này không làm giảm giá trị bài học: về bản chất, đây là cùng một mẫu hình, và nó đang phục vụ bạn thật.

## Bài học cho người thiết kế

- Mẫu hình LLM-wiki không phải lý thuyết: một sản phẩm đang chạy (Claude Code) đã hiện thực nó và bạn hưởng lợi mỗi phiên.
- Bạn có thể nghiên cứu chính hệ thống này như một template: một chỉ mục, mỗi tri thức một file, liên kết chéo, cộng luật bảo trì rõ ràng. Đó gần như đúng công thức trong [design-playbook](design-playbook.md).
- Nếu muốn nghiêm ngặt OKF, chỉ cần nâng `metadata.type` lên `type` cấp cao nhất và cho `MEMORY.md` theo dạng `index.md`, là kho memory trở thành một OKF bundle hợp lệ.

## Xem thêm

- [llm-wiki-concept](llm-wiki-concept.md) - mẫu hình gốc.
- [ecosystem-and-tooling](ecosystem-and-tooling.md) - các hiện thân khác (trip2g, RightMemory).
- [real-okf-bundle-and-agent](real-okf-bundle-and-agent.md) - một gói OKF sản xuất thật để đối chiếu.
