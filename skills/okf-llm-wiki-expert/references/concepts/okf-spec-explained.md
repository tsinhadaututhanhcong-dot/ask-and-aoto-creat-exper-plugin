---
type: Reference
title: Giải thích đặc tả OKF v0.1
description: Bản diễn giải tiếng Việt đầy đủ, có hệ thống về đặc tả Open Knowledge Format phiên bản 0.1, đủ để đọc hiểu và tự kiểm tra tính tuân thủ.
tags:
  - okf
  - spec
  - frontmatter
  - reference
timestamp: 2026-07-03T00:00:00Z
source: Diễn giải từ file nguồn verbatim cùng thư mục source-okf-spec-v0.1.md (OKF v0.1 Draft, GoogleCloudPlatform/knowledge-catalog).
---

# Giải thích đặc tả OKF v0.1

Concept này diễn giải toàn bộ đặc tả OKF v0.1 bằng tiếng Việt. Bản gốc verbatim nằm ở [source-okf-spec-v0.1.md](source-okf-spec-v0.1.md) - khi cần trích chính xác từng câu chữ, hãy đọc file gốc đó; concept này là lớp giảng dạy nằm trên nó.

Một câu để nhớ: OKF chỉ là một thư mục các file markdown có YAML frontmatter. Không có schema registry, không có nhà chức trách trung tâm, không có công cụ bắt buộc. Câu thần chú trong spec: nếu bạn `cat` được một file thì bạn đọc được OKF; nếu bạn `git clone` được một repo thì bạn ship được nó.

## 1. Động lực và triết lý

OKF là định dạng mở, thân thiện cả người lẫn agent, dùng để biểu diễn tri thức - tức phần metadata, ngữ cảnh, và hiểu biết đã tuyển chọn bao quanh dữ liệu và hệ thống. Nó được thiết kế để con người viết, agent sinh, trao đổi giữa các tổ chức, và cả hai phía cùng tiêu thụ.

Bốn tiêu chí nền tảng của định dạng:

- `Readable` - người đọc được mà không cần công cụ.
- `Parseable` - agent phân tích được mà không cần SDK riêng.
- `Diffable` - so sánh được trong version control.
- `Portable` - mang đi được qua các công cụ, tổ chức, và thời gian.

Tinh thần xuyên suốt là minimally opinionated: OKF chỉ chuẩn hóa một tập nhỏ quy ước cấu trúc đủ để một kho tri thức tự mô tả được chính nó; mọi thứ vượt ra ngoài đó được để cho bên sản xuất tự quyết.

### Goals (mục tiêu)

1. Định nghĩa một định dạng phổ quát để enrichment agent ghi vào.
2. Hướng dẫn consumption agent cách đọc và duyệt qua nó.
3. Tạo thuận lợi cho việc trao đổi tri thức giữa các hệ thống và tổ chức.
4. Chuẩn hóa số ít trường bắt buộc phải có để nội dung tiêu thụ được một cách có ý nghĩa.

### Non-goals (cố tình không làm)

- Không định nghĩa một taxonomy cố định các loại concept.
- Không quy định hạ tầng lưu trữ, phục vụ, hay truy vấn.
- Không thay thế các schema chuyên biệt theo miền (Avro, Protobuf, OpenAPI...). OKF tham chiếu tới chúng chứ không nuốt chửng chúng.

## 2. Thuật ngữ

- `Knowledge Bundle` - một tập hợp tri thức khép kín, phân cấp. Đây là đơn vị phân phối.
- `Concept` - một đơn vị tri thức trong một bundle, biểu diễn bằng đúng một file markdown. Có thể tả một tài sản hữu hình (một bảng, một API), một ý niệm trừu tượng (một chỉ số, một quy trình nghiệp vụ), hay bất cứ thứ gì ở giữa.
- `Concept ID` - đường dẫn của file concept trong bundle, sau khi bỏ đuôi `.md`. Ví dụ `tables/users.md` có Concept ID là `tables/users`.
- `Frontmatter` - khối metadata YAML nằm giữa hai dòng `---` ở đầu file.
- `Body` - toàn bộ nội dung sau frontmatter.
- `Link` - một markdown link chuẩn từ concept này sang concept khác, dùng để diễn đạt quan hệ vượt ngoài phân cấp cha/con ngầm định.
- `Citation` - một link từ concept tới nguồn ngoài, chống lưng cho một khẳng định trong body.

## 3. Cấu trúc bundle

Một bundle là một cây thư mục các file markdown. Cấu trúc thư mục độc lập với miền: bên sản xuất tự tổ chức concept theo cách hợp lý nhất với tri thức đang nắm bắt.

```
path/to/bundle/
├── index.md          # Tùy chọn. Mục lục cho progressive disclosure.
├── log.md            # Tùy chọn. Lịch sử cập nhật theo thời gian.
├── <concept>.md      # Một concept ở gốc bundle.
└── <subdirectory>/   # Thư mục con nhóm các concept lại.
    ├── index.md
    ├── <concept>.md
    └── <subdirectory>/ ...
```

Một bundle có thể phân phối dưới dạng:

- Một git repository (khuyến nghị, vì có lịch sử, ghi công, diff).
- Một tarball hoặc zip của thư mục.
- Một thư mục con nằm trong một repo lớn hơn.

### 3.1 Tên file dành riêng (reserved)

Hai tên file sau có ý nghĩa cố định ở mọi cấp trong cây và không được dùng làm concept:

| Tên file   | Mục đích                        |
|------------|---------------------------------|
| `index.md` | Mục lục thư mục (xem mục 6).     |
| `log.md`   | Lịch sử cập nhật (xem mục 7).    |

Mọi file `.md` còn lại đều là concept. OKF không định nghĩa một định dạng file riêng để gom tài liệu theo tag; ai muốn xem theo tag thì tổng hợp lúc tiêu thụ bằng cách quét frontmatter.

## 4. Tài liệu concept

Mỗi concept là một file markdown UTF-8, gồm hai phần: một khối YAML frontmatter (mở và đóng bằng `---` trên dòng riêng), và một body markdown tự do.

### 4.1 Frontmatter

```yaml
---
type: <Type name>              # BẮT BUỘC
title: <Tên hiển thị, tùy chọn>
description: <Tóm tắt một câu, tùy chọn>
resource: <URI chuẩn của tài sản gốc, tùy chọn>
tags: [<tag>, <tag>]           # Tùy chọn
timestamp: <ISO 8601 datetime> # Thời điểm sửa gần nhất, tùy chọn
# ... các cặp key/value khác do producer tự định nghĩa
---
```

Trường bắt buộc duy nhất:

- `type` - một chuỗi ngắn cho biết đây là loại concept gì. Consumer dùng nó để định tuyến, lọc, và trình bày. Ví dụ: `BigQuery Table`, `BigQuery Dataset`, `API Endpoint`, `Metric`, `Playbook`, `Reference`. Giá trị `type` không đăng ký tập trung; bên sản xuất nên chọn giá trị mô tả và tự giải thích, còn consumer bắt buộc phải dung nạp `type` lạ một cách nhẹ nhàng (thường coi như concept chung).

Trường khuyến nghị (theo thứ tự ưu tiên):

- `title` - tên hiển thị cho người. Nếu thiếu, consumer có thể suy ra từ tên file.
- `description` - một câu tóm tắt concept. Dùng cho bộ sinh `index.md`, đoạn trích tìm kiếm, preview.
- `resource` - một URI định danh duy nhất tài sản mà concept mô tả. Vắng mặt với concept tả ý niệm trừu tượng thay vì tài nguyên vật lý.
- `tags` - một danh sách YAML các chuỗi ngắn để phân loại cắt ngang.
- `timestamp` - datetime ISO 8601 của lần thay đổi có ý nghĩa gần nhất.

Mở rộng: producer được thêm bất kỳ key nào. Consumer nên giữ nguyên key lạ khi round-trip và không được từ chối tài liệu chỉ vì có trường không nhận ra.

### 4.2 Body

Body là markdown chuẩn. Nên ưu tiên markdown có cấu trúc (heading, list, table, khối mã) hơn văn xuôi dài, vì cấu trúc giúp cả người đọc lẫn agent truy xuất. Không có mục nào bắt buộc. Ba heading sau mang ý nghĩa quy ước, nên dùng khi phù hợp:

| Heading       | Mục đích                                        |
|---------------|-------------------------------------------------|
| `# Schema`    | Mô tả có cấu trúc các cột/trường của một tài sản. |
| `# Examples`  | Ví dụ dùng cụ thể, thường là khối mã.           |
| `# Citations` | Nguồn ngoài chống lưng cho các khẳng định (mục 8). |

Spec kèm hai ví dụ concept: một cái có `resource` (kiểu `BigQuery Table`, body có `# Schema` dạng bảng và mục Joins), một cái không có `resource` (kiểu `Playbook`, body có Trigger và Steps). Xem chi tiết trong file gốc.

## 5. Liên kết chéo (cross-linking)

Concept có thể trỏ tới concept khác bằng markdown link chuẩn, hai dạng:

- Absolute (bundle-relative): bắt đầu bằng `/`, hiểu từ gốc bundle, ví dụ `[customers table](/tables/customers.md)`. Đây là dạng khuyến nghị vì bền khi file bị di chuyển trong thư mục con.
- Relative: đường dẫn markdown tương đối thường, ví dụ `[concept kế bên](./other.md)`.

Ngữ nghĩa link: một link từ A sang B khẳng định có một quan hệ. Loại quan hệ cụ thể (cha/con, references, joins-with, depends-on...) được diễn đạt bằng văn cảnh xung quanh, không phải bằng bản thân link. Bộ dựng đồ thị thường coi mọi link là cạnh có hướng, không kiểu. Consumer bắt buộc phải chịu được broken link: một link trỏ tới đích chưa tồn tại không phải lỗi định dạng, mà có thể chỉ là tri thức chưa được viết ra.

Lưu ý từ thực tế: dù spec khuyến nghị link tuyệt đối bắt đầu bằng `/`, các gói OKF sản xuất của Google lại thường dùng link tương đối (ví dụ `inputs.md`, `../datasets/x.md`). Cả hai đều hợp lệ. Xem [real-okf-bundle-and-agent](real-okf-bundle-and-agent.md).

## 6. File index

`index.md` có thể xuất hiện ở bất kỳ thư mục nào, kể cả gốc bundle. Nó liệt kê nội dung thư mục để phục vụ progressive disclosure - cho người hoặc agent thấy cái gì đang có trước khi mở từng tài liệu.

File index không có frontmatter (ngoại lệ duy nhất ở mục 11). Body dùng một hoặc nhiều mục, mỗi mục nhóm concept dưới một heading, mỗi dòng là một link kèm mô tả:

```markdown
# Nhóm / Section

* [Title 1](relative-url-1) - mô tả ngắn mục 1
* [Title 2](relative-url-2) - mô tả ngắn mục 2
```

Mỗi mục nên lấy `description` từ frontmatter của concept được trỏ tới. Producer có thể sinh `index.md` tự động; consumer có thể tự tổng hợp một cái khi không có sẵn.

## 7. File log (tùy chọn)

`log.md` có thể xuất hiện ở bất kỳ cấp nào để ghi lịch sử thay đổi trong phạm vi đó. Định dạng là danh sách phẳng các mục nhóm theo ngày, mới nhất trước:

```markdown
# Directory Update Log

## 2026-05-22
* **Update**: Thêm bảng [Customer Metrics](/tables/customer-metrics.md).
* **Creation**: Lập [Dataplex Playbook](/playbooks/dataplex.md).

## 2026-05-15
* **Initialization**: Tạo cấu trúc thư mục nền.
```

Heading ngày bắt buộc dùng dạng ISO 8601 `YYYY-MM-DD`. Từ in đậm mở đầu (`**Update**`, `**Creation**`, `**Deprecation**`...) là quy ước, không bắt buộc.

## 8. Citations

Khi body có khẳng định lấy từ tài liệu ngoài, liệt kê nguồn dưới heading `# Citations` ở cuối tài liệu, có đánh số:

```markdown
# Citations

[1] [BigQuery public dataset announcement](https://cloud.google.com/...)
[2] [Internal data quality runbook](https://wiki.acme.internal/data/quality)
```

Link citation có thể là URL tuyệt đối, đường dẫn bundle-relative, hoặc đường dẫn vào một thư mục `references/` phản chiếu tài liệu ngoài thành concept OKF hạng nhất.

## 9. Tuân thủ (conformance)

Một bundle tuân thủ OKF v0.1 nếu:

1. Mọi file `.md` không dành riêng đều có khối YAML frontmatter phân tích được.
2. Mọi khối frontmatter có trường `type` khác rỗng.
3. Mọi file dành riêng (`index.md`, `log.md`) tuân theo cấu trúc ở mục 6 và 7 khi có mặt.

Consumer nên coi mọi ràng buộc khác là hướng dẫn mềm. Đặc biệt, consumer không được từ chối một bundle vì: thiếu trường frontmatter tùy chọn; gặp `type` lạ; gặp key lạ; broken cross-link; thiếu file `index.md`. Mô hình tiêu thụ khoan dung này là cố ý: OKF phải còn hữu ích khi bundle lớn lên, được tái cấu trúc, và được agent sinh ra một phần.

## 10. Quan hệ với các định dạng khác

OKF cố tình gần với vài mẫu hình đã có: các LLM wiki repo dùng markdown cộng frontmatter làm kho tri thức cho agent; các công cụ tri thức cá nhân như Obsidian và Notion; hướng metadata-as-code lưu metadata cạnh mã nguồn thay vì trong một registry riêng. Khác biệt chính của OKF là nó được specified - ghim xuống tập nhỏ luật cần cho khả năng tương tác mà không áp đặt công cụ.

## 11. Versioning

Tài liệu này đặc tả OKF phiên bản 0.1. Các bản sau đánh số dạng `<major>.<minor>`: bump minor thêm phần tương thích ngược (trường tùy chọn mới, heading quy ước mới); bump major có thể phá vỡ (đổi tên trường bắt buộc, đổi tên file dành riêng). Bundle có thể khai báo phiên bản đích bằng `okf_version: "0.1"` trong frontmatter của `index.md` ở gốc - đây là nơi duy nhất một `index.md` được phép có frontmatter. Consumer không hiểu phiên bản khai báo thì nên cố tiêu thụ theo kiểu best-effort thay vì từ chối.

## Cheat sheet để tra nhanh

Trường frontmatter:

| Trường       | Bắt buộc | Ý nghĩa                                  |
|--------------|----------|------------------------------------------|
| `type`       | Có       | Loại concept; consumer dùng để định tuyến/lọc. |
| `title`      | Không    | Tên hiển thị; suy từ tên file nếu thiếu. |
| `description`| Không    | Tóm tắt một câu.                         |
| `resource`   | Không    | URI của tài sản gốc.                     |
| `tags`       | Không    | Danh sách chuỗi phân loại cắt ngang.     |
| `timestamp`  | Không    | ISO 8601 lần sửa gần nhất.               |
| (khác)       | Không    | Producer tự thêm; consumer giữ nguyên.   |

File dành riêng:

| File       | Frontmatter?                     | Nội dung                         |
|------------|----------------------------------|----------------------------------|
| `index.md` | Không (trừ `okf_version` ở root)  | Mục lục nhóm theo heading.        |
| `log.md`   | Không                            | Log theo ngày ISO, mới nhất trước.|

Ba quy tắc tuân thủ tối thiểu: mọi concept có frontmatter phân tích được; mọi frontmatter có `type` khác rỗng; file dành riêng đúng cấu trúc. Ngoài ra, đừng bao giờ từ chối một bundle vì thiếu trường, `type` lạ, key lạ, link gãy, hay thiếu index.

## Xem thêm

- [llm-wiki-concept](llm-wiki-concept.md) - mẫu hình vận hành mà OKF chính thức hóa.
- [design-playbook](design-playbook.md) - dùng đặc tả này để dựng một hệ thống hoàn chỉnh.
- [glossary-quickstart](glossary-quickstart.md) - tra thuật ngữ và làm thử bundle tối thiểu.
