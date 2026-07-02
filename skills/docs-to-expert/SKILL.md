---
name: docs-to-expert
description: >
  Tự động tạo một "Expert Skill" tra cứu tài liệu từ một URL trang docs (ví dụ: developer docs).
  Ưu tiên mirror qua chuẩn llms.txt (một file cho mỗi trang gốc, không băm nhỏ, không thể trùng),
  chỉ cào HTML khi trang nguồn không hỗ trợ.
when_to_use: >
  - Khi người dùng muốn tạo một skill chuyên gia từ một trang web tài liệu (docs url).
  - Khi người dùng yêu cầu "bắt lấy URL", "ingest docs", "tạo wiki từ trang web".
  - Khi cần cập nhật lại một skill dạng này đã tạo trước đó mà không muốn làm lại từ đầu.
allowed-tools: Bash, Read, Write, WebFetch, Glob, Grep
effort: high
---

# Docs to Expert Orchestrator

Skill này đóng vai trò điều phối (Orchestrator) tự động hóa toàn bộ quy trình: từ việc lấy nội dung của một trang web tài liệu, đến việc tổ chức thành một Expert Skill hoàn chỉnh (một file `.md` cho mỗi trang gốc, gom trong `references/concepts/`, có `INDEX.md` dẫn lối).

**Nguyên tắc cốt lõi:** mỗi trang tài liệu gốc = đúng một file trên đĩa. Không băm nhỏ theo tiêu đề (dễ trùng khi hai đoạn khác nhau vô tình cùng tên, ví dụ một dòng comment code `# Before` trong ví dụ bị nhầm thành tiêu đề trang). Tên file luôn suy ra từ URL - vốn dĩ duy nhất, không thể trùng.

## Quy trình Thực thi (Pipeline)

### Bước 1: Xác nhận thông tin
Đảm bảo bạn đã có:
1. `<root_url>`: một URL bất kỳ nằm trong trang tài liệu (VD: `https://code.claude.com/docs/en/overview`).
2. `<skill_name>`: tên của Kỹ năng Chuyên gia sẽ được tạo ra (kebab-case, VD: `claude-expert`).
*(Nếu thiếu, hãy hỏi người dùng).*

### Bước 2: Tạo thư mục đích
Thư mục skill đích nằm trong thư mục skills cá nhân của người dùng, không hardcode đường dẫn máy cụ thể:
```powershell
$skillDir = Join-Path $env:USERPROFILE ".claude\skills\<skill_name>"
New-Item -ItemType Directory -Force -Path "$skillDir\references"
```

### Bước 3: Lấy nội dung (ưu tiên llms.txt, cào HTML là dự phòng)

**Nhánh A (mặc định - thử trước tiên):** chạy `fetch_llms_docs.py`. Script tự dò `llms.txt` ở gốc site hoặc dưới `/docs`, tải nguyên văn từng trang `.md`, ghi mỗi trang thành một file trong `concepts/`, và tự sinh `INDEX.md` trực tiếp từ chính danh sách llms.txt - không cần bước băm nhỏ riêng.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/fetch_llms_docs.py" --root "<root_url>" --output "$skillDir\references"
```

Nếu script in ra `Tai xong: N trang, 0 loi` -> `references/` đã hoàn chỉnh, **bỏ qua Bước 4, sang thẳng Bước 5**. Script tự coi một trang có nội dung quá ngắn (dưới ~80 ký tự sau khi lấy) là lỗi thay vì âm thầm ghi file rỗng - nếu `N loi` > 0 và cảnh báo nói "trang co the render bang JavaScript", trang nguồn nhiều khả năng là SPA (nội dung chỉ xuất hiện sau khi chạy JavaScript phía client) - chuyển thẳng sang Nhánh C, không cần thử Nhánh B (Nhánh B cào HTML thô cũng gặp đúng vấn đề tương tự).

**Nhánh B (dự phòng - khi script thoát mã 2 / in `NO_LLMS_TXT`):** trang nguồn không hỗ trợ llms.txt. Dùng `extract_links.py --export-dir` (script này tự thử hậu tố `.md` cho từng trang trước khi cào HTML, và luôn đặt tên file theo URL nên cũng không thể trùng):

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/extract_links.py" --url "<root_url>" --output "$skillDir\references\links.txt" --export-dir "$skillDir\references\concepts"
```

Script tự sinh `$skillDir\references\concepts\knowledge_graph.md` - đổi tên/di chuyển file này thành `$skillDir\references\INDEX.md`.

**Gotcha đã gặp thực tế (Document AI, NotebookLM):** `extract_links.py` chỉ crawl tiếp các link có URL bắt đầu đúng bằng chuỗi `<root_url>` (`startswith`), và đặt tên file xuất ra theo PATH của URL (bỏ qua query string). Hai hệ quả: (1) nếu `<root_url>` là một trang lá cụ thể (vd `.../docs/overview`), script sẽ không bao giờ tìm thấy các trang anh em khác (`.../docs/create-processor`) - phải dùng một prefix rộng hơn (vd `.../docs` hoặc gốc mục, không phải 1 trang lá) làm `<root_url>`; (2) nếu `<root_url>` có kèm query string chọn ngôn ngữ (vd `?hl=zh-tw`), các bản dịch khác của cùng 1 trang sẽ cùng chung 1 tên file và ghi đè lẫn nhau, kết quả cuối chỉ còn 1 ngôn ngữ ngẫu nhiên - luôn dùng URL tiếng Anh, không kèm `?hl=`.

**Nhánh C (trang cần JavaScript để render nội dung - đã gặp thực tế với antigravity.google):** dùng `fetch_js_rendered.py`, dùng trình duyệt headless (Playwright) để render từng trang trước khi trích nội dung, tái dùng đúng các hàm parse/convert của `fetch_llms_docs.py` nên cùng định dạng, cùng quy tắc "một trang gốc, một file":

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/fetch_js_rendered.py" --llms-txt "<url_llms.txt_da_tim_thay_o_Nhanh_A>" --output "$skillDir\references"
```

Yêu cầu đã cài `playwright` (`pip install playwright && playwright install chromium`) - kiểm tra bằng `python -m playwright --version` trước khi chạy, cài nếu thiếu.

**Nhánh D (chỉ khi cả A, B, C đều thất bại - trang chống bot, cấu trúc quá đặc thù):** tự viết một script cào tùy biến bằng `Write`, lưu vào một file tạm, chạy thử bằng `Bash`, sửa lỗi và lặp lại đến khi ra được `INDEX.md` + `concepts/` hoàn chỉnh theo đúng quy tắc "một trang gốc, một file". Không có sub-agent chuyên biệt nào để giao việc này - tự làm trực tiếp bằng `Write` + `Bash`.

### Bước 4: (chỉ khi đi Nhánh B) Dọn lại INDEX.md
Mở `knowledge_graph.md` vừa sinh, giữ lại đúng phần "Table of Contents" dạng danh sách link, đó chính là nội dung của `INDEX.md`. Phần "Graph" (sơ đồ mermaid) có thể bỏ hoặc giữ tùy ý, không bắt buộc cho việc tra cứu.

### Bước 5: Phát hiện đa bề mặt + gắn nhãn (nếu có)

Nhiều trang tài liệu thực ra mô tả nhiều "bề mặt"/sản phẩm khác nhau dưới cùng một domain (ví dụ Claude Code có CLI/Desktop/VS Code/Web/SDK; Google Antigravity có 2.0/IDE/CLI/SDK). Nếu bỏ qua bước này, agent tra cứu về sau có thể vớ trúng một trang thuộc bề mặt khác với bề mặt đang được hỏi rồi trả lời sai kiểu "Desktop có tính năng X" trong khi X chỉ có ở CLI - đây là lỗi thật đã xảy ra và phải chủ động phòng từ lúc tạo skill, không đợi người dùng phát hiện rồi báo lại.

Chạy dò trước:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/tag_by_surface.py" --detect --index "$skillDir\references\INDEX.md"
```

Script ghi ra `surface_mapping.json` cạnh `INDEX.md` và in một trong hai kết quả:

**`TIER1_CONFIDENT`** (tìm được cấu trúc rõ qua tên file, ví dụ tiền tố lặp lại kiểu `docs-cli-*`/`docs-ide-*`): đọc lướt vài trang mẫu mỗi nhóm để xác nhận nhanh (không tin mù kết quả máy móc), sửa `surface_mapping.json` nếu có trang bị xếp sai hoặc thiếu (nhóm quá nhỏ như chỉ 1-2 trang thường bị bỏ sót, phải tự thêm tay), rồi chạy `--apply` (xem dưới).

**`TIER1_UNCLEAR`** (tên file không lộ cấu trúc - ví dụ URL nguồn phẳng không có tiền tố theo bề mặt, trường hợp này đã gặp thật với `code.claude.com`): đọc toàn bộ tiêu đề + mô tả đã có sẵn trong `INDEX.md` (không cần fetch thêm gì), tự phân loại thủ công xem mỗi trang thuộc bề mặt nào - đúng việc đã làm tay cho `claude-expert`. Sửa `surface_mapping.json` cho từng file (giá trị là tên bề mặt tự đặt, ví dụ `cli`/`desktop`/`sdk`/`shared`).

Nếu rõ ràng trang nguồn chỉ có một sản phẩm/bề mặt duy nhất (không đa dạng), bỏ qua toàn bộ Bước 5, dùng template đơn giản ở Bước 6.

Script cũng quét gợi ý những trang có thể là "trang đối chiếu chính thức giữa các bề mặt" (từ khóa kiểu so sánh/lựa chọn). Đọc lại các trang được gợi ý để xác nhận thật - nếu đúng là trang đối chiếu chính thức, ghi tên file lại để dùng ở bước `--apply`. Nếu không có trang nào như vậy (trường hợp Google Antigravity), bỏ qua, `--apply` sẽ tự thêm cảnh báo "không có trang đối chiếu chính thức" vào `INDEX.md`.

Sau khi `surface_mapping.json` đã đầy đủ (không còn giá trị `UNCLASSIFIED` nào), áp dụng:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/tag_by_surface.py" --apply --index "$skillDir\references\INDEX.md" --mapping "$skillDir\references\surface_mapping.json" --comparison-files "trang1.md,trang2.md"
```

(`--comparison-files` bỏ qua nếu không có trang đối chiếu chính thức nào được xác nhận.) Script gắn `platform:` vào frontmatter mỗi file và sinh lại `INDEX.md` nhóm theo bề mặt, mục đối chiếu chính thức (nếu có) luôn ở đầu.

### Bước 6: Đóng gói SKILL.md cho Expert

Dùng `Write` để tạo `$skillDir\SKILL.md`. Chọn đúng 1 trong 2 template dưới đây tùy Bước 5 có chạy hay không.

**Template đơn giản** (Bước 5 không áp dụng - chỉ 1 bề mặt/sản phẩm) - thay `{SKILL_NAME}`, `{ROOT_URL}`, `{CURRENT_DATE}`:

```markdown
---
name: {SKILL_NAME}
description: >
  Chuyên gia tra cứu tài liệu hướng dẫn kỹ thuật liên quan đến {SKILL_NAME}.
when_to_use: >
  - Khi người dùng hoặc Agent khác cần thông tin chuyên sâu về công nghệ hoặc framework này.
allowed-tools: Read, Grep
effort: medium
---

# Chuyên gia {SKILL_NAME}

## Những điểm dễ sai (Gotchas)

| CÁCH LÀM SAI (Ảo giác) | CÁCH LÀM ĐÚNG (Dựa trên tài liệu) |
|---|---|
| Dựa trên trí nhớ hoặc kiến thức pre-train có sẵn (dẫn đến ảo giác). | **BẮT BUỘC** dùng tool `Read` để đọc tệp `references/INDEX.md` TRƯỚC, sau đó đọc các file concept tương ứng trong thư mục `references/concepts/`. |

## Cây Quyết định (Decision Tree)

Mỗi khi nhận được yêu cầu:
1. **NẾU người dùng hỏi nguyên lý, API, cách cấu hình, hoặc gỡ lỗi:**
   - **Bước 1:** Đọc file `references/INDEX.md` để tìm chủ đề liên quan.
   - **Bước 2:** Dùng tool `Read` để đọc các tệp `.md` cụ thể trong thư mục `references/concepts/` mà INDEX trỏ tới.
   - **Bước 3:** Trích xuất thông tin liên quan trực tiếp đến câu hỏi và trả lời.
2. **NẾU Agent khác hỏi để lấy ngữ cảnh:**
   - Đọc `INDEX.md` và các concept file liên quan, sau đó trả về đúng JSON / cấu trúc dữ liệu được yêu cầu.

## Tự Nhận Thức & Cập Nhật (Self-Update)
- URL gốc tạo ra bạn: `{ROOT_URL}`
- Ngày nạp dữ liệu: `{CURRENT_DATE}`

**Nghĩa vụ của bạn:** Nếu trong quá trình dùng, tài liệu báo lỗi `deprecated`, `version mismatch`, hoặc đã quá 3-6 tháng kể từ Ngày nạp dữ liệu, BẠN PHẢI chủ động đề xuất: *"Tài liệu của tôi có thể đã cũ, hãy cho phép tôi gọi lại docs-to-expert để cập nhật (chế độ update, không cần tạo lại từ đầu)."*

## Triết lý Cốt lõi
*Không giả định, không bịa đặt. Tài liệu (docs) trong thư mục references là chân lý duy nhất.*
```

**Template đa bề mặt** (Bước 5 đã chạy `--apply`) - thêm `{DANH_SACH_BE_MAT}` (liệt kê tên các bề mặt từ `surface_mapping.json`, ví dụ `cli`/`desktop`/`sdk`/`shared`) và `{QUY_TAC_DOI_CHIEU}` (một trong hai câu: nếu có `--comparison-files` thì "đọc các trang đối chiếu chính thức: X, Y trước khi trả lời câu hỏi so sánh giữa các bề mặt"; nếu không thì "không có trang đối chiếu chính thức - áp dụng quy tắc im lặng = chưa xác nhận: nếu tính năng chỉ thấy ở bề mặt khác, trả lời rõ là chưa xác nhận cho bề mặt đang hỏi, không suy diễn"):

```markdown
---
name: {SKILL_NAME}
description: >
  Chuyên gia tra cứu tài liệu hướng dẫn kỹ thuật liên quan đến {SKILL_NAME}: {DANH_SACH_BE_MAT}.
when_to_use: >
  - Khi người dùng hoặc Agent khác cần thông tin chuyên sâu về công nghệ hoặc framework này.
  - Đặc biệt khi câu hỏi so sánh hoặc xác nhận tính năng giữa các bề mặt ({DANH_SACH_BE_MAT}).
allowed-tools: Read, Grep
effort: medium
---

# Chuyên gia {SKILL_NAME}

## Những điểm dễ sai (Gotchas)

| CÁCH LÀM SAI (Ảo giác) | CÁCH LÀM ĐÚNG (Dựa trên tài liệu) |
|---|---|
| Dựa trên trí nhớ hoặc kiến thức pre-train có sẵn (dẫn đến ảo giác). | **BẮT BUỘC** dùng tool `Read` để đọc tệp `references/INDEX.md` TRƯỚC, sau đó đọc các file concept tương ứng trong thư mục `references/concepts/`. |
| Tìm thấy 1 file khớp từ khóa và kết luận ngay tính năng đó cũng có ở bề mặt khác đang được hỏi. | Kiểm tra trường `platform:` trong frontmatter của file đó. {QUY_TAC_DOI_CHIEU} |

## Cây Quyết định (Decision Tree)

0. **Bước 0 - Xác định bề mặt đang được hỏi (BẮT BUỘC, làm trước mọi bước khác):** phân loại câu hỏi vào một trong {DANH_SACH_BE_MAT}. `references/INDEX.md` đã nhóm sẵn theo đúng các mục này. Chỉ tìm trong đúng mục đã xác định + mục dùng chung (nếu có).
1. **NẾU người dùng hỏi nguyên lý, API, cách cấu hình, hoặc gỡ lỗi:**
   - **Bước 1:** Đọc file `references/INDEX.md`, tìm trong đúng mục bề mặt đã xác định ở Bước 0.
   - **Bước 2:** Dùng tool `Read` để đọc các tệp `.md` cụ thể trong thư mục `references/concepts/` mà INDEX trỏ tới.
   - **Bước 3:** Trích xuất thông tin liên quan trực tiếp đến câu hỏi và trả lời.
2. **NẾU Agent khác hỏi để lấy ngữ cảnh:**
   - Đọc `INDEX.md` và các concept file liên quan, sau đó trả về đúng JSON / cấu trúc dữ liệu được yêu cầu.

## So sánh mở giữa các bề mặt (không quy về được một mục có sẵn)

Câu dạng "X khác Y ở đâu" khó xử lý an toàn hơn câu nhị phân "X có Y không" - thường không có sẵn một trang trả lời thẳng, phải tự ghép thông tin từ 2-3 file mô tả riêng lẻ từng bề mặt. Không thể chỉ nói "không có tài liệu so sánh" rồi dừng (không hữu ích), nhưng cũng không được trình bày phần ghép nối như một sự thật tài liệu đã xác nhận trực tiếp.

Cách làm đúng:
1. Đọc riêng file mô tả từng bề mặt đang được hỏi (không đoán từ 1 file khớp từ khóa).
2. Nếu {QUY_TAC_DOI_CHIEU} nói không có trang đối chiếu chính thức, nói rõ ngay từ đầu câu trả lời điều đó.
3. Trình bày khác biệt như suy luận ghép nối, luôn gắn nguồn cho từng phần (ví dụ "theo tài liệu về X... còn theo tài liệu về Y...") để phân biệt đâu là trích dẫn trực tiếp, đâu là do tự nối lại.
4. Nếu một phần của câu hỏi không có file nào nhắc tới ở cả hai phía, nói rõ phần đó chưa có tài liệu - không lấp đầy bằng suy đoán.

## Tự Nhận Thức & Cập Nhật (Self-Update)
- URL gốc tạo ra bạn: `{ROOT_URL}`
- Ngày nạp dữ liệu: `{CURRENT_DATE}`
- Đã phân loại các trang theo bề mặt: {DANH_SACH_BE_MAT}.

**Nghĩa vụ của bạn:** Nếu trong quá trình dùng, tài liệu báo lỗi `deprecated`, `version mismatch`, hoặc đã quá 3-6 tháng kể từ Ngày nạp dữ liệu, BẠN PHẢI chủ động đề xuất: *"Tài liệu của tôi có thể đã cũ, hãy cho phép tôi gọi lại docs-to-expert để cập nhật (chế độ update, không cần tạo lại từ đầu)."*

## Triết lý Cốt lõi
*Không giả định, không bịa đặt. Tài liệu (docs) trong thư mục references là chân lý duy nhất. Khi không chắc một tính năng có thuộc về bề mặt đang hỏi hay không, nói rõ sự không chắc chắn đó thay vì suy diễn.*
```

### Bước 7: Báo cáo
Báo cho người dùng: đã tạo `<skill_name>` tại `$skillDir`, số trang lấy được, đi theo nhánh nào (A/B/C/D), có chạy Bước 5 hay không và tìm được bao nhiêu bề mặt.

## Cập nhật một skill đã tạo (không làm lại từ đầu)

Khi tài liệu nguồn có khả năng đã đổi và người dùng muốn làm mới một skill đã tạo bằng công cụ này (đi Nhánh A khi tạo lần đầu), chạy lại đúng lệnh cũ kèm `--update`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/fetch_llms_docs.py" --root "<root_url>" --output "$skillDir\references" --update
```

Script tự so sánh với `INDEX.md` hiện có, chỉ tải lại `.md` cho trang mới xuất hiện hoặc trang có mô tả trong llms.txt đã đổi; báo cáo số trang thêm/đổi/giữ nguyên. Toàn bộ bước này chạy bằng script thuần, không cần agent đọc/viết lại từng file - rẻ hơn hẳn so với tạo lại skill từ đầu. Nếu skill được tạo qua Nhánh B (không có llms.txt), chạy lại Bước 3 Nhánh B từ đầu - trang không hỗ trợ llms.txt thường cũng không có cách nào rẻ hơn để biết phần nào đã đổi.

Nếu skill này có gắn nhãn đa bề mặt (đã chạy Bước 5 lúc tạo), các trang mới/đổi sau `--update` chưa có `platform:`. Chạy lại `tag_by_surface.py --detect` trên `INDEX.md` vừa cập nhật - chỉ cần phân loại tay cho những trang còn thiếu nhãn (thường rất ít so với tổng số trang), rẻ hơn nhiều so với phân loại lại từ đầu.

## Bổ sung nguồn từ GitHub repo (khi người dùng chỉ định tường minh)

**Trường hợp dùng:** một expert cần cả tài liệu chính thức (trang docs) LẪN tài liệu của một công cụ/thư viện liên quan chỉ tồn tại dưới dạng repo GitHub (ví dụ: một MCP server/CLI cộng đồng để thao tác với sản phẩm đó). Ví dụ thật: `notebooklm-expert` cần cả `support.google.com/notebooklm` (chính thức) lẫn repo `jacob-bd/notebooklm-mcp-cli` (công cụ CLI/MCP cộng đồng) vì người dùng muốn học cách dùng MCP để điều khiển NotebookLM.

**Quy tắc tin cậy (BẮT BUỘC tuân thủ):** khác với trang docs (có thể tự tìm qua `WebSearch` + xác minh domain chính thức ở Bước 4 template phía trên), **repo GitHub KHÔNG BAO GIỜ được tự ý tìm/chọn** — chỉ ingest một repo khi người dùng chỉ định đích danh URL repo đó. Lý do: không có cách xác minh tự động "repo này đáng tin cậy" như cách xác minh domain chính thức; quyết định tin tưởng một repo cộng đồng cụ thể là quyết định của con người, không phải của AI tự suy đoán.

**Cách chạy:**

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/fetch_repo_docs.py" --repo "<github_repo_url>" --output "$skillDir\references"
```

Script `git clone --depth 1` repo vào thư mục tạm, lấy: `README*` ở gốc repo, mọi file dưới `docs/`, và các file có tên gợi ý là định nghĩa tool/schema (chứa `tool`/`schema`/`mcp`/`server`, ví dụ `server.py`, `tools.json`) — bỏ qua `node_modules/`, `dist/`, `.git/`, file rỗng hoặc lớn hơn 60KB, tối đa 30 file (`--max-files` để đổi). Ghi mỗi file thành `concepts/repo-<đường-dẫn-đã-làm-phẳng>.md`, có ghi rõ nguồn (`repo_url/blob/<branch>/<path>`) ở đầu file. Xoá thư mục clone tạm sau khi xong.

**Gotcha đã gặp thực tế (ag-kit):** heuristic mặc định (README + `docs/` + tên file gợi ý tool/schema) không phải lúc nào cũng khớp cấu trúc repo — ví dụ repo mà bản thân nó LÀ một bộ template (agent/skill/workflow definitions), nội dung giá trị nằm trong một thư mục có tên riêng (vd `.agents/`) không khớp heuristic. Khi kiểm tra thấy số file ingest được quá ít so với kỳ vọng, `git clone --depth 1` repo vào thư mục tạm để xem cây thư mục thật (`find <tmp> -maxdepth 3`), rồi dùng thêm cờ `--include-glob "<pattern>"` (lặp lại nhiều lần được, khớp theo đường dẫn tương đối gốc repo, hỗ trợ wildcard `*`) để buộc lấy đúng phần đó, ví dụ:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/docs-to-expert/scripts/fetch_repo_docs.py" --repo "<url>" --output "$skillDir\references" --max-files 120 --include-glob ".agents/agent/*.md" --include-glob ".agents/workflows/*.md" --include-glob ".agents/rules/*.md" --include-glob ".agents/skills/*/SKILL.md" --include-glob "AGENT_FLOW.md" --include-glob "CHANGELOG.md"
```

Nhớ tăng `--max-files` (mặc định 30) nếu số file khớp glob nhiều hơn mức mặc định — nếu không script sẽ dừng sớm khi chạm giới hạn.

**Sau khi chạy:**
1. Mở `INDEX.md` hiện có của expert, thêm một mục mới `## Nguồn bổ sung: repo <tên_repo> (bên thứ ba, người dùng chỉ định tường minh)` liệt kê các file `repo-*.md` vừa sinh, có 1 dòng ghi rõ đây không phải tài liệu chính thức.
2. Nếu expert đã có nội dung từ trang docs chính thức trước đó, thêm một dòng vào bảng Gotchas của `SKILL.md` expert đó: phân biệt rõ khi nào dùng file chính thức (`concepts/<slug-docs>.md`) và khi nào dùng file repo (`concepts/repo-*.md`) — không lẫn lộn hai nguồn khi trả lời.
3. Cập nhật mục "Tự Nhận Thức & Cập Nhật" của `SKILL.md` expert đó: tách rõ "Nguồn chính thức" và "Nguồn bổ sung" (kèm URL repo, số file, ngày ingest).
