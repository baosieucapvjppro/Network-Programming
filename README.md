# Ứng dụng Chat đa người dùng

Hệ thống chat room thời gian thực cho phép nhiều người dùng kết nối đồng thời, gửi tin nhắn công khai và tin nhắn riêng tư.

## Cài đặt nhanh

### Yêu cầu
- Python 3.7+

### Chạy ứng dụng

**1. Khởi động Server:**
```bash
python server.py
```

**2. Chạy Client GUI (Giao diện đồ họa):**
```bash
python client_gui.py
```

**Hoặc Client CLI (Dòng lệnh):**
```bash
python client.py 127.0.0.1 60000
```

## 📖 Hướng dẫn chi tiết

Xem file [HUONG_DAN_CHAY.md](HUONG_DAN_CHAY.md) để biết hướng dẫn đầy đủ.

##  Tính năng

-  Chat đa người dùng real-time
-  Tin nhắn công khai (broadcast)
-  Tin nhắn riêng tư (private message)
-  Quản lý người dùng với username
-  Giao diện GUI và CLI
-  Danh sách người dùng online

##  Lệnh

- `/nick <tên>` - Đặt tên người dùng
- `/list` - Xem danh sách người dùng online
- `/pm <tên> <nội dung>` - Gửi tin nhắn riêng tư
- `/quit` - Thoát khỏi chat
- `/help` - Hiển thị trợ giúp

##  Cấu trúc dự án

```
Network-Programming/
├── server.py          # Server xử lý kết nối và tin nhắn
├── client.py          # Client dòng lệnh
├── client_gui.py      # Client giao diện đồ họa
├── README.md          # File này
└── HUONG_DAN_CHAY.md  # Hướng dẫn chi tiết
```

## 🔧 Công nghệ

- Python 3.x
- Socket Programming (TCP/IP)
- Multi-threading
- Tkinter (GUI)

##  License

MIT License
