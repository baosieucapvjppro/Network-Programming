import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, ttk
import socket
import threading
import re

ENC = 'utf-8'
buffer = b""
selected_user = None
my_username = ""

def update_user_list():
    """Gửi lệnh /list để cập nhật danh sách người dùng"""
    try:
        client.sendall("/list\n".encode(ENC))
    except:
        pass

def parse_user_list(message):
    """Phân tích danh sách người dùng từ tin nhắn server"""
    if message.startswith("Online: "):
        users_str = message[8:].strip()
        if users_str and users_str != "(trống)":
            users = [u.strip() for u in users_str.split(",")]
            return users
    return None

def receive_messages():
    global buffer
    while True:
        try:
            data = client.recv(4096)
            if not data:
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "\n[Mất kết nối tới server]\n", "system")
                chat_box.config(state=tk.DISABLED)
                chat_box.see(tk.END)
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                message = line.decode(ENC, errors='ignore')
                
                # Phân tích danh sách người dùng
                users = parse_user_list(message)
                if users is not None:
                    update_user_listbox(users)
                
                # Tự động cập nhật danh sách khi có người vào/ra
                if message.startswith("*") and ("đổi tên thành" in message or "đã thoát" in message or "đã tham gia" in message):
                    # Đợi một chút rồi cập nhật danh sách
                    root.after(100, update_user_list)
                
                # Hiển thị tin nhắn với màu sắc
                chat_box.config(state=tk.NORMAL)
                if message.startswith("[PM từ") or message.startswith("[PM đến"):
                    chat_box.insert(tk.END, message + '\n', "pm")
                elif message.startswith("*"):
                    chat_box.insert(tk.END, message + '\n', "system")
                elif message.startswith("["):
                    chat_box.insert(tk.END, message + '\n', "message")
                else:
                    chat_box.insert(tk.END, message + '\n')
                chat_box.config(state=tk.DISABLED)
                chat_box.see(tk.END)
        except Exception as e:
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"\n[Lỗi: {e}]\n", "system")
            chat_box.config(state=tk.DISABLED)
            break

def update_user_listbox(users):
    """Cập nhật danh sách người dùng trong listbox"""
    if not users:
        return
    
    # Sử dụng after để đảm bảo cập nhật UI an toàn từ thread
    def _update():
        user_listbox.delete(0, tk.END)
        user_listbox.insert(0, "📢 Tất cả")
        
        # Sắp xếp danh sách: tên của mình lên đầu, sau đó các tên khác theo alphabet
        sorted_users = sorted(users, key=lambda x: (x != my_username, x))
        
        for user in sorted_users:
            user = user.strip()  # Loại bỏ khoảng trắng thừa
            if not user:
                continue
            if user == my_username:
                # Hiển thị tên của mình với icon khác
                user_listbox.insert(tk.END, f"😊 {user} (Bạn)")
            else:
                user_listbox.insert(tk.END, f"👤 {user}")
    
    try:
        root.after(0, _update)
    except:
        _update()

def on_user_select(event):
    """Xử lý khi chọn người dùng từ danh sách"""
    global selected_user
    selection = user_listbox.curselection()
    if selection:
        selected_text = user_listbox.get(selection[0])
        if selected_text == "📢 Tất cả":
            selected_user = None
            recipient_label.config(text="Gửi đến: Tất cả", fg="#2196F3")
        elif "(Bạn)" in selected_text:
            # Không cho phép nhắn tin cho chính mình
            messagebox.showinfo("Thông báo", "Bạn không thể nhắn tin cho chính mình!")
            selected_user = None
            recipient_label.config(text="Gửi đến: Tất cả", fg="#2196F3")
        else:
            # Loại bỏ icon và lấy tên
            selected_user = selected_text.replace("👤 ", "").strip()
            recipient_label.config(text=f"Gửi đến: {selected_user} (Riêng tư)", fg="#FF5722")

def send_message(event=None):
    message = entry.get().strip()
    if not message:
        return
    try:
        # Kiểm tra nếu người dùng gõ lệnh /pm thủ công
        if message.startswith("/pm "):
            # Phân tích lệnh /pm để kiểm tra người nhận
            parts = message.split(maxsplit=2)
            if len(parts) >= 2:
                target = parts[1].strip()
                if target == my_username:
                    messagebox.showwarning("Cảnh báo", "Bạn không thể gửi tin nhắn riêng cho chính mình!")
                    return
            # Gửi lệnh /pm
            client.sendall((message + "\n").encode(ENC))
        elif selected_user:
            # Gửi tin nhắn riêng qua UI (đã chọn người dùng)
            client.sendall(f"/pm {selected_user} {message}\n".encode(ENC))
        else:
            # Gửi tin nhắn công khai
            client.sendall((message + "\n").encode(ENC))
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể gửi tin nhắn: {e}")

def refresh_users():
    """Làm mới danh sách người dùng"""
    update_user_list()

def on_closing():
    """Xử lý khi đóng cửa sổ"""
    try:
        client.sendall("/quit\n".encode(ENC))
        client.close()
    except:
        pass
    root.destroy()

# Kết nối tới server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 60000))
except Exception as e:
    print(f"Không thể kết nối tới server: {e}")
    exit(1)

root = tk.Tk()
root.title("💬 Chat App")
root.geometry("900x600")
root.configure(bg="#f5f5f5")

# Yêu cầu người dùng nhập tên
my_username = simpledialog.askstring("Tên người dùng", "Nhập tên của bạn:", parent=root)
if not my_username:
    messagebox.showerror("Lỗi", "Bạn phải nhập tên!")
    client.close()
    root.destroy()
    exit(1)

# Gửi lệnh /nick để đặt tên
try:
    client.sendall(f"/nick {my_username}\n".encode(ENC))
except Exception as e:
    messagebox.showerror("Lỗi", f"Không thể đặt tên: {e}")
    client.close()
    root.destroy()
    exit(1)

# Frame chính
main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame bên trái - Danh sách người dùng
left_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, borderwidth=1)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

users_title = tk.Label(left_frame, text="👥 Người dùng Online", font=("Arial", 12, "bold"), 
                       bg="white", fg="#333", pady=10)
users_title.pack(fill=tk.X)

user_listbox = tk.Listbox(left_frame, width=25, font=("Arial", 10), 
                          bg="white", fg="#333", selectbackground="#2196F3",
                          selectforeground="white", relief=tk.FLAT, borderwidth=0)
user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
user_listbox.bind('<<ListboxSelect>>', on_user_select)
user_listbox.insert(0, "📢 Tất cả")

refresh_btn = tk.Button(left_frame, text="🔄 Làm mới", command=refresh_users,
                       bg="#4CAF50", fg="white", font=("Arial", 9, "bold"),
                       relief=tk.FLAT, cursor="hand2", pady=5)
refresh_btn.pack(fill=tk.X, padx=5, pady=5)

# Frame bên phải - Chat
right_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, borderwidth=1)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Header
header_frame = tk.Frame(right_frame, bg="#2196F3", height=50)
header_frame.pack(fill=tk.X)
header_frame.pack_propagate(False)

chat_title = tk.Label(header_frame, text=f"💬 Chat - {my_username}", 
                     font=("Arial", 14, "bold"), bg="#2196F3", fg="white")
chat_title.pack(side=tk.LEFT, padx=15, pady=10)

# Recipient label
recipient_label = tk.Label(header_frame, text="Gửi đến: Tất cả", 
                          font=("Arial", 10), bg="#2196F3", fg="white")
recipient_label.pack(side=tk.RIGHT, padx=15)

# Chat box với màu sắc
chat_box = scrolledtext.ScrolledText(right_frame, state=tk.DISABLED, 
                                     width=60, height=20, wrap=tk.WORD,
                                     font=("Arial", 10), bg="#fafafa", 
                                     relief=tk.FLAT, borderwidth=0)
chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Cấu hình màu sắc cho các loại tin nhắn
chat_box.tag_config("message", foreground="#333")
chat_box.tag_config("pm", foreground="#FF5722", font=("Arial", 10, "bold"))
chat_box.tag_config("system", foreground="#9E9E9E", font=("Arial", 9, "italic"))

# Input frame
input_frame = tk.Frame(right_frame, bg="white")
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

entry = tk.Entry(input_frame, font=("Arial", 11), relief=tk.FLAT, 
                bg="#f5f5f5", fg="#333", insertbackground="#2196F3")
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 5))
entry.bind("<Return>", send_message)
entry.focus()

send_button = tk.Button(input_frame, text="📤 Gửi", command=send_message,
                       bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                       relief=tk.FLAT, cursor="hand2", width=10, pady=8)
send_button.pack(side=tk.LEFT)

# Bắt đầu thread nhận tin nhắn
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

# Tự động cập nhật danh sách người dùng sau 1 giây
root.after(1000, update_user_list)

# Xử lý đóng cửa sổ
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
