---
type: Reference
title: Hệ sinh thái và công cụ quanh OKF LLM-wiki
description: Bộ công cụ tham chiếu chính thức của Google đi kèm OKF, cùng các bản triển khai cộng đồng quanh gist LLM-wiki của Karpathy.
tags:
  - okf
  - tooling
  - ecosystem
  - trip2g
  - rightmemory
timestamp: 2026-07-03T00:00:00Z
source: Phần A từ source-okf-readme.md cùng thư mục; phần B tổng hợp từ danh sách trong gist Karpathy và nghiên cứu.
---

# Hệ sinh thái và công cụ quanh OKF LLM-wiki

Concept này chia hai phần: (A) bộ công cụ tham chiếu chính thức Google phát hành kèm OKF, và (B) hệ sinh thái triển khai cộng đồng nở rộ quanh [gist LLM-wiki](source-llm-wiki-gist.md).

## Phần A - Công cụ tham chiếu chính thức của OKF

Nguồn: [OKF README](source-okf-readme.md).

### Reference Agent (công cụ làm giàu)

Chạy hai lượt để sinh ra một OKF bundle:

- BQ Pass: rút metadata từ một dataset BigQuery, tạo một concept cho mỗi bảng hoặc view.
- Web Pass: dùng LLM bò qua các URL hạt giống để làm giàu concept đang có và tạo tài liệu `Reference` mới. Có giới hạn cấu hình như `--web-max-pages` và domain allowlist để không tràn.

Cách cài và chạy (rút từ README):

```bash
python3.13 -m venv .venv
.venv/bin/pip install -e .[dev]

python -m reference_agent enrich \
    --source bq \
    --dataset <project>.<dataset> \
    --web-seed-file seeds.txt \
    --out ./bundles/<name>

python -m reference_agent visualize --bundle ./bundles/<name>
```

### Static HTML Visualizer

Một trang HTML tự chứa, không cần backend, biến một OKF bundle thành đồ thị tương tác:

- Dựng đồ thị lực hút (force-directed), nút tô màu theo `type`.
- Panel chi tiết hiển thị frontmatter và markdown đã render.
- Có backlink, cross-reference, search, lọc theo type, nhiều kiểu layout.
- Dùng Cytoscape.js và marked.js tải từ CDN.

### Ba gói mẫu kèm công thức

Mỗi gói ghép một recipe (URL hạt giống và lệnh chính xác) với một bundle đã sinh và một trực quan hóa:

- GA4 e-commerce.
- Stack Overflow (bài tập làm giàu nhiều concept).
- Bitcoin (khoe quan hệ khóa ngoại).

### mdcode

Công cụ dòng lệnh trong `toolbox/mdcode/demo`, thao tác với code nhúng trong markdown.

## Phần B - Hệ sinh thái cộng đồng quanh gist Karpathy

Gist LLM-wiki (hơn 5.000 sao) sinh ra một loạt bản triển khai. Các cái tiêu biểu:

### trip2g - máy chủ wiki qua MCP

Một kho Obsidian đồng bộ ra web, phơi ra qua giao thức MCP. Đặc điểm:

- Trang markdown có frontmatter `mcp_method` biến thành công cụ MCP gọi được.
- Hai chế độ truy xuất: Mode A đi theo index và wikilink một cách có chủ đích; Mode B tìm kiếm vector cho kho lớn hơn.
- Hỗ trợ federation: các kho tri thức tham chiếu và truy vấn lẫn nhau.
- Dùng bộ file khởi đầu `AGENTS.md`, `SCHEMA.md`, `_mcp_initialize.md`, cộng `index.md` và `log.md` - đúng tinh thần OKF.

### RightMemory - bộ nhớ agent bền vững nền Git

File lõi `MEMORY.md` với lược đồ chuyên biệt: anchor `{#slug}` làm điểm tham chiếu, node có ID duy nhất, edge có kiểu (dep, cfg, ver...). Tách vai trò rõ ràng: retrieve (đọc), update (ghi bền), dreamer (hợp nhất), pruner (dọn). Agent chính không tự sửa file mà gọi qua một skill điều phối để tránh xung đột và nửa-vời. Git làm nền đồng bộ đa thiết bị và lưu vết.

### Các dự án khác

- ProjectBrain.md: một chuẩn tri thức nền Git cho agent.
- QiJu: công cụ lịch sử quyết định.
- MindMux.ai: bàn làm việc local-first.
- sqz: nén ngữ cảnh.
- qmd: search engine markdown local (BM25 cộng vector, LLM re-rank, có CLI và MCP server) - chính công cụ Karpathy gợi ý cho bước thêm search.
- expo-llm-wiki, llm-wiki-newsroom: các bản dựng wiki khác.

## Ghi chú đáng giá

Hệ thống bộ nhớ của chính Claude Code - thư mục `memory/` với `MEMORY.md` làm chỉ mục, mỗi ghi nhớ một file, liên kết `[[tên]]` - là một hiện thân trực tiếp của mẫu hình LLM-wiki. Nếu bạn đang dùng Claude Code, bạn đang sống trong một ví dụ minh họa.

## Xem thêm

- [design-playbook](design-playbook.md) - Bước 7 mở rộng dùng đúng các công cụ này.
- [google-context](google-context.md) - Knowledge Catalog, bản thương mại hóa của Google.
- [real-okf-bundle-and-agent](real-okf-bundle-and-agent.md) - mổ xẻ mã nguồn tác nhân và gói mẫu OKF thật.
