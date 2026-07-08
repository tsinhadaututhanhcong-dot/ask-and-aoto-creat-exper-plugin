---
type: Reference
title: Các bẫy thiết kế và phê bình cộng đồng
description: Những điểm dễ sai khi thiết kế một hệ thống OKF LLM-wiki, và các phê bình từ cộng đồng, để người thiết kế tránh cạm bẫy và hiểu giá trị thật nằm ở đâu.
tags:
  - okf
  - llm-wiki
  - gotchas
  - critique
  - lint
timestamp: 2026-07-03T00:00:00Z
source: Tổng hợp nghiên cứu và thảo luận Hacker News quanh OKF và gist LLM-wiki.
---

# Các bẫy thiết kế và phê bình cộng đồng

Concept này giúp bạn tránh những sai lầm đã thấy trong thực tế, và hiểu tại sao giá trị của mẫu hình không nằm ở bản thân định dạng file.

## Phần A - Bẫy thiết kế

- `index.md` phình to ở quy mô lớn. Cách đọc-index-trước chạy tốt tới khoảng 100 nguồn. Vượt mức đó, đừng dựa hết vào index; thêm một search engine thật như `qmd`. Xem Bước 7 trong [design-playbook](design-playbook.md).
- Broken link là bình thường. Theo [OKF spec](okf-spec-explained.md), một link trỏ tới đích chưa tồn tại không phải lỗi mà có thể là tri thức chưa viết. Đừng viết code cứng từ chối bundle vì link gãy.
- Type sprawl (loạn type). Để `type` mọc lung tung khiến consumer khó định tuyến. Giữ một từ vựng `type` gọn, mô tả, nhất quán; định nghĩa nó ngay trong file schema.
- Schema drift (lệch schema). File schema và thực tế wiki dần lệch nhau theo thời gian. Phải cùng tiến hóa file schema khi phát hiện quy ước mới, và dùng lint để phát hiện lệch.
- LLM vẫn sai khi bảo trì. Nó có thể viết nhầm cross-reference, bỏ sót cập nhật, hoặc tổng hợp lệch. Đây chính là lý do thao tác lint và một agent linter là bắt buộc, không phải tùy chọn.
- Một ingest chạm quá nhiều trang. Một nguồn có thể chạm 10 tới 15 trang; nếu ingest hàng loạt không giám sát, một lỗi có thể lan truyền. Nên review khi còn ít nguồn, và giữ mình trong vòng lặp ở giai đoạn đầu.
- Xử lý ảnh còn vụng. LLM không đọc markdown có ảnh inline trong một lượt; phải đọc text trước rồi xem ảnh riêng. Nếu nguồn của bạn chỉ có text, bỏ qua toàn bộ phần ảnh cho nhẹ.

## Phần B - Phê bình cộng đồng

- Trùng lặp công cụ. Có ý kiến cho rằng NotebookLM đã phục vụ mục đích tương tự, nên OKF LLM-wiki chưa hẳn mới về công năng. Phản biện: điểm khác biệt là artifact bền vững con người kiểm soát được, không phải một hộp đen.
- Gánh nặng ở quy mô lớn. Khi kho tri thức phình to, đơn giản hóa trở nên tối quan trọng để tránh chi phí quản lý vượt tầm. Chính Karpathy nhấn mạnh điểm này, và đó là lý do thao tác lint ra đời.
- Bài nổi bật trên Hacker News là một linter cho OKF. Điều này cho thấy khâu kiểm soát chất lượng tự động mới là giá trị gia tăng thật sự, chứ không phải bản thân định dạng markdown.
- Hoài nghi kiểu SEO/GEO. Một số nguồn đặt câu hỏi liệu OKF là công cụ thật hay chỉ là chiêu tối ưu hiện diện cho mô hình (Generative Engine Optimization).

## Phần C - Bài học sâu

Định dạng chỉ là cái khung. Giá trị thật nằm ở vòng kiểm soát chất lượng: lint đều đặn, phát hiện mâu thuẫn, dọn trang mồ côi, lấp khoảng trống. Một hệ thống OKF LLM-wiki mạnh không phải hệ thống có cấu trúc file đẹp nhất, mà là hệ thống có kỷ luật bảo trì tốt nhất. Khi thiết kế, hãy đầu tư vào workflow lint trong file schema ngang với ingest và query.

## Xem thêm

- [design-playbook](design-playbook.md) - workflow LINT và checklist hệ thống vững.
- [llm-wiki-concept](llm-wiki-concept.md) - vì sao bookkeeping là phần cốt lõi.
