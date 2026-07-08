---
type: Concept
title: Mẫu hình LLM-wiki của Karpathy
description: Giải thích đầy đủ mẫu hình LLM-wiki mà Andrej Karpathy đề xuất - kiến trúc ba lớp, ba thao tác ingest/query/lint, và lý do nó khác RAG - vốn là nền tư tưởng mà OKF chính thức hóa.
tags:
  - llm-wiki
  - karpathy
  - concept
  - memex
  - agent-memory
timestamp: 2026-07-03T00:00:00Z
source: Diễn giải từ file nguồn verbatim cùng thư mục source-llm-wiki-gist.md (gist Andrej Karpathy).
---

# Mẫu hình LLM-wiki của Karpathy

Concept này diễn giải gist "LLM Wiki" của Andrej Karpathy - nguồn tư tưởng mà [OKF](okf-spec-explained.md) chính thức hóa thành một đặc tả. Bản gốc verbatim nằm ở [source-llm-wiki-gist.md](source-llm-wiki-gist.md). Bản thân gist tự nhận là một "idea file" trừu tượng, thiết kế để bạn dán vào agent của mình rồi cùng agent dựng ra chi tiết cụ thể.

## Ý tưởng cốt lõi

Trải nghiệm phổ biến của người dùng với LLM và tài liệu là RAG: bạn tải lên một mớ file, LLM truy hồi các mẩu liên quan lúc hỏi, rồi sinh câu trả lời. Cách này chạy được, nhưng LLM tái khám phá tri thức từ đầu ở mỗi câu hỏi. Không có tích lũy. Hỏi một câu tinh tế cần tổng hợp năm tài liệu, LLM phải đi tìm và ghép lại các mảnh mỗi lần. NotebookLM, tải file lên ChatGPT, và phần lớn hệ RAG đều hoạt động kiểu này.

Ý tưởng ở đây khác: thay vì chỉ truy hồi từ tài liệu thô lúc hỏi, LLM tăng dần xây và bảo trì một cuốn wiki bền vững - một tập file markdown có cấu trúc, liên kết chéo, nằm giữa bạn và các nguồn thô. Khi thêm nguồn mới, LLM không chỉ đánh chỉ mục để truy hồi sau. Nó đọc, rút thông tin then chốt, và tích hợp vào wiki đang có: cập nhật trang thực thể, sửa lại tóm tắt chủ đề, ghi chú nơi dữ liệu mới mâu thuẫn với khẳng định cũ, củng cố hoặc thách thức phần tổng hợp đang tiến hóa. Tri thức được biên soạn một lần rồi giữ tươi, không phải suy lại ở mỗi truy vấn.

Đây là khác biệt then chốt: cuốn wiki là một artifact bền vững, cộng dồn (persistent, compounding). Các cross-reference đã có sẵn. Các mâu thuẫn đã được đánh dấu. Phần tổng hợp đã phản ánh mọi thứ bạn đã đọc. Wiki cứ giàu thêm với mỗi nguồn bạn thêm và mỗi câu bạn hỏi.

Bạn gần như không bao giờ tự viết wiki - LLM viết và bảo trì toàn bộ. Bạn phụ trách sourcing, khám phá, và đặt câu hỏi đúng. LLM làm mọi việc nặng nhọc: tóm tắt, cross-reference, sắp xếp, và ghi chép sổ sách vốn là thứ làm một kho tri thức thực sự hữu ích theo thời gian. Câu ví von nổi tiếng của Karpathy: Obsidian là IDE, LLM là lập trình viên, wiki là codebase.

## Các bối cảnh áp dụng

Mẫu hình này áp dụng rộng:

- Cá nhân: theo dõi mục tiêu, sức khỏe, tâm lý, tự cải thiện - sắp xếp nhật ký, bài báo, ghi chú podcast thành một bức tranh có cấu trúc về chính mình.
- Nghiên cứu: đào sâu một chủ đề qua nhiều tuần hoặc tháng, đọc paper và báo cáo, dựng dần một wiki toàn diện với luận điểm tiến hóa.
- Đọc sách: sắp xếp từng chương, dựng trang cho nhân vật, chủ đề, mạch truyện. Kiểu fan wiki như Tolkien Gateway - hàng ngàn trang liên kết dựng qua nhiều năm - nhưng bạn tự dựng khi đọc, LLM lo hết cross-reference.
- Business/team: một wiki nội bộ do LLM bảo trì, nạp từ Slack thread, transcript họp, tài liệu dự án, cuộc gọi khách. Có thể có người review. Wiki luôn tươi vì LLM làm phần bảo trì không ai trong nhóm muốn làm.
- Phân tích cạnh tranh, thẩm định (due diligence), lập kế hoạch chuyến đi, ghi chú khóa học, đào sâu sở thích - bất cứ đâu bạn tích lũy tri thức theo thời gian và muốn nó có tổ chức thay vì rải rác.

## Kiến trúc ba lớp

- Raw sources (nguồn thô): bộ tài liệu nguồn bạn tuyển chọn - bài báo, paper, ảnh, file dữ liệu. Chúng bất biến: LLM đọc từ đó nhưng không bao giờ sửa. Đây là nguồn chân lý.
- The wiki: một thư mục các file markdown do LLM sinh - tóm tắt, trang thực thể, trang khái niệm, so sánh, tổng quan, tổng hợp. LLM sở hữu lớp này hoàn toàn: tạo trang, cập nhật khi có nguồn mới, giữ cross-reference, giữ mọi thứ nhất quán. Bạn đọc, LLM viết.
- The schema: một tài liệu (ví dụ `CLAUDE.md` cho Claude Code hoặc `AGENTS.md` cho Codex) nói cho LLM biết wiki được tổ chức thế nào, quy ước là gì, và workflow nào phải theo khi ingest nguồn, trả lời câu hỏi, hay bảo trì. Đây là file cấu hình then chốt - chính nó biến LLM từ một chatbot chung chung thành một người bảo trì wiki có kỷ luật. Bạn và LLM cùng tiến hóa file này theo thời gian khi hiểu ra cái gì hợp với miền của mình.

## Ba thao tác vận hành

Ingest (nạp). Bạn thả một nguồn mới vào bộ raw và bảo LLM xử lý. Một luồng ví dụ: LLM đọc nguồn, bàn với bạn các điểm rút ra, viết một trang tóm tắt trong wiki, cập nhật index, cập nhật các trang thực thể và khái niệm liên quan khắp wiki, và ghi một dòng vào log. Một nguồn có thể chạm 10 tới 15 trang wiki. Karpathy thích nạp từng nguồn một và giữ mình trong vòng lặp (đọc tóm tắt, kiểm tra cập nhật, hướng dẫn LLM nhấn mạnh gì), nhưng bạn cũng có thể nạp hàng loạt với ít giám sát hơn. Hãy tự phát triển workflow hợp phong cách của mình và ghi nó vào schema cho các phiên sau.

Query (truy vấn). Bạn hỏi wiki. LLM tìm các trang liên quan, đọc, và tổng hợp câu trả lời có trích dẫn. Câu trả lời có nhiều dạng: một trang markdown, một bảng so sánh, một bộ slide (Marp), một biểu đồ (matplotlib), một canvas. Ý quan trọng: câu trả lời tốt có thể được file ngược lại wiki thành trang mới. Một so sánh bạn yêu cầu, một phân tích, một mối liên hệ bạn phát hiện - những thứ này giá trị và không nên biến mất vào lịch sử chat. Nhờ vậy các lần khám phá của bạn cộng dồn vào kho tri thức đúng như nguồn được nạp.

Lint (rà soát). Định kỳ, bảo LLM kiểm tra sức khỏe wiki. Tìm: mâu thuẫn giữa các trang, khẳng định cũ đã bị nguồn mới thay thế, trang mồ côi không có link trỏ vào, khái niệm quan trọng được nhắc nhưng thiếu trang riêng, cross-reference thiếu, khoảng trống dữ liệu có thể lấp bằng một lần tìm web. LLM giỏi gợi ý câu hỏi mới để điều tra và nguồn mới để tìm. Việc này giữ wiki khỏe khi nó lớn lên.

## index.md và log.md

Hai file đặc biệt giúp cả LLM lẫn bạn điều hướng wiki khi nó lớn:

- `index.md` thiên về nội dung. Nó là catalog mọi thứ trong wiki - mỗi trang một link, một dòng tóm tắt, và tùy chọn metadata như ngày hay số nguồn. Tổ chức theo nhóm (thực thể, khái niệm, nguồn...). LLM cập nhật nó ở mỗi lần ingest. Khi trả lời, LLM đọc index trước để tìm trang liên quan rồi khoan sâu. Cách này chạy tốt bất ngờ ở quy mô vừa (khoảng 100 nguồn, vài trăm trang) và tránh được nhu cầu dựng hạ tầng RAG embedding.
- `log.md` thiên về thời gian. Nó là bản ghi chỉ-thêm về việc gì đã xảy ra và khi nào - ingest, query, lint. Mẹo hữu ích: nếu mỗi dòng bắt đầu bằng một tiền tố nhất quán (ví dụ `## [2026-04-02] ingest | Tên bài`), log trở nên phân tích được bằng unix tool đơn giản, ví dụ `grep "^## \[" log.md | tail -5` cho bạn 5 mục gần nhất. Log cho bạn dòng thời gian tiến hóa và giúp LLM hiểu gần đây đã làm gì.

## Vì sao mẫu hình này chạy được

Phần nhọc nhằn của việc bảo trì một kho tri thức không phải đọc hay suy nghĩ, mà là ghi chép sổ sách: cập nhật cross-reference, giữ tóm tắt tươi, ghi chú khi dữ liệu mới mâu thuẫn cái cũ, giữ nhất quán qua hàng chục trang. Con người bỏ rơi wiki vì gánh nặng bảo trì lớn nhanh hơn giá trị. LLM không chán, không quên cập nhật một cross-reference, và chạm 15 file trong một lượt. Wiki được bảo trì vì chi phí bảo trì gần bằng không.

Việc của con người: tuyển nguồn, định hướng phân tích, hỏi câu hỏi hay, và nghĩ xem tất cả có ý nghĩa gì. Việc của LLM: mọi thứ còn lại.

## Liên hệ Memex

Ý tưởng này gần tinh thần Memex của Vannevar Bush (1945) - một kho tri thức cá nhân, tuyển chọn, với các associative trails giữa tài liệu. Tầm nhìn của Bush gần cái này hơn là gần cái mà web đã trở thành: riêng tư, chủ động tuyển chọn, với các mối nối giữa tài liệu quý giá ngang bản thân tài liệu. Phần Bush không giải được là ai làm phần bảo trì. LLM lo phần đó.

## Mọi thứ đều tùy chọn và modular

Gist cố tình trừu tượng. Cấu trúc thư mục cụ thể, quy ước schema, định dạng trang, công cụ - tất cả tùy miền, sở thích, và LLM bạn chọn. Mọi thứ được nhắc đều tùy chọn: nguồn của bạn có thể chỉ là text nên không cần xử lý ảnh; wiki có thể đủ nhỏ để chỉ cần index không cần search engine; bạn có thể không cần slide. Cách dùng đúng là chia sẻ ý tưởng này với agent rồi cùng nhau tạo ra một phiên bản hợp nhu cầu của bạn.

## Xem thêm

- [okf-spec-explained](okf-spec-explained.md) - đặc tả chính thức hóa mẫu hình này.
- [design-playbook](design-playbook.md) - biến ý tưởng thành một hệ thống cụ thể, từng bước.
- [okf-vs-rag-graphrag](okf-vs-rag-graphrag.md) - vì sao cách này khác RAG, và khi nào phối hợp.
