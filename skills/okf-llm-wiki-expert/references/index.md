# INDEX - okf-llm-wiki-expert

Mục lục tri thức của expert về OKF (Open Knowledge Format) và mẫu hình LLM-wiki. Đọc file này trước, rồi mở các concept trong `concepts/` mà mục dưới trỏ tới.

## Lộ trình đọc gợi ý theo trình độ

- Người mới hoàn toàn: bắt đầu ở [glossary-quickstart](concepts/glossary-quickstart.md), rồi [llm-wiki-concept](concepts/llm-wiki-concept.md).
- Muốn thiết kế một hệ thống: đọc thẳng [design-playbook](concepts/design-playbook.md), tra chuẩn ở [okf-spec-explained](concepts/okf-spec-explained.md) khi cần.
- Người đã biết RAG/GraphRAG: bắt đầu ở [okf-vs-rag-graphrag](concepts/okf-vs-rag-graphrag.md).
- Muốn xem ví dụ thật, mã nguồn: [real-okf-bundle-and-agent](concepts/real-okf-bundle-and-agent.md) và [case-study-claude-memory](concepts/case-study-claude-memory.md).

## Nền tảng khái niệm

* [llm-wiki-concept](concepts/llm-wiki-concept.md) - mẫu hình LLM-wiki của Karpathy: kiến trúc ba lớp, ba thao tác ingest/query/lint, vì sao khác RAG, liên hệ Memex.
* [okf-spec-explained](concepts/okf-spec-explained.md) - diễn giải đầy đủ đặc tả OKF v0.1: bundle, concept, frontmatter, linking, index/log, citations, conformance, versioning, kèm cheat sheet.

## Thiết kế và thực hành

* [design-playbook](concepts/design-playbook.md) - file trung tâm: cẩm nang từng bước dựng một hệ thống OKF LLM-wiki hoàn chỉnh, kèm template CLAUDE.md và ví dụ xuyên suốt.
* [glossary-quickstart](concepts/glossary-quickstart.md) - bảng thuật ngữ đầy đủ và quickstart 10 phút cho người mới.

## Đối chiếu và bối cảnh

* [okf-vs-rag-graphrag](concepts/okf-vs-rag-graphrag.md) - so sánh RAG, OKF LLM-wiki, GraphRAG; khi nào dùng cái nào; cách phối hợp; liên hệ LightRAG.
* [google-context](concepts/google-context.md) - bối cảnh chiến lược: blog công bố OKF và sản phẩm Knowledge Catalog; vì sao Google vừa mở chuẩn vừa bán cỗ máy.
* [ecosystem-and-tooling](concepts/ecosystem-and-tooling.md) - công cụ tham chiếu chính thức (enrichment agent, visualizer, mdcode, gói mẫu) và hệ sinh thái cộng đồng (trip2g, RightMemory, qmd...).

## Ví dụ thực tế và triển khai (mổ xẻ mã nguồn)

* [real-okf-bundle-and-agent](concepts/real-okf-bundle-and-agent.md) - mổ xẻ gói OKF sản xuất thật (dataset, table schema lồng nhau, metric) và mã nguồn tác nhân làm giàu (Google ADK + Gemini, lượt BQ và lượt Web); năm bài học nơi thực tế lệch đặc tả.
* [case-study-claude-memory](concepts/case-study-claude-memory.md) - hệ thống memory của chính Claude Code như một LLM-wiki sống, kiểm tra được ngay trên đĩa; phép ánh xạ trực tiếp sang OKF.

## Bẫy và phê bình

* [gotchas-and-critiques](concepts/gotchas-and-critiques.md) - các điểm dễ sai khi thiết kế và phê bình cộng đồng; bài học rằng giá trị nằm ở vòng kiểm soát chất lượng (lint).

## Nguồn gốc verbatim (chân lý duy nhất)

Các file dưới đây là nội dung gốc tải nguyên văn, dùng để đối chiếu khi cần trích chính xác. Không sửa chúng.

* [source-okf-spec-v0.1.md](concepts/source-okf-spec-v0.1.md) - đặc tả OKF v0.1 nguyên văn (GoogleCloudPlatform/knowledge-catalog).
* [source-okf-readme.md](concepts/source-okf-readme.md) - README thư mục okf nguyên văn.
* [source-llm-wiki-gist.md](concepts/source-llm-wiki-gist.md) - gist LLM-wiki của Karpathy nguyên văn.
