---
type: Reference
title: "Q&A nội bộ: Backend hybrid-engine vs pipeline, tiếng Việt/Anh, và cách MinerU giữ cấu trúc"
description: "> NGUỒN: Đây KHÔNG phải tài liệu chính thức của MinerU."
timestamp: 2026-07-06T03:34:16Z
---
# Q&A nội bộ: Backend hybrid-engine vs pipeline, tiếng Việt/Anh, và cách MinerU giữ cấu trúc

> NGUỒN: Đây KHÔNG phải tài liệu chính thức của MinerU. Đây là tài liệu Q&A nội bộ do người dùng và trợ lý soạn từ một phiên làm việc thực tế (benchmark ngày 2026-07-03), có đối chiếu với tài liệu chính thức (context7 `/opendatalab/mineru`) và kiểm chứng bằng dữ liệu độc lập (SSI iBoard). Khi trả lời, hãy phân biệt rõ: phần nào là kết luận đo đạc thực nghiệm trên một máy/một phiên bản cụ thể, phần nào trùng khớp với tài liệu chính thức. Nếu câu hỏi thuần về cú pháp/tính năng chính thức, ưu tiên các file `MinerU-*.md` (docs gốc) trước file này.
>
> BỐI CẢNH ĐO ĐẠC: máy Windows 11, GPU NVIDIA RTX A2000 8GB, CUDA Toolkit 13.3, MinerU bản 3.4.0 cài trong venv. Tài liệu test: báo cáo tài chính scan tiếng Việt (MWG Quý 1/2026, 43 trang, không có text layer).
>
> CẬP NHẬT 2026-07-04: bổ sung Q7 (đối chứng mù 9 số dấu phẩy R1) và Q8 (soát 2 con dấu R2) - khép hẳn hai nghi vấn chất lượng cuối cùng.

## Q1. hybrid-engine và pipeline khác nhau về bản chất thế nào?

Đây là hai triết lý đọc tài liệu khác nhau:

- **pipeline**: kiểu OCR cổ điển, chia thành một dây chuyền nhiều model chuyên biệt, mỗi model làm một việc: dò bố cục trang, dò vị trí chữ, nhận diện chữ theo từng bộ ngôn ngữ cụ thể (dựa trên họ PaddleOCR), thêm model dò bảng (wired/wireless), dò con dấu. Điểm yếu: model nhận diện chữ phải chọn đúng "bộ chữ cái" qua cờ `-l/--lang`.
- **hybrid-engine**: kết hợp bước dò bố cục cổ điển VỚI một mô hình thị giác-ngôn ngữ lớn (VLM, kiểu Qwen2-VL), chạy qua lmdeploy/turbomind trên GPU. VLM đa ngữ sẵn, không cần chọn bộ chữ cái, hiểu ngữ cảnh. Tên "hybrid" (lai) là vì trộn hai cách này. Đây là backend mặc định MinerU khuyến nghị.
- (Còn `vlm-engine` = thuần VLM, không kèm dò bố cục cổ điển; và các biến thể `*-http-client` để đẩy tính toán sang máy chủ khác.)

## Q2. Vì sao tiếng Việt phải dùng hybrid-engine, không dùng pipeline?

Vì pipeline làm rụng hết dấu tiếng Việt (ví dụ "TÀI SẢN" thành "TÀI SÀN", "THUẾ" thành "Thu"), trong khi hybrid-engine giữ đúng dấu.

Nguyên nhân gốc (kiểm chứng qua `mineru --help` trên bản cài 3.4.0): cờ `-l/--lang` của pipeline chỉ liệt kê `ch, ch_server, korean, ta, te, ka, th, el, arabic, east_slavic, cyrillic, devanagari`, mặc định `ch`. Không có tiếng Việt, cũng không có tùy chọn Latin chung nào. Tức bản này của pipeline không có model OCR đọc được chữ Latin có dấu; chỉnh cờ ngôn ngữ kiểu gì cũng không cứu được. hybrid-engine/vlm dùng VLM đa ngữ nên không vướng vấn đề này.

LƯU Ý PHIÊN BẢN (quan trọng, tránh nói quá): tài liệu chính thức MinerU (bản mới hơn) cho thấy danh sách `--lang` có thêm `en` và `latin`. Nghĩa là kết luận "pipeline không làm được tiếng Việt" chỉ đúng chắc chắn cho bản đang cài (3.4.0) tại thời điểm test; bản MinerU mới hơn có thể bổ sung `latin` giúp pipeline đọc được chữ Latin có dấu. Khi tư vấn, nên nói rõ điều này là đặc thù phiên bản.

Hệ quả thực dụng: pipeline KHÔNG phải phương án dự phòng cho VĂN BẢN tiếng Việt trên bản này. Nó chỉ dùng để vớt vát SỐ LIỆU (các con số vẫn đúng 100%, chỉ chữ mất dấu) khi hybrid-engine không chạy được vì lỗi GPU/CUDA/turbomind. Khi gặp lỗi đó, cách đúng là sửa lại turbomind, không phải chuyển hẳn sang pipeline.

## Q3. Với PDF tiếng Anh thì dùng backend nào?

Với tiếng Anh, lý do cấm pipeline ở tiếng Việt không còn đúng: tiếng Anh không có dấu phụ, chỉ là chữ Latin cơ bản a-z/A-Z/số, mà model mặc định `ch` của pipeline vốn bao gồm sẵn chữ và số Latin. Nên pipeline đọc tiếng Anh tốt.

Khác biệt còn lại không nằm ở chữ mà ở bố cục:
- Tài liệu tiếng Anh đơn giản (một cột, ít bảng): cả hai backend đều tốt; pipeline còn có lợi thế nhẹ và bền hơn (không phụ thuộc turbomind), chạy được cả khi GPU trục trặc.
- Tài liệu tiếng Anh phức tạp (bảng gộp ô, nhiều cột, bố cục dày): vẫn nên hybrid-engine, vì chỗ pipeline làm xô lệch trong test là cấu trúc bảng gộp ô - lỗi này thuộc xử lý bố cục, không liên quan ngôn ngữ, nên vẫn xảy ra với tiếng Anh.

Khuyến nghị đơn giản: giữ hybrid-engine làm mặc định cho tất cả (Anh lẫn Việt) để chỉ có một quy tắc; chỉ cân nhắc pipeline cho tiếng Anh khi GPU/turbomind hỏng hoặc tài liệu chỉ toàn chữ đơn giản và muốn luồng nhẹ. (Lưu ý: nhận định về tiếng Anh này suy ra từ benchmark tiếng Việt cộng nguyên nhân gốc, chưa chạy test tiếng Anh trực tiếp.)

## Q4. Tốc độ hai backend thế nào?

Trên máy test, mỗi backend xử lý 5 trang rơi vào khoảng 1 đến 3 phút, đã tính thời gian nạp model. Không đưa con số "trang/giây" vì mẫu nhỏ và tốc độ phụ thuộc nội dung (trang nhiều bảng lâu hơn hẳn trang chỉ có chữ).

Chi tiết đáng biết:
- Lần chạy đầu luôn nặng nhất do nạp model (hybrid mất ~13 giây dựng turbomind; pipeline lần đầu còn tải thêm model dò con dấu ~30 giây, chỉ một lần rồi lưu lại).
- Với hybrid, bước tốn thời gian nhất là dò/trích bố cục từng vùng trên trang.
- Ở quy mô nhỏ, hai backend cùng cấp độ tốc độ, không chênh đủ để chọn dựa trên tốc độ. Nên chọn theo chất lượng (hybrid cho tiếng Việt).

## Q5. MinerU xử lý bảng biểu, hình ảnh, biểu đồ ra sao (so với pdfplumber làm vỡ cấu trúc)?

Điểm cốt lõi cần hiểu đúng: MinerU làm HAI việc tách bạch nhau.

1. Lấy nội dung CHỮ trong khối văn bản: đây là cái `-m auto|txt|ocr` quyết định. `txt` = lấy thẳng từ lớp chữ có sẵn của PDF (nhanh, chính xác tuyệt đối); `ocr` = đọc chữ từ ảnh; `auto` = tự chọn theo từng trang. Với PDF có sẵn chữ thì phần chữ được trích gần như tức thì, khỏi OCR.
2. HIỂU BỐ CỤC trang: luôn chạy, bất kể việc 1 dùng txt hay ocr. Đây mới là thứ khiến MinerU hơn hẳn pdfplumber.

Vì sao đây là khác biệt cốt tử: trong file PDF gốc, "bảng" không được lưu dưới dạng lưới ô - nó chỉ là các chữ đặt ở tọa độ x,y, không có thông tin ô nào thuộc dòng/cột nào. pdfplumber chỉ đổ luồng chữ theo thứ tự nội bộ nên bảng vỡ, biểu đồ mất. MinerU phải nhìn ảnh render của trang bằng model thị giác để dựng lại lưới ô. Vì vậy dù PDF đã có sẵn chữ, MinerU vẫn "nhìn" trang để hiểu bảng.

Theo tài liệu chính thức MinerU, phần hiểu bố cục luôn: dựng bảng thành HTML có cấu trúc ô đầy đủ (gộp dòng/cột, kể cả bảng nối qua nhiều trang); cắt hình/ảnh ra thành file ảnh riêng và nhúng vào kết quả kèm tiêu đề/chú thích hình; chuyển công thức thành LaTeX; sắp xếp theo đúng thứ tự đọc của người; tự loại đầu trang/chân trang. Hai cờ `-t/--table` và `-f/--formula` mặc định bật, độc lập với `-m method`.

Riêng BIỂU ĐỒ (chart) cần nói rõ để không kỳ vọng sai:
- Mặc định, biểu đồ được xử lý như một tấm hình: cắt ra và nhúng dưới dạng ảnh. MinerU KHÔNG tự biến biểu đồ thành số liệu/bảng.
- Muốn máy đọc hiểu nội dung biểu đồ (mô tả bằng lời, hoặc cố rút số), phải bật phân tích ảnh/biểu đồ, tức chạy hybrid với `--effort high` (mặc định `medium` tắt phân tích ảnh/biểu đồ cho nhanh). Đổi lại chậm hơn.
- Với báo cáo tài chính thường không cần, vì số liệu nằm ở bảng chứ không ở biểu đồ.

## Q6. Độ chính xác thực đo trên báo cáo tài chính scan tiếng Việt

Benchmark trên MWG Q1/2026 (scan thuần, đối chứng với dữ liệu độc lập SSI iBoard):
- Ba báo cáo tài chính (CĐKT, KQKD, LCTT): cả hai backend khớp 100% số liệu (18/18 chỉ tiêu chính) với nguồn độc lập. hybrid-engine giữ đúng dấu tiếng Việt và cấu trúc bảng phức tạp (rowspan); pipeline đúng số nhưng mất dấu và xô lệch bảng gộp ô.
- 5 trang thuyết minh ngẫu nhiên (đối chứng bằng 5 tác nhân đọc ảnh độc lập): khớp gần tuyệt đối. Lỗi duy nhất: cả hai backend đọc một số "267.633.483" thành "267,633,483" (nhầm dấu chấm/phẩy phân cách hàng nghìn) - không phải sai chữ số, chỉ sai ký hiệu phân cách.

Bài học vận hành: nếu parse số từ output MinerU bằng script, cần chuẩn hóa mọi dấu phân cách hàng nghìn về "." trước khi parse (với số tiền VND vốn là số nguyên, dấu phân cách luôn là chấm), đừng tin tuyệt đối ký hiệu dấu câu trong output.

## Q7. Kiểm chứng chuyên sâu R1: 9 số dính dấu phẩy có sai chữ số nào không? (2026-07-04)

Benchmark ban đầu (Q6) soát mẫu 5 trang, ước lượng "1 lỗi dấu phân cách". Khi quét TOÀN VĂN 43 trang bằng regex, phát hiện thật ra có 9 lượt số dính dấu phẩy (trang 36-38 của PDF, tức page_idx 35-37 trong content_list.json). Cần kiểm: dấu phẩy chỉ sai ký hiệu (chữ số đúng), hay sai cả chữ số?

Phương pháp kiểm (ba con đường độc lập, không dùng kết quả MinerU làm đáp án):

1. **Đối chứng mù bằng vision**: 3 agent độc lập đọc trang scan gốc ở 400-600dpi (render qua PyMuPDF), không biết MinerU đọc ra cái gì. Chép nguyên trạng từng ô, phóng to 3x-12x để phân biệt dấu chấm/phẩy.
2. **Kiểm số học nội bảng**: cả 9 số đều nằm trong bảng có dòng tổng/cộng dồn. Tính lại mọi phép cộng/trừ xem có khớp.
3. **Kiểm hiệu hai cột**: 6/9 số nằm ở cột KQKD của bảng thuế hoãn lại (trang 37); mỗi số bằng hiệu hai cột cân đối kế toán cùng dòng (hai cột này in bằng dấu chấm, hoàn toàn độc lập với cột R1).

Kết quả: **9/9 đúng từng chữ số.** Và phát hiện quan trọng: dấu phẩy nằm NGAY TRONG BẢN IN GỐC. Tài liệu MWG trộn hai kiểu phân cách (toàn bộ cột KQKD trang 37 in bằng dấu phẩy, cùng bảng các cột khác in dấu chấm; trang 38 dòng TỔNG CỘNG cột Lỗ thuế in bằng dấu phẩy nhưng cùng dòng cột khác in dấu chấm). Đây KHÔNG phải lỗi OCR - MinerU chép trung thực bản in. Phần benchmark cũ (Q6) ghi "nhầm dấu chấm/phẩy" là chưa chính xác; bản in gốc đã in bằng dấu phẩy sẵn.

Phát hiện phụ: bản in gốc của MWG tự mâu thuẫn 2 đồng ở dòng "Lợi nhuận chưa thực hiện" trang 37. Hiệu hai cột cân đối kế toán: 8.945.978.659 - 11.149.953.660 = -2.203.975.001; nhưng số in ở cột KQKD là (2,203,974,999). Tổng cột KQKD lại khớp đúng với 226.984.924.968 nếu dùng 2.203.974.999, tức bản in gốc ưu tiên tổng đúng và chấp nhận lệch 2 đồng ở chi tiết. Hai lượt đọc độc lập (MinerU và vision) cho cùng kết quả - lỗi thuộc về tài liệu, không phải trích xuất.

Ý nghĩa vận hành: xác nhận MinerU hybrid-engine 3.4.0 không làm sai một chữ số nào trên tài liệu test này. Quy tắc chuẩn hóa dấu phẩy thành dấu chấm khi đưa vào wiki vẫn cần (vì bản in gốc trộn hai kiểu), nhưng bản chất không phải sửa lỗi OCR mà là chuẩn hóa định dạng bản in.

## Q8. Kiểm chứng R2: con dấu đè chữ - MinerU có mất nội dung không? (2026-07-04)

Content_list.json ghi nhận 2 khối `sub_type: "seal"` ở trang 9 và trang 35 (đánh số từ 1). Agent vision đọc trang gốc để xác minh:

**Trang 35**: hai vệt dấu giáp lai nằm sát mép phải trang (phần lớn thân dấu ngoài mép giấy, chỉ in cung tròn bên trái). Nằm gọn trong lề trắng, KHÔNG đè chữ hay con số nào. Không mất nội dung.

**Trang 9**: con dấu tròn đỏ hoàn chỉnh, đóng chồng lên chữ ký Tổng Giám đốc theo đúng lệ (dấu đè 1/3 chữ ký). MinerU tách con dấu thành ảnh riêng (đúng: đây là ảnh, không phải chữ). Tuy nhiên MinerU BỎ SÓT:
- Tên người ký thứ ba "Vũ Đăng Linh" cùng chức danh "Tổng Giám đốc" (nằm sát dưới mép dưới con dấu, bị gộp vào vùng ảnh con dấu nên rơi khỏi lớp chữ).
- Dòng địa danh "Thành phố Hồ Chí Minh, Việt Nam" (nằm sát mép trên con dấu).
- Hai người ký còn lại (Nguyễn Thu Thủy - Người lập, Lý Trần Kim Ngân - Kế toán trưởng) MinerU trích đầy đủ vì nằm xa con dấu.

Ý nghĩa: đây là đặc tính đã biết của MinerU khi xử lý con dấu - vùng ảnh con dấu "nuốt" luôn chữ xung quanh nếu nằm sát mép. Chỉ mất metadata chữ ký (tên người, chức danh, ngày), KHÔNG mất số liệu tài chính. Khi trích xuất tài liệu có dấu và chữ ký, nên biết rằng thông tin vùng này có thể không đầy đủ trong lớp chữ - nếu cần chính xác tên/chức danh người ký, phải mở ảnh con dấu (trong thư mục images/ của output) để đọc bổ sung bằng vision.
