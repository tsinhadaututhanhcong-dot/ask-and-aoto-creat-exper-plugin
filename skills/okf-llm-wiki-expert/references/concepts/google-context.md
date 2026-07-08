---
type: Reference
title: OKF trong bối cảnh chiến lược của Google
description: Đặt Open Knowledge Format vào chiến lược Data Cloud của Google - blog công bố OKF và sản phẩm Knowledge Catalog - để hiểu tại sao Google vừa mở chuẩn vừa bán cỗ máy vận hành chuẩn.
tags:
  - google
  - okf
  - knowledge-catalog
  - dataplex
  - strategy
timestamp: 2026-07-03T00:00:00Z
source: Tổng hợp nghiên cứu (blog Google Cloud dạng HTML, không có file verbatim cục bộ); đối chiếu với source-okf-readme.md và source-llm-wiki-gist.md cùng thư mục.
---

# OKF trong bối cảnh chiến lược của Google

Concept này trả lời một câu hỏi các file khác không trả lời: tại sao Google công bố một định dạng mở, trung lập nhà cung cấp, rồi tự mình xây sản phẩm xoay quanh nó. Hiểu bối cảnh giúp bạn thiết kế hệ thống của riêng mình với tầm nhìn dài hạn hơn, thay vì chỉ làm theo công thức.

## Hai mảnh ghép chiến lược

Google đặt hai vật thể lên bàn cờ cùng lúc, bổ trợ cho nhau:

| Mảnh ghép | Bản chất | Vai trò |
|-----------|----------|---------|
| OKF (Open Knowledge Format) | Một định dạng mở, trung lập nhà cung cấp | Cho cả ngành dùng chung để trao đổi tri thức |
| Knowledge Catalog | Một sản phẩm đóng của Google | Tiêu thụ và sinh ra tri thức theo định dạng đó |

Nước đi kinh điển nằm ở chỗ: Google vừa mở chuẩn cho toàn ngành, vừa bán cỗ máy vận hành chuẩn đó. Ai cũng dùng được OKF mà không bị khóa vào Google; nhưng khi bạn muốn một hệ thống doanh nghiệp sẵn sàng phục vụ agent ở quy mô lớn, Knowledge Catalog là sản phẩm đang chờ sẵn.

## Blog công bố OKF

Google Cloud công bố OKF qua bài blog "How the Open Knowledge Format can improve data sharing", đăng khoảng giữa tháng 6/2026, tác giả Sam McVeety và Amir Hormati thuộc nhóm Data Cloud.

Những điểm cốt lõi từ blog:

- Blog trích dẫn thẳng gist LLM-wiki của Karpathy. Google tự nhận OKF chính là bước chính thức hóa mẫu hình LLM-wiki - vốn là một ý tưởng trừu tượng, tùy chọn, modular (xem [llm-wiki-concept](llm-wiki-concept.md)) - thành một định dạng mở, trung lập nhà cung cấp.
- Google nhấn mạnh OKF chỉ là markdown cộng YAML frontmatter. Không nên phức tạp hóa: không runtime mới, không SDK bắt buộc. Một bundle có thể ship dưới dạng tarball hoặc một git repo. Điều này trùng khớp với tinh thần trong [OKF README](source-okf-readme.md) và [OKF spec](okf-spec-explained.md): portable, không lock-in, ai cũng produce và consume được.

### Ba nguyên tắc thiết kế được nhắc lại

Blog nhắc lại ba nguyên tắc định hình OKF, cũng là ba câu thần chú bạn nên mang theo khi thiết kế hệ thống của mình:

1. Minimally opinionated - chỉ một tập nhỏ key bắt buộc để bảo đảm khả năng tương tác, còn lại để mở.
2. Tách bạch producer và consumer - bên sản xuất tri thức và bên tiêu thụ độc lập nhau.
3. Là format không phải platform - OKF không gắn với một agent, framework, model provider hay serving system nào.

## Knowledge Catalog: cỗ máy tiêu thụ OKF

Nếu OKF là ngôn ngữ chung, thì Knowledge Catalog là cỗ máy của Google nói ngôn ngữ đó. Đây là bước tiến hóa của Dataplex thành một context engine luôn bật, phục vụ các agent doanh nghiệp. Nó đứng trên ba trụ.

- Aggregation (gom): gom metadata từ các kho Google (BigQuery, AlloyDB, Spanner, Cloud SQL, Firestore, Looker), catalog bên thứ ba (Atlan, Collibra, Datahub), và hệ thống doanh nghiệp (Salesforce, SAP, ServiceNow, Workday).
- Enrichment (làm giàu): Gemini sinh mô tả ngôn ngữ tự nhiên, glossary, cùng rào chắn ngữ nghĩa và các mẫu SQL đã kiểm chứng để chống truy vấn ảo giác.
- Search (tìm kiếm): tìm kiếm ngữ nghĩa lai, độ trễ dưới một giây, tôn trọng phân quyền.

Knowledge Catalog cấp nguồn tri thức cho các agent doanh nghiệp, ví dụ Deep Research Agent trong Gemini Enterprise. Tri thức gom và làm giàu không nằm yên mà trở thành ngữ cảnh sống cho các agent hoạt động ở tầng trên.

## Ý nghĩa cho người thiết kế hệ thống OKF

- Chọn định dạng mở làm nền móng. Vì OKF là markdown cộng YAML, tri thức bạn tạo ra không bị khóa vào một công cụ. Bắt đầu bằng một thư mục file và git đúng như [OKF spec](okf-spec-explained.md) mô tả, sau này mới nối vào một context engine nếu cần.
- Tách bạch rõ producer và consumer để hệ thống dễ thay thế từng phần, dễ mở rộng.
- Hiểu đường đi dài hạn. Nếu hệ thống của bạn lớn dần, mẫu hình Knowledge Catalog (gom, làm giàu, tìm kiếm, cấp nguồn cho agent) là một bản đồ tham khảo về nơi bạn có thể tới.

## Xem thêm

- [okf-spec-explained](okf-spec-explained.md) - đặc tả kỹ thuật của định dạng.
- [ecosystem-and-tooling](ecosystem-and-tooling.md) - reference agent, visualizer và công cụ quanh OKF.
- [design-playbook](design-playbook.md) - cách thiết kế một hệ thống OKF LLM-wiki hoàn chỉnh.
