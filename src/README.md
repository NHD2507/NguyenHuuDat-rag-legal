# ⚖️ Legal RAG Assistant

## 1. Giới thiệu

Legal RAG Assistant là hệ thống hỏi đáp văn bản pháp luật sử dụng kỹ thuật Retrieval-Augmented Generation (RAG).

Hệ thống cho phép người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên về nội dung của văn bản pháp luật. Thay vì đưa toàn bộ tài liệu vào mô hình ngôn ngữ, hệ thống sẽ truy xuất các đoạn văn liên quan nhất từ cơ sở tri thức trước khi gửi cho Gemini để sinh câu trả lời.

### Bộ tri thức hiện tại

- Nghị định 113/2017/NĐ-CP
- Quy định chi tiết và hướng dẫn thi hành một số điều của Luật Hóa chất

---

# 2. Tính năng

## Đã triển khai

- Đọc dữ liệu từ PDF
- Chia nhỏ tài liệu thành các chunk
- Sinh embedding cho từng chunk
- Lưu trữ vector bằng ChromaDB
- Tìm kiếm ngữ nghĩa (Semantic Search)
- Sinh câu trả lời bằng Gemini
- Hiển thị nguồn tham khảo theo trang
- Giao diện chat bằng Streamlit
- Cache dữ liệu để tăng hiệu năng
- Threshold kiểm soát hallucination

---

# 3. Cấu trúc thư mục

```text
rag-test/
│
├── app.py
├── data/
│   └── legal_document.pdf
│
├── chroma_db/
│
├── src/
│   ├── ingestion.py
│   ├── embedding.py
│   ├── retriever.py
│   ├── generator.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# 4. Hướng dẫn cài đặt

## Yêu cầu

- Python 3.11+
- pip

## Clone project

```bash
git clone <repository_url>
cd rag-test
```

## Tạo môi trường ảo

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / MacOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## Cài thư viện

```bash
pip install -r requirements.txt
```

---

# 5. Cấu hình môi trường

Tạo file `.env`:

```env
GEMINI_API_KEY=your_api_key
```

---

# 6. Chạy chương trình

```bash
streamlit run app.py
```

Sau khi chạy:

```text
http://localhost:8501
```

---

# 7. Kiến trúc hệ thống

```text
PDF
 │
 ▼
Load dữ liệu
 │
 ▼
Chunking
 │
 ▼
Embedding
 │
 ▼
ChromaDB
 │
 ▼
Retriever
 │
 ▼
Context
 │
 ▼
Gemini
 │
 ▼
Câu trả lời
```

## Luồng xử lý

1. Đọc dữ liệu từ PDF.
2. Chia tài liệu thành các chunk.
3. Sinh vector embedding cho từng chunk.
4. Lưu vector vào ChromaDB.
5. Người dùng nhập câu hỏi.
6. Retriever tìm Top-K chunk liên quan.
7. Context được gửi đến Gemini.
8. Gemini sinh câu trả lời dựa trên context.
9. Hiển thị câu trả lời và nguồn tham khảo.

---

# 8. Các quyết định kỹ thuật và Trade-off

## 8.1 Embedding Model

Sử dụng:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

### Lý do

- Hỗ trợ tiếng Việt
- Chạy local
- Miễn phí
- Tốc độ nhanh

### Trade-off

Ưu điểm:

- Dễ triển khai
- Không phát sinh chi phí API

Nhược điểm:

- Chất lượng retrieval thấp hơn BGE-M3 hoặc E5-Large

---

## 8.2 Vector Database

Sử dụng:

```text
ChromaDB
```

### Lý do

- Dễ cài đặt
- Không cần server riêng
- Phù hợp bài toán nhỏ và vừa

### Trade-off

Ưu điểm:

- Setup nhanh
- Chạy local

Nhược điểm:

- Không tối ưu cho tập dữ liệu rất lớn

---

## 8.3 Chunk Size

```text
Chunk Size = 1000
Chunk Overlap = 150
```

### Lý do

Giữ được ngữ cảnh pháp lý đầy đủ giữa các điều khoản.

### Trade-off

Chunk lớn:

- Tốn token hơn
- Retrieval chậm hơn

Chunk nhỏ:

- Mất ngữ nghĩa
- Giảm độ chính xác

---

## 8.4 Threshold

```text
Threshold = 4.0
```

### Lý do

Ngăn hệ thống trả lời các câu hỏi không liên quan tới tài liệu.

Ví dụ:

```text
Thời tiết hôm nay thế nào?
```

Kết quả:

```text
Không tìm thấy thông tin trong tài liệu.
```

---

## 8.5 Chiến lược Chunking

Sử dụng:

```text
Tách theo Điều
```

### Lý do

Văn bản pháp luật được tổ chức theo Điều và Khoản.

Việc chunk theo Điều giúp tăng độ chính xác khi truy xuất.

---

# 9. Ví dụ sử dụng

## Câu hỏi hợp lệ

```text
Điều 1 quy định gì?

Điều kiện sản xuất hóa chất là gì?

Kho chứa hóa chất cần đáp ứng những yêu cầu nào?
```

## Câu hỏi ngoài phạm vi

```text
Thời tiết hôm nay thế nào?

Công thức nấu phở bò?

Ai là tổng thống Mỹ?
```

Kết quả mong đợi:

```text
Không tìm thấy thông tin trong tài liệu.
```

---

# 10. Hạn chế hiện tại

- Chỉ hỗ trợ một tài liệu PDF
- Chưa hỗ trợ OCR cho PDF scan
- Chưa có Hybrid Search (BM25 + Embedding)
- Chưa có Reranking
- Chưa hỗ trợ upload PDF từ giao diện
- Chưa hỗ trợ đa người dùng

---

# 11. Hướng phát triển

## Retrieval

- Hybrid Search (BM25 + Embedding)
- Cross Encoder Reranking

## Data

- Hỗ trợ nhiều tài liệu
- Hỗ trợ PDF Scan

## UI/UX

- Upload PDF trực tiếp
- Citation theo đoạn văn
- Streaming response

## Production

- Docker
- Authentication
- Logging
- Monitoring

---

# 12. Mô tả các hàm chính

## load_pdf(pdf_path)

### Mô tả

Đọc PDF và trích xuất văn bản theo từng trang.

### Tham số

```python
pdf_path: str
```

### Trả về

```python
List[Dict]
```

---

## create_chunks(pages)

### Mô tả

Chia tài liệu thành các chunk phục vụ retrieval.

### Tham số

```python
pages: List[Dict]
```

### Trả về

```python
List[Dict]
```

---

## add_documents(chunks)

### Mô tả

Sinh embedding và lưu vào ChromaDB.

### Tham số

```python
chunks: List[Dict]
```

### Trả về

```python
None
```

---

## retrieve(query)

### Mô tả

Tìm kiếm các chunk liên quan nhất đến câu hỏi.

### Tham số

```python
query: str
```

### Trả về

```python
Dict
```

---

## generate_answer(question, context)

### Mô tả

Sinh câu trả lời bằng Gemini dựa trên context đã truy xuất.

### Tham số

```python
question: str
context: str
```

### Trả về

```python
str
```

---

# 13. Screenshots

Thêm ảnh màn hình tại đây:

- Giao diện chat
- Kết quả retrieval
- Hiển thị nguồn tham khảo
- Trả lời từ Gemini

---

# 14. Tác giả

**Nguyễn Hữu Đạt**

AI Engineer Intern
