# Báo cáo Chuyên sâu về Hermes Agent Harness: Kiến trúc và Phản biện Hệ thống

Bản báo cáo này tổng hợp chi tiết toàn bộ cấu trúc vận hành của hệ thống Hermes Agent Harness, đồng thời đưa ra những phân tích sâu sắc dựa trên các phản biện kỹ thuật:

## 1. Vòng lặp Harness và Hệ thống công cụ cục bộ
Phân tích cơ chế kiểm soát LLM thông qua vòng lặp "dây cương" (Harness) để tự động hóa tác vụ mà không cần sự can thiệp liên tục của con người. Hệ thống sử dụng các công cụ mạnh mẽ như Terminal, Browser, Cron Job và cơ chế ủy quyền song song cho các Sub-agent (ví dụ như gọi Claude CLI để viết và chạy mã Python).

## 2. Ba loại bộ nhớ phân cấp
Hệ thống lưu trữ bộ nhớ được chia làm 3 tầng:
*   **Bộ nhớ quy trình (Procedure Memory)**: Lưu trữ các kỹ năng dưới dạng tệp Markdown tại thư mục cục bộ `hermes/skills/` (ví dụ thực tế về kỹ năng định dạng video `video prep`).
*   **Bộ nhớ ngữ nghĩa (Semantic Memory)**: Lưu các sự thật bền vững của người dùng vào tệp văn bản thuần `memory.md`.
*   **Bộ nhớ sự kiện (Episodic Memory)**: Lưu trữ toàn bộ lịch sử trò chuyện trong cơ sở dữ liệu SQLite cục bộ `state.db`.

## 3. Giải đáp và phân tích phản biện
*   **Tại sao chỉ dùng tìm kiếm từ khóa Top-K thay vì Embeddings**: Hermes thực sự chỉ sử dụng văn bản thuần và tìm kiếm từ khóa Top-K. Lựa chọn này giúp hệ thống vận hành cực kỳ nhẹ nhàng và minh bạch ngay trên máy cục bộ, dù có thể gặp hạn chế về khả năng hiểu ngữ nghĩa đồng nghĩa.
*   **Cơ chế tóm tắt an toàn của mô hình phụ trợ**: Quy trình nén lịch sử chat diễn ra "theo thời gian" (over time) bằng các mô hình phụ trợ giá rẻ (auxiliary models) để chắt lọc thông tin từ `state.db` sang `memory.md`. Hệ thống đảm bảo quyền riêng tư nhờ lưu trữ 100% cục bộ, tuy nhiên tài liệu gốc không cung cấp thêm các thiết lập an toàn hay điều kiện kích hoạt kỹ thuật cụ thể nào khác để tránh "ảo tưởng" (hallucinations).
*   **Tính năng tự học kỹ năng mới (Self-Improving Skills)**: Tính năng tự học kỹ năng **chưa thực sự tự hoạt động** trong thực tế thử nghiệm. Agent mới chỉ tự động học và sửa lỗi bộ nhớ ngữ nghĩa khi gặp sự cố (ví dụ ghi nhận lỗi *"YouTube scraping quirk"* sau khi nhập sai URL). Các kỹ năng xử lý công việc phức tạp hiện tại vẫn cần người dùng ra lệnh tạo lập một cách thủ công.
