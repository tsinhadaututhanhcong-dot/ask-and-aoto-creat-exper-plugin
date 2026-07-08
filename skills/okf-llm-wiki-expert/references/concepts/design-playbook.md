---
type: Playbook
title: Cẩm nang thiết kế hệ thống OKF LLM-wiki
description: Hướng dẫn thực hành từng bước để thiết kế và xây dựng một hệ thống OKF LLM-wiki hoàn chỉnh và mạnh mẽ từ con số không, cho người ở bất kỳ trình độ nào, kèm template CLAUDE.md và ví dụ xuyên suốt.
tags:
  - okf
  - llm-wiki
  - playbook
  - how-to
  - schema
timestamp: 2026-07-03T00:00:00Z
source: Tổng hợp từ source-okf-spec-v0.1.md và source-llm-wiki-gist.md cùng thư mục, biên soạn thành quy trình thực hành.
---

# Cẩm nang thiết kế hệ thống OKF LLM-wiki

Đây là file trung tâm của expert. Nếu bạn chỉ đọc một file, hãy đọc file này. Nó biến hai thứ trừu tượng - đặc tả [OKF](okf-spec-explained.md) và mẫu hình [LLM-wiki](llm-wiki-concept.md) - thành một quy trình bạn làm theo được, dù bạn là người mới hoàn toàn hay kỹ sư có kinh nghiệm.

## Phần A - Tư duy nền

Ghép hai mảnh lại: OKF là định dạng (cách xếp file trên đĩa), LLM-wiki là triết lý vận hành (ai làm gì, khi nào). Một hệ thống hoàn chỉnh gồm ba lớp cộng ba thao tác cộng một vòng bảo trì:

- Ba lớp: raw sources (nguồn thô bất biến), OKF bundle (wiki markdown có cấu trúc), schema file (cẩm nang vận hành cho agent).
- Ba thao tác: ingest (nạp nguồn), query (hỏi và tổng hợp), lint (rà soát sức khỏe).
- Vòng bảo trì: lặp ingest và query, xen kẽ lint, để wiki giàu dần mà không phân rã.

Nguyên tắc chỉ đường: con người tuyển nguồn và hỏi câu hỏi đúng; LLM làm mọi việc ghi chép sổ sách. Nếu bạn thấy mình đang tự tay sửa cross-reference, bạn đang làm sai vai.

## Phần B - Các bước thiết kế

### Bước 0 - Xác định phạm vi và chọn nền

Trả lời ba câu trước khi tạo file nào:

1. Miền là gì? Ví dụ: wiki nghiên cứu cổ phiếu cá nhân, catalog một dataset bán hàng, kho tri thức nội bộ một nhóm.
2. Nguồn thô đến từ đâu? Bài báo, báo cáo tài chính, bảng dữ liệu, transcript.
3. Ai tiêu thụ? Chỉ mình bạn, một agent, hay cả nhóm.

Chọn nền: một git repo chứa markdown là đủ và khuyến nghị (có version, branch, diff miễn phí). Tùy chọn mở thư mục wiki bằng Obsidian để xem graph view trong lúc LLM sửa.

### Bước 1 - Dựng khung ba lớp trên đĩa

Một bố cục khởi đầu gọn:

```
my-wiki/
├── CLAUDE.md              # Lớp schema: cẩm nang vận hành cho agent
├── raw/                   # Lớp nguồn thô, bất biến
│   └── (các file nguồn bạn thả vào đây)
└── wiki/                  # OKF bundle: nơi LLM viết
    ├── index.md
    ├── log.md
    ├── entities/
    ├── concepts/
    └── sources/
```

Quy tắc sắt: LLM chỉ đọc `raw/`, chỉ ghi `wiki/`. Không bao giờ để LLM sửa nguồn thô.

### Bước 2 - Thiết kế từ vựng type và taxonomy thư mục

Nhớ: trong OKF, `type` là trường bắt buộc duy nhất, và giá trị `type` do bạn tự đặt (không đăng ký tập trung). Hãy chọn một tập nhỏ, mô tả, nhất quán. Ví dụ cho wiki nghiên cứu:

| type            | Dùng cho                                   |
|-----------------|--------------------------------------------|
| `Source-Summary`| Tóm tắt một nguồn thô đã nạp.               |
| `Entity`        | Một thực thể (công ty, người, sản phẩm).    |
| `Concept`       | Một khái niệm hoặc chủ đề.                  |
| `Metric`        | Một chỉ số có định nghĩa và cách tính.       |
| `Playbook`      | Một quy trình hoặc runbook.                 |
| `Reference`     | Tài liệu tham chiếu ngoài.                  |

Lưu ý từ thực tế: trong gói OKF sản xuất của Google, metric không dùng type `Metric` riêng mà được lưu với `type: Reference` (gắn tag `metric`), và từ vựng type thực tế rất nhỏ. Xem [real-okf-bundle-and-agent](real-okf-bundle-and-agent.md). Chọn cách nào cũng được, miễn nhất quán.

Taxonomy thư mục phản ánh miền, không phải một khuôn áp đặt. Trong `wiki/`, `entities/` chứa `Entity`, `concepts/` chứa `Concept`, `sources/` chứa `Source-Summary`, và cứ thế.

### Bước 3 (then chốt) - Viết file schema

Đây là bước làm nên hoặc phá hỏng hệ thống. File schema (`CLAUDE.md`) là cẩm nang biến agent thành người bảo trì có kỷ luật. Dưới đây là một template đầy đủ bạn có thể chép và sửa:

```markdown
# CLAUDE.md - Cẩm nang vận hành wiki

Đây là một OKF LLM-wiki. Bạn là người bảo trì. Con người tuyển nguồn và
hỏi; bạn làm mọi việc đọc, viết, cross-reference, và ghi sổ.

## Cấu trúc
- `raw/` là nguồn thô, BẤT BIẾN. Chỉ đọc, không bao giờ sửa.
- `wiki/` là bundle OKF bạn sở hữu. Mọi file concept có frontmatter với
  trường `type` bắt buộc.
- `wiki/index.md` là mục lục; `wiki/log.md` là nhật ký theo ngày.

## Quy tắc frontmatter
Mỗi concept mở đầu bằng:
    ---
    type: <một trong: Source-Summary | Entity | Concept | Metric | Playbook | Reference>
    title: <tên hiển thị>
    description: <một câu>
    tags: [<tag>, ...]
    timestamp: <ISO 8601>
    ---

## Quy tắc liên kết
- Ưu tiên link bundle-relative bắt đầu bằng `/`, ví dụ [X](/entities/x.md).
- Quan hệ diễn đạt bằng văn cảnh quanh link, không gắn nhãn vào link.
- Link tới trang chưa tồn tại là chấp nhận được (tri thức chưa viết).

## Workflow INGEST (khi tôi thả nguồn mới vào raw/)
1. Đọc nguồn. Nêu 3 tới 5 điểm rút ra và chờ tôi xác nhận trọng tâm.
2. Viết một trang `Source-Summary` trong wiki/sources/.
3. Cập nhật hoặc tạo các trang Entity và Concept liên quan (thường 5 tới 15 trang).
4. Thêm cross-reference hai chiều giữa các trang liên quan.
5. Cập nhật wiki/index.md.
6. Ghi một dòng vào wiki/log.md dạng: ## [YYYY-MM-DD] ingest | <tên nguồn>

## Workflow QUERY (khi tôi hỏi)
1. Đọc wiki/index.md trước để tìm trang liên quan.
2. Đọc các trang đó, tổng hợp câu trả lời có trích dẫn tới file wiki.
3. Nếu câu trả lời có giá trị lâu dài, hỏi tôi có nên file nó thành trang
   mới trong wiki không.
4. Ghi một dòng query vào log nếu câu trả lời được file lại.

## Workflow LINT (khi tôi bảo rà soát)
Quét toàn wiki và báo cáo: mâu thuẫn giữa các trang; khẳng định cũ đã bị
nguồn mới thay thế; trang mồ côi không có link trỏ vào; khái niệm được nhắc
nhiều lần nhưng thiếu trang riêng; cross-reference thiếu; khoảng trống dữ
liệu nên tìm thêm nguồn. Đề xuất hành động, chờ tôi duyệt trước khi sửa.
```

Điểm mấu chốt: schema phải mô tả rõ cả ba workflow. Một wiki thiếu workflow lint sẽ phân rã khi lớn; thiếu workflow query rõ ràng sẽ khiến agent bỏ qua index và trả lời hời hợt.

### Bước 4 - Bootstrap với vài nguồn đầu

Thả 3 tới 5 nguồn vào `raw/` và chạy vòng ingest từng cái một. Giữ mình trong vòng lặp: đọc tóm tắt, kiểm tra trang được cập nhật, chỉnh schema khi phát hiện một quy ước còn thiếu (ví dụ bạn nhận ra cần thêm type `Event`). Giai đoạn này chính là lúc bạn và agent cùng tiến hóa schema.

### Bước 5 - Query và cộng dồn

Bắt đầu hỏi. Mỗi câu trả lời có giá trị lâu dài, hãy file lại thành trang wiki (một bảng so sánh, một phân tích, một mối liên hệ). Đây là cơ chế khiến khám phá của bạn cộng dồn thay vì tan vào chat.

### Bước 6 - Lint và bảo trì định kỳ

Sau mỗi vài lần ingest, chạy lint. Sửa mâu thuẫn, gộp trang trùng, viết trang cho khái niệm còn mồ côi. Xem chi tiết các bẫy ở [gotchas-and-critiques](gotchas-and-critiques.md).

### Bước 7 - Mở rộng khi quy mô tăng

Khi wiki vượt khoảng 100 nguồn, `index.md` không còn đủ. Lúc đó thêm hạ tầng:

- Search: một search engine markdown như `qmd` (BM25 cộng vector, LLM re-rank, có CLI và MCP server).
- Trực quan hóa: một bộ visualizer graph để thấy hình dạng wiki, hub và orphan.
- Chia sẻ nhiều agent: bọc wiki thành một MCP server để nhiều agent cùng dùng chung. Xem các bản triển khai ở [ecosystem-and-tooling](ecosystem-and-tooling.md).

## Phần C - Ví dụ xuyên suốt: catalog một dataset bán hàng

Đi hết từ khung tới một vòng ingest, một query, một lint, theo đúng ví dụ orders/customers của spec.

Bố cục:

```
sales-wiki/
├── CLAUDE.md
├── raw/
│   └── orders-schema-export.csv
└── wiki/
    ├── index.md
    ├── log.md
    └── tables/
        ├── orders.md
        └── customers.md
```

`wiki/tables/orders.md` sau vòng ingest đầu:

```markdown
---
type: BigQuery Table
title: Orders
description: Một dòng cho mỗi đơn hàng hoàn tất.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, orders, revenue]
timestamp: 2026-07-03T00:00:00Z
---

# Schema

| Column        | Type      | Description                                   |
|---------------|-----------|-----------------------------------------------|
| `order_id`    | STRING    | Mã đơn hàng duy nhất toàn cục.                 |
| `customer_id` | STRING    | Khóa ngoại tới [customers](/tables/customers.md). |
| `total_usd`   | NUMERIC   | Tổng đơn tính bằng USD.                        |

# Joins

Nối với [customers](/tables/customers.md) qua `customer_id`.
```

`wiki/index.md`:

```markdown
# Tables

* [Orders](tables/orders.md) - một dòng cho mỗi đơn hàng hoàn tất.
* [Customers](tables/customers.md) - một dòng cho mỗi khách hàng.
```

Một dòng `wiki/log.md`:

```markdown
## 2026-07-03
* **Creation**: Nạp orders-schema-export.csv, lập [orders](/tables/orders.md) và [customers](/tables/customers.md).
```

Một query mẫu: "Làm sao nối doanh thu với khách hàng?" Agent đọc index, mở orders và customers, trả lời rằng nối qua `customer_id`, trích dẫn cả hai trang. Nếu bạn thấy hữu ích lâu dài, agent file câu trả lời thành `wiki/concepts/revenue-by-customer.md`.

Một lint mẫu: agent phát hiện `customers.md` chưa có link trỏ ngược về `orders.md`, đề xuất thêm cross-reference hai chiều; phát hiện `total_usd` được nhắc nhưng chưa có trang `Metric` riêng, đề xuất tạo.

## Phần D - Checklist hệ thống hoàn chỉnh và mạnh mẽ

Đánh dấu đủ các mục sau nghĩa là hệ thống của bạn vững:

- Có đủ ba lớp: `raw/` bất biến, `wiki/` là bundle OKF, một file schema.
- Schema mô tả đủ ba workflow ingest, query, lint.
- Mọi concept có frontmatter với `type` khác rỗng (điều kiện tuân thủ OKF).
- `index.md` được cập nhật tự động ở mỗi ingest.
- `log.md` có tiền tố nhất quán để grep được.
- Quy ước link nhất quán, ưu tiên bundle-relative bắt đầu bằng `/`.
- Có vòng lint định kỳ, không để wiki phân rã.
- Có kế hoạch thêm search khi vượt khoảng 100 nguồn.
- Có chiến lược chống LLM sai: review khi ingest nhiều trang, lint đều đặn.

## Phần E - Các quyết định thiết kế và đánh đổi

- Có nên dùng RAG song song không? Có, cho phần đuôi dài. Xem [okf-vs-rag-graphrag](okf-vs-rag-graphrag.md).
- Các bẫy thường gặp và phê bình cộng đồng: xem [gotchas-and-critiques](gotchas-and-critiques.md).
- Muốn làm thử nhanh một bundle tối thiểu trong 10 phút: xem [glossary-quickstart](glossary-quickstart.md).
