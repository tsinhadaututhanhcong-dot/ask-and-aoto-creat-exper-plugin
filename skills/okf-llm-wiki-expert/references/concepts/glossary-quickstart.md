---
type: Reference
title: Bảng thuật ngữ và quickstart 10 phút
description: Tra nhanh mọi thuật ngữ OKF LLM-wiki, và một hướng dẫn cầm tay chỉ việc để dựng một OKF bundle tối thiểu chạy được trong 10 phút cho người mới hoàn toàn.
tags:
  - okf
  - glossary
  - quickstart
  - beginner
timestamp: 2026-07-03T00:00:00Z
source: Định nghĩa bám theo source-okf-spec-v0.1.md và source-llm-wiki-gist.md cùng thư mục.
---

# Bảng thuật ngữ và quickstart 10 phút

Dành cho người mới: đọc phần A để nắm từ vựng, làm theo phần B để có ngay một bundle chạy được.

## Phần A - Bảng thuật ngữ

- OKF (Open Knowledge Format): định dạng mở, biểu diễn tri thức bằng một thư mục file markdown có YAML frontmatter.
- LLM-wiki: mẫu hình để LLM tăng dần xây và bảo trì một cuốn wiki bền vững thay vì truy hồi tài liệu thô mỗi lần hỏi.
- Knowledge Bundle: một tập hợp tri thức khép kín, phân cấp; đơn vị phân phối của OKF.
- Concept: một đơn vị tri thức, biểu diễn bằng đúng một file markdown.
- Concept ID: đường dẫn file trong bundle sau khi bỏ đuôi `.md` (ví dụ `tables/users.md` cho ID `tables/users`).
- Frontmatter: khối metadata YAML giữa hai dòng `---` ở đầu file.
- `type`: trường bắt buộc duy nhất của mỗi concept; cho biết đây là loại concept gì.
- `index.md`: file mục lục một thư mục, phục vụ progressive disclosure; không có frontmatter (trừ `okf_version` ở gốc).
- `log.md`: nhật ký thay đổi theo ngày ISO 8601, mới nhất trước.
- Link (absolute bundle-relative): bắt đầu bằng `/`, hiểu từ gốc bundle; dạng khuyến nghị. Link relative: đường dẫn markdown tương đối thường.
- Citation: link từ concept tới nguồn ngoài, liệt kê dưới heading `# Citations`.
- Ingest: nạp một nguồn mới; LLM đọc, tóm tắt, cập nhật các trang liên quan, ghi log.
- Query: hỏi wiki; LLM đọc index, tổng hợp câu trả lời có trích dẫn, có thể file lại thành trang mới.
- Lint: rà soát sức khỏe wiki - mâu thuẫn, trang cũ, orphan, khoảng trống.
- Schema file: file cấu hình (`CLAUDE.md` hoặc `AGENTS.md`) quy định cấu trúc, quy ước, và workflow cho agent.
- Enrichment agent: công cụ tự động sinh hoặc làm giàu một OKF bundle từ nguồn dữ liệu.
- Progressive disclosure: cho người hoặc agent thấy cái gì đang có (qua index) trước khi mở từng tài liệu.
- Conformance: một bundle hợp lệ OKF v0.1 khi mọi concept có frontmatter phân tích được và có `type` khác rỗng.
- RAG: truy hồi các mẩu văn bản theo tương đồng vector lúc hỏi.
- GraphRAG: trích xuất đồ thị tri thức từ tài liệu và truy vấn theo đồ thị.
- Memex: khái niệm kho tri thức cá nhân của Vannevar Bush (1945), tiền thân tinh thần của LLM-wiki.

## Phần B - Quickstart 10 phút

Bạn không cần gì ngoài một trình soạn thảo và một LLM agent. Làm 5 bước sau.

### 1. Tạo cây thư mục

```
hello-okf/
├── CLAUDE.md
├── raw/
└── wiki/
    ├── index.md
    └── tables/
        ├── orders.md
        └── customers.md
```

### 2. Viết concept đầu tiên

`wiki/tables/orders.md`:

```markdown
---
type: BigQuery Table
title: Orders
description: Một dòng cho mỗi đơn hàng hoàn tất.
tags: [sales, orders]
timestamp: 2026-07-03T00:00:00Z
---

# Schema

| Column        | Type    | Description                                   |
|---------------|---------|-----------------------------------------------|
| `order_id`    | STRING  | Mã đơn hàng duy nhất.                          |
| `customer_id` | STRING  | Khóa ngoại tới [customers](/tables/customers.md). |

Thuộc về bảng [customers](/tables/customers.md).
```

Viết `customers.md` tương tự với vài cột và một link trỏ ngược về `/tables/orders.md`.

### 3. Viết index.md

`wiki/index.md` (không frontmatter):

```markdown
# Tables

* [Orders](tables/orders.md) - một dòng cho mỗi đơn hàng hoàn tất.
* [Customers](tables/customers.md) - một dòng cho mỗi khách hàng.
```

### 4. Viết một schema tối giản

`CLAUDE.md`:

```markdown
# CLAUDE.md
Đây là một OKF LLM-wiki. raw/ là nguồn thô bất biến; wiki/ là bundle tôi
sở hữu. Mỗi concept có frontmatter với type bắt buộc.

INGEST: đọc nguồn trong raw/, viết tóm tắt, cập nhật các concept và index,
ghi một dòng log.
QUERY: đọc wiki/index.md trước, rồi drill vào trang liên quan, trả lời có
trích dẫn.
LINT: tìm mâu thuẫn, trang mồ côi, khẳng định cũ, cross-reference thiếu.
```

### 5. Vòng ingest đầu tiên

Thả một file nguồn vào `raw/`, rồi bảo agent: "Ingest nguồn mới trong raw/ theo CLAUDE.md." Kiểm tra các trang được cập nhật, chỉnh schema nếu thấy thiếu quy ước. Xong. Bạn vừa có một OKF LLM-wiki chạy được.

## Đi tiếp

- [design-playbook](design-playbook.md) - dựng hệ thống hoàn chỉnh, mạnh mẽ.
- [okf-spec-explained](okf-spec-explained.md) - tra chuẩn khi cần chính xác.
