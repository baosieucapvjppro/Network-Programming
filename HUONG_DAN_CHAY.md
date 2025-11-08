# HƯỚNG DẪN CHẠY DỰ ÁN CHAT ĐA NGƯỜI DÙNG

##  Yêu cầu hệ thống

- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows, Linux, macOS
- **Thư viện**: Chỉ sử dụng thư viện chuẩn của Python (không cần cài đặt thêm)

---

##  CÁCH 1: Chạy với Client GUI (Giao diện đồ họa)

### Bước 1: Khởi động Server

Mở Terminal/Command Prompt và chạy:

```bash
python server.py
```

Hoặc chỉ định port cụ thể:

```bash
python server.py 60000
```

**Kết quả mong đợi:**
```
Server lắng nghe tại 0.0.0.0:60000
```

### Bước 2: Khởi động Client GUI

Mở Terminal/Command Prompt mới (giữ server chạy) và chạy:

```bash
python client_gui.py
```

**Lưu ý:** Client GUI hiện tại hardcoded kết nối đến `127.0.0.1:60000`. Nếu server chạy trên port khác, cần sửa file `client_gui.py` dòng 161.

**Quy trình sử dụng:**
1. Hộp thoại xuất hiện yêu cầu nhập tên
2. Nhập tên của bạn và nhấn OK
3. Giao diện chat sẽ hiển thị
4. Chọn người dùng từ danh sách bên trái (hoặc để "Tất cả" cho tin nhắn công khai)
5. Gõ tin nhắn và nhấn Enter hoặc click nút "Gửi"
6. Để gửi tin nhắn riêng: Chọn người dùng từ danh sách, sau đó gõ tin nhắn

---

##  CÁCH 2: Chạy với Client CLI (Dòng lệnh)

### Bước 1: Khởi động Server

Mở Terminal/Command Prompt và chạy:

```bash
python server.py
```

Hoặc:

```bash
python server.py 60000
```

### Bước 2: Khởi động Client CLI

Mở Terminal/Command Prompt mới (có thể mở nhiều cửa sổ để test nhiều client) và chạy:

```bash
python client.py 127.0.0.1 60000
```

**Quy trình sử dụng:**
1. Sau khi kết nối, server sẽ gửi thông báo chào mừng
2. Đặt tên bằng lệnh: `/nick <tên của bạn>`
   - Ví dụ: `/nick Alice`
3. Xem danh sách người dùng: `/list`
4. Gửi tin nhắn công khai: Gõ tin nhắn bình thường và nhấn Enter
5. Gửi tin nhắn riêng: `/pm <tên người nhận> <nội dung>`
   - Ví dụ: `/pm Bob Hello Bob!`
6. Thoát: `/quit` hoặc nhấn `Ctrl+C`

---

## 📝 CÁC LỆNH HỖ TRỢ

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `/nick <tên>` | Đặt hoặc đổi tên người dùng | `/nick Alice` |
| `/list` | Xem danh sách người dùng online | `/list` |
| `/pm <tên> <nội dung>` | Gửi tin nhắn riêng tư | `/pm Bob Hello` |
| `/quit` | Thoát khỏi chat | `/quit` |
| `/help` | Hiển thị trợ giúp | `/help` |

---

##  TEST VỚI NHIỀU CLIENT

### Test với Client GUI:

1. Khởi động server: `python server.py`
2. Mở nhiều cửa sổ Terminal/Command Prompt
3. Trong mỗi cửa sổ, chạy: `python client_gui.py`
4. Nhập tên khác nhau cho mỗi client
5. Test gửi tin nhắn công khai và riêng tư

### Test với Client CLI:

1. Khởi động server: `python server.py`
2. Mở nhiều cửa sổ Terminal/Command Prompt
3. Trong mỗi cửa sổ, chạy: `python client.py 127.0.0.1 60000`
4. Đặt tên khác nhau: `/nick Alice`, `/nick Bob`, `/nick Charlie`
5. Test các chức năng:
   - Gửi tin nhắn công khai
   - Gửi tin nhắn riêng tư
   - Xem danh sách người dùng
   - Đổi tên
   - Thoát và tham gia lại

---

##  CHẠY TRÊN MẠNG LAN

### Bước 1: Chạy Server

Trên máy server, chạy:

```bash
python server.py 60000
```

**Lưu ý:** Server mặc định lắng nghe trên `0.0.0.0`, nghĩa là chấp nhận kết nối từ mọi địa chỉ IP.

### Bước 2: Tìm địa chỉ IP của máy server

**Trên Windows:**
```bash
ipconfig
```
Tìm dòng "IPv4 Address" (ví dụ: 192.168.1.100)

**Trên Linux/macOS:**
```bash
ifconfig
```
hoặc
```bash
ip addr
```

### Bước 3: Chạy Client từ máy khác

**Với Client CLI:**
```bash
python client.py <IP_SERVER> 60000
```
Ví dụ: `python client.py 192.168.1.100 60000`

**Với Client GUI:**
Cần sửa file `client_gui.py` dòng 161:
```python
client.connect(('192.168.1.100', 60000))  # Thay 127.0.0.1 bằng IP server
```

---

##  XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "Address already in use"

**Nguyên nhân:** Port đã được sử dụng bởi ứng dụng khác

**Giải pháp:**
- Đóng ứng dụng đang dùng port đó
- Hoặc đổi port: `python server.py 8080`
- Trên Linux/macOS: Tìm và kill process: `lsof -i :60000`

### Lỗi 2: "Connection refused"

**Nguyên nhân:** Server chưa khởi động hoặc địa chỉ/port sai

**Giải pháp:**
- Kiểm tra server đã chạy chưa
- Kiểm tra địa chỉ IP và port có đúng không
- Kiểm tra firewall có chặn port không

### Lỗi 3: "Python was not found"

**Nguyên nhân:** Python chưa được cài đặt hoặc chưa có trong PATH

**Giải pháp:**
- Cài đặt Python từ https://www.python.org/downloads/
- Khi cài đặt, nhớ tích chọn "Add Python to PATH"
- Hoặc thử: `py server.py` (Windows) hoặc `python3 server.py` (Linux/macOS)

### Lỗi 4: "Tên đã được dùng"

**Nguyên nhân:** Tên người dùng đã tồn tại trong hệ thống

**Giải pháp:**
- Chọn tên khác: `/nick <tên_mới>`
- Tên không được chứa khoảng trắng

### Lỗi 5: "Không tìm thấy người dùng" (khi gửi PM)

**Nguyên nhân:** Tên người nhận không tồn tại hoặc đã rời khỏi chat

**Giải pháp:**
- Kiểm tra danh sách người dùng: `/list`
- Đảm bảo tên viết đúng chính tả

---

##  VÍ DỤ SỬ DỤNG

### Scenario: 3 người dùng chat với nhau

**Terminal 1 (Server):**
```bash
python server.py
```
```
Server lắng nghe tại 0.0.0.0:60000
Kết nối từ ('127.0.0.1', 54321)
Kết nối từ ('127.0.0.1', 54322)
Kết nối từ ('127.0.0.1', 54323)
```

**Terminal 2 (Client 1 - Alice):**
```bash
python client.py 127.0.0.1 60000
```
```
Đã kết nối tới 127.0.0.1:60000
Chào mừng đến với Chat!
Lệnh: /nick <ten>, /list, /pm <ten> <msg>, /quit, /help
Hãy đặt tên bằng lệnh: /nick <ten>
/nick Alice
Đã đặt tên: Alice
* Alice đã tham gia chat
Hello everyone!
[Alice] Hello everyone!
```

**Terminal 3 (Client 2 - Bob):**
```bash
python client.py 127.0.0.1 60000
```
```
Đã kết nối tới 127.0.0.1:60000
Chào mừng đến với Chat!
/nick Bob
Đã đặt tên: Bob
* Bob đã tham gia chat
[Alice] Hello everyone!
Hi Alice!
[Bob] Hi Alice!
/pm Alice This is private
[PM đến Alice] This is private
```

**Terminal 4 (Client 3 - Charlie với GUI):**
```bash
python client_gui.py
```
- Nhập tên: Charlie
- Chọn Bob từ danh sách
- Gõ: "Hi Bob!"
- Tin nhắn sẽ được gửi dưới dạng private message

---

##  TÙY CHỈNH

### Thay đổi port mặc định

**Server:**
Sửa dòng 144 trong `server.py`:
```python
port = int(sys.argv[1]) if len(sys.argv) >= 2 else 8080  # Đổi 60000 thành 8080
```

**Client GUI:**
Sửa dòng 161 trong `client_gui.py`:
```python
client.connect(('127.0.0.1', 8080))  # Đổi 60000 thành 8080
```

### Thay đổi địa chỉ server trong Client GUI

Sửa dòng 161 trong `client_gui.py`:
```python
client.connect(('192.168.1.100', 60000))  # Thay bằng IP server thực tế
```

Hoặc thêm input dialog:
```python
server_ip = simpledialog.askstring("Server IP", "Nhập địa chỉ server:", 
                                   initialvalue='127.0.0.1')
server_port = simpledialog.askinteger("Server Port", "Nhập cổng server:", 
                                      initialvalue=60000)
client.connect((server_ip, server_port))
```

---

##  KIỂM TRA KẾT NỐI

### Kiểm tra port có đang được sử dụng không

**Windows:**
```bash
netstat -an | findstr 60000
```

**Linux/macOS:**
```bash
netstat -an | grep 60000
```
hoặc
```bash
lsof -i :60000
```

### Test kết nối với telnet

```bash
telnet 127.0.0.1 60000
```

Nếu kết nối thành công, bạn có thể gõ lệnh trực tiếp:
```
/nick TestUser
Hello
```

---

##  TÀI LIỆU THAM KHẢO

- Python Socket Programming: https://docs.python.org/3/library/socket.html
- Python Threading: https://docs.python.org/3/library/threading.html
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html

---

**Chúc bạn sử dụng thành công! **
