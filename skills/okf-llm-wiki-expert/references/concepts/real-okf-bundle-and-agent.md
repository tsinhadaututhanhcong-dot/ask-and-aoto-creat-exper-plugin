---
type: Reference
title: Gói OKF thật và tác nhân làm giàu (mổ xẻ mã nguồn)
description: Mổ xẻ các gói mẫu OKF sản xuất thật và mã nguồn tác nhân làm giàu trong repo GoogleCloudPlatform/knowledge-catalog, kèm những bài học thực tế lệch so với đặc tả.
tags:
  - okf
  - reference-agent
  - sample-bundle
  - real-world
  - google-adk
timestamp: 2026-07-03T00:00:00Z
source: Trích từ repo GoogleCloudPlatform/knowledge-catalog (clone --depth 1 ngày 2026-07-03), thư mục okf/bundles và okf/src/reference_agent.
---

# Gói OKF thật và tác nhân làm giàu (mổ xẻ mã nguồn)

File này khác các concept diễn giải khác ở chỗ nó dựa trên mã nguồn và gói mẫu thật đã clone từ repo, không phải diễn giải từ README. Mục đích: cho bạn thấy một OKF bundle sản xuất trông ra sao ở quy mô thật, và tác nhân làm giàu thật hoạt động thế nào, để bạn thiết kế theo mẫu tốt nhất. Bổ sung cho [ecosystem-and-tooling](ecosystem-and-tooling.md) (vốn ở tầng mô tả).

## Phần A - Giải phẫu một gói OKF thật

Gói ga4 trong repo có cấu trúc: `datasets/`, `tables/`, và `references/` chia tiếp thành `joins/` và `metrics/`. Mỗi thư mục có `index.md` riêng. Ví dụ `index.md` gốc gói ga4 (thật):

```markdown
# Subdirectories

* [datasets](datasets/index.md) - A sample of obfuscated Google Analytics BigQuery event export data...
* [references](references/index.md) - This directory contains specifications for data joins and definitions for user activity and purchase metrics.
* [tables](tables/index.md) - Contains Google Analytics event export data from the `ga4_obfuscated_sample_ecommerce` dataset.
```

### Một concept dataset thật

`bundles/ga4/datasets/ga4_obfuscated_sample_ecommerce.md` (rút gọn phần thân):

```markdown
---
type: BigQuery Dataset
resource: https://bigquery.googleapis.com/v2/projects/bigquery-public-data/datasets/ga4_obfuscated_sample_ecommerce
title: BigQuery sample dataset for Google Analytics ecommerce web implementation
description: A sample of obfuscated Google Analytics BigQuery event export data for three months...
tags:
- ecommerce
- web analytics
- Google Analytics
- BigQuery
- public dataset
timestamp: '2026-05-28T22:49:59+00:00'
---

# Overview
...
# Pre-requisites
...
# Limitations
...
# Using the dataset
## Sample Query
```sql
SELECT COUNT(*) AS event_count, COUNT(DISTINCT user_pseudo_id) AS user_count ...
```
# Citations
- https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset
```

### Một concept table thật (schema lồng nhau)

`bundles/crypto_bitcoin/tables/transactions.md` cho thấy một bảng thật có schema RECORD REPEATED lồng nhau, nhiều mẫu truy vấn, và citations đánh số:

```markdown
---
type: BigQuery Table
resource: https://.../crypto_bitcoin/tables/transactions
title: Bitcoin Transactions
description: A comprehensive table detailing all transactions on the Bitcoin blockchain.
tags: [bitcoin, blockchain, transactions, crypto, public data, etl]
timestamp: '2026-05-28T22:45:04+00:00'
---

The `transactions` table in the [crypto_bitcoin](../datasets/crypto_bitcoin.md) dataset...
detailed arrays for both [inputs](inputs.md) and [outputs](outputs.md)...

# Schema
- `hash` STRING REQUIRED: The hash of this transaction
- ...
- `inputs` RECORD REPEATED: Transaction inputs
  - `index` INTEGER REQUIRED: 0-indexed number of an input...
# Common query patterns
```sql
SELECT DATE(block_timestamp) AS transaction_date, COUNT(hash) ...
```
# Citations
[1] [Bitcoin Transactions](https://...)
[2] [Bitcoin ETL](https://github.com/blockchain-etl/bitcoin-etl)
```

## Phần B - Năm bài học thực tế (nơi thực tế lệch đặc tả)

Đối chiếu gói thật với [OKF spec](okf-spec-explained.md) cho ra năm bài học quý:

1. Từ vựng type trong thực tế rất nhỏ. Google chỉ dùng vài giá trị: `BigQuery Dataset`, `BigQuery Table`, và `Reference`. Đặc tả cho phép type tự do, nhưng giữ nó gọn giúp consumer định tuyến dễ. Đây đúng lời khuyên chống type sprawl ở [gotchas-and-critiques](gotchas-and-critiques.md).
2. Metric được lưu với `type: Reference`, không phải một type `Metric` riêng. Ví dụ `references/metrics/avg_pageviews.md` có `type: Reference`, gắn `tags: [metric]`, thân chỉ một câu mô tả cộng một đoạn SQL cộng citations. Bài học: dùng type ở mức thô, phân biệt tinh hơn bằng tag và vị trí thư mục.
3. Gói thật dùng link tương đối, không phải link tuyệt đối bundle-relative. Spec khuyến nghị dạng `/tables/...`, nhưng gói thật viết `[inputs](inputs.md)` và `[crypto_bitcoin](../datasets/crypto_bitcoin.md)`. Cả hai đều hợp lệ. Bài học: chọn một quy ước và giữ nhất quán; link tương đối gọn nhưng dễ gãy hơn khi di chuyển file, đúng như spec cảnh báo.
4. Producer thêm section thân bài thoải mái. Ngoài `# Schema`, `# Examples`, `# Citations` quy ước, gói thật dùng `# Overview`, `# Pre-requisites`, `# Limitations`, `# Using the dataset`, `# Common query patterns`. Đặc tả không cấm; cấu trúc phục vụ nội dung.
5. `index.md` ở mọi cấp được sinh tự động, mỗi mục kéo `description` từ frontmatter của concept con. `timestamp` thật là ISO 8601 đầy đủ kèm offset, ví dụ `2026-05-28T22:49:59+00:00`.

## Phần C - Tác nhân làm giàu thật hoạt động thế nào

Mã nguồn `okf/src/reference_agent` cho thấy kiến trúc thật, gọn hơn nhiều người tưởng:

- Nền: Google ADK (`google.adk.Agent`, `FunctionTool`) cộng Gemini, model mặc định `gemini-flash-latest`.
- Hai tác nhân, mỗi tác nhân là một LLM kèm một bộ công cụ nhỏ:
  - Lượt BQ (`build_bq_agent`): công cụ `list_concepts`, `read_concept_raw`, `sample_rows`, `read_existing_doc`, `write_concept_doc`. Với mỗi concept trong dataset, runner gửi một thông điệp kiểu: "Enrich the concept with id: X, OKF type: Y. Follow the standard workflow and write exactly one document for this concept." Nghĩa là một concept, một tài liệu.
  - Lượt Web (`build_web_agent`): thêm công cụ `fetch_url`. Runner gửi các seed URL kèm giới hạn cứng và câu: "crawl outward as your judgment directs... Prefer skipping over borderline fetches - the budget is small."
- Sau hai lượt, `regenerate_indexes` tự dựng lại `index.md` ở mọi cấp.

### Điểm nối đắt giá với crawler của chúng ta

Lượt Web của Google là một crawler do Gemini điều khiển, và nó dùng đúng các núm kiểm soát mà skill crawler `truy-vet-url-tan-cung` của bạn có: `web_max_pages` (mặc định 100), `web_max_depth` (mặc định 2), và `allowed_hosts` mặc định bằng domain của các seed (tức same-domain by default). Khác biệt cốt lõi:

- Crawler của Google chọn link nào để theo bằng phán đoán của Gemini (đắt hơn, hiểu ngữ cảnh).
- Crawler `truy-vet-url-tan-cung` theo link một cách tất định (rẻ, tái lập được, không cần API model).

Hai cách bổ trợ nhau: dùng crawler tất định để lập bản đồ và gom trang, rồi để một model quyết định trang nào đáng biến thành concept.

## Phần D - Bài học cho hệ thống của bạn

Bạn không cần Google ADK hay Gemini để làm điều tương tự. Mẫu hình tái lập được với bất kỳ agent nào, kể cả [design playbook](design-playbook.md):

- Một agent, một bộ công cụ nhỏ: liệt kê concept, đọc concept, ghi concept, và fetch URL.
- Quy tắc một concept một tài liệu.
- Tự sinh lại index sau mỗi lượt.
- Lượt web có ngân sách chặt (max-pages, max-depth, same-domain), ưu tiên bỏ qua hơn là fetch bừa.

## Xem thêm

- [design-playbook](design-playbook.md) - dựng hệ thống của riêng bạn theo mẫu này.
- [okf-spec-explained](okf-spec-explained.md) - đối chiếu các bài học lệch chuẩn.
- [case-study-claude-memory](case-study-claude-memory.md) - một hiện thân sống khác của mẫu hình.
