---
type: Reference
title: OKF LLM-wiki đối chiếu RAG và GraphRAG
description: So sánh ba cách trao ngữ cảnh cho agent - RAG, OKF LLM-wiki, GraphRAG - kèm khi nào dùng cái nào và cách phối hợp trong một hệ thống.
tags:
  - okf
  - rag
  - graphrag
  - lightrag
  - comparison
timestamp: 2026-07-03T00:00:00Z
source: Tổng hợp nghiên cứu; đối chiếu ý RAG-vs-wiki trong source-llm-wiki-gist.md cùng thư mục.
---

# OKF LLM-wiki đối chiếu RAG và GraphRAG

Concept này trả lời câu hỏi thực dụng nhất khi thiết kế: nên dùng RAG, OKF LLM-wiki, hay GraphRAG, và có thể phối hợp không. Đây không phải cuộc đấu một mất một còn.

## Ba cách tiếp cận

RAG cổ điển. Lúc hỏi mới truy hồi các mẩu văn bản theo độ tương đồng vector, nhồi vào cửa sổ ngữ cảnh, rồi sinh câu trả lời. Như [gist Karpathy](source-llm-wiki-gist.md) nói: LLM tái khám phá tri thức từ đầu ở mỗi câu hỏi, không tích lũy. Mạnh khi kho tài liệu khổng lồ, phi cấu trúc, và bạn cần tìm động.

OKF LLM-wiki. Trao cho agent một đồ thị đã cấu trúc sẵn để nó đi lại có chủ đích (traverse deliberately). Việc tổng hợp làm một lần lúc nạp và giữ bền: cross-reference và mâu thuẫn đã xử lý trước. Mạnh khi tri thức đã được tuyển chọn và lặp đi lặp lại - lược đồ bảng, định nghĩa chỉ số, join path, so tay quy trình.

GraphRAG. Trích xuất một đồ thị tri thức (thực thể và quan hệ) từ tài liệu, thường nạp vào một cơ sở dữ liệu đồ thị chuyên dụng, rồi truy vấn theo đồ thị. Điểm chung với OKF: cả hai dùng cấu trúc quan hệ tường minh thay vì chỉ dựa vào tương đồng ngữ nghĩa mờ. Khác biệt: GraphRAG thường giữ đồ thị trong graph DB; OKF giữ đồ thị ở dạng file markdown phẳng mà con người đọc và sửa được, Git quản được - các cross-link chính là cạnh của đồ thị.

## Bảng so sánh

| Tiêu chí | RAG | OKF LLM-wiki | GraphRAG |
|----------|-----|--------------|----------|
| Cơ chế lưu tri thức | Vector trong DB | File markdown có cấu trúc | Đồ thị trong graph DB |
| Thời điểm tổng hợp | Mỗi lần hỏi | Một lần lúc nạp, giữ bền | Lúc trích xuất đồ thị |
| Cách truy xuất | Tương đồng vector | Duyệt index và cross-link | Duyệt quan hệ trong đồ thị |
| Con người đọc/sửa trực tiếp? | Khó (vector mờ) | Dễ (markdown thuần) | Trung bình (cần công cụ) |
| Khi nào chọn | Kho lớn, phi cấu trúc, tra long-tail | Tri thức tuyển chọn, quan hệ, dùng lại nhiều | Cần suy luận nhiều bước theo quan hệ |
| Điểm yếu | Không tích lũy, ghép lại mỗi lần | Cần bảo trì (LLM lo), search yếu khi rất lớn | Hạ tầng nặng, trích xuất đồ thị tốn công |

## Cách phối hợp trong một hệ thống

Nhiều kiến trúc agent chạy cả hai lớp cùng lúc:

- Dùng OKF cho ngữ cảnh quan hệ, có cấu trúc, dùng lại thường xuyên: lược đồ, chỉ số, quy trình. Câu hỏi nhị phân kiểu "X có Y không" hoặc "nối X với Y thế nào" thì wiki trả lời gọn và chắc.
- Dùng RAG truy hồi cho phần đuôi dài, tra cứu ngẫu nhiên trong khối tài liệu lớn mà chưa kịp đưa vào wiki.

Cách nghĩ đúng: OKF là bộ nhớ làm việc có tổ chức của agent; RAG là kho lưu trữ rộng để với tới khi wiki chưa phủ. Khi một câu trả lời từ RAG tỏ ra giá trị lâu dài, hãy file nó vào wiki (xem workflow query trong [design-playbook](design-playbook.md)) để lần sau khỏi truy hồi lại.

## Liên hệ LightRAG

LightRAG vốn trộn đồ thị với truy hồi, nên là điểm hội tụ tự nhiên để thử nghiệm ý tưởng wiki do agent bảo trì: bạn có thể để phần đồ thị đóng vai OKF bundle (quan hệ tường minh, con người kiểm soát) và phần truy hồi lo đuôi dài. Với ai đang nghiên cứu RAG/GraphRAG/LightRAG, OKF vừa là đối thủ, vừa là bạn đồng hành, vừa là một cách hiện thực GraphRAG bằng markdown mà con người kiểm soát được.

## Xem thêm

- [llm-wiki-concept](llm-wiki-concept.md) - vì sao mẫu hình wiki khác RAG.
- [design-playbook](design-playbook.md) - cách dựng hệ thống, gồm khi nào bật RAG song song.
