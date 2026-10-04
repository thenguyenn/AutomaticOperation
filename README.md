# 🤖 Automatic Operation

Công cụ tự động hóa thao tác click, copy, paste giữa các ứng dụng (WPS, trình duyệt...).

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

## ✨ Tính năng

- ✅ Ghi vị trí click đơn giản (F4 để lưu)
- ✅ Tự động Copy/Paste từ WPS sau mỗi click
- ✅ Lặp lại workflow nhiều lần
- ✅ Tự động xuống dòng trong WPS
- ✅ Lưu/tải cấu hình
- ✅ Giao diện đơn giản, dễ sử dụng

## 📥 Cài đặt

### Cách 1: Tải file EXE (Khuyến nghị) ⭐

1. Vào [Releases](../../releases) 
2. Tải `AutomaticOperation.exe`
3. Chạy ngay, không cần cài đặt!

> **Lưu ý**: File EXE sẽ có sẵn sau khi push code lên GitHub (tự động build bởi GitHub Actions)

### Cách 2: Chạy từ source code

```cmd
git clone https://github.com/your-username/AutomaticOperation.git
cd AutomaticOperation
python -m pip install -r requirements.txt
python AutomaticOperation_GUI.py
```

## 🚀 Cách sử dụng

### 1. Ghi vị trí click
- Click nút **"Ghi vị trí Click"**
- Di chuyển chuột đến các vị trí cần click
- Nhấn **F4** để lưu mỗi vị trí
- Nhấn **ESC** khi hoàn tất

### 2. Cài đặt loop
- Nhập số lần lặp (ví dụ: 10, 100...)
- Tick "Tự động xuống dòng WPS" nếu muốn tự động chuyển sang dòng tiếp theo

### 3. Thực thi
- Click **"THỰC THI"**
- Xác nhận thông tin
- Chương trình sẽ tự động chạy!

## 🎬 Workflow

**Với mỗi vị trí click đã lưu:**
```
1. Click vào vị trí
2. Chuyển sang WPS
3. Copy (Ctrl+C)
4. Quay lại trình duyệt
5. Paste (Ctrl+V)
```

**Sau khi hoàn thành 1 vòng lặp:**
```
→ Tự động xuống dòng trong WPS (nếu bật)
→ Tiếp tục vòng lặp tiếp theo
```

## 💡 Ví dụ thực tế

**Kịch bản**: Điền form từ 100 dòng dữ liệu trong WPS

**Bước 1**: Ghi 3 vị trí
- Vị trí 1: Ô "Tên"
- Vị trí 2: Ô "Số điện thoại"
- Vị trí 3: Nút "Submit"

**Bước 2**: Cài đặt
- Số lần lặp: 100
- Tự xuống dòng WPS: ✓

**Bước 3**: Thực thi
→ **Kết quả**: 100 dòng dữ liệu được điền tự động trong vài phút! ⚡

## 🏗️ Build file EXE

### Yêu cầu
- Python 3.7+ ([Tải tại đây](https://www.python.org/downloads/))

### Cách 1: Dùng file .bat
```cmd
build_exe.bat
```

### Cách 2: Thủ công
```cmd
python -m pip install pyinstaller
python -m pip install -r requirements.txt
pyinstaller --onefile --noconsole --name AutomaticOperation AutomaticOperation_GUI.py
```

File EXE tại: `dist\AutomaticOperation.exe`

### Cách 3: GitHub Actions (Tự động)
Push code lên GitHub → File EXE tự động build trong Actions

## ⌨️ Phím tắt

| Phím | Chức năng |
|------|-----------|
| **F4** | Lưu vị trí click hiện tại |
| **ESC** | Kết thúc ghi vị trí / Dừng thực thi |

## 📝 Cấu hình

File `config.json` lưu:
- Tất cả vị trí click
- Số lần lặp
- Cài đặt tự động xuống dòng

## ⚠️ Lưu ý

- Đảm bảo WPS và trình duyệt đang mở
- Đợi 3 giây sau khi nhấn "Thực thi" để chuẩn bị
- Có thể dừng bất cứ lúc nào bằng ESC
- Độ phân giải màn hình không nên thay đổi sau khi ghi vị trí

## 🐛 Troubleshooting

**Không chuyển được cửa sổ?**
→ Đảm bảo cả WPS và trình duyệt đang mở

**Click sai vị trí?**
→ Kiểm tra độ phân giải màn hình không đổi

**Copy/Paste không hoạt động?**
→ Các ứng dụng có thể cần thêm thời gian phản hồi

## 📄 License

MIT License - Xem [LICENSE](LICENSE)

## 🤝 Đóng góp

Contributions, issues và feature requests đều được chào đón!
Xem [CONTRIBUTING.md](CONTRIBUTING.md)

## 🌟 Support

Nếu project hữu ích, hãy cho 1 ⭐ nhé!

---

**Made with ❤️ for automation enthusiasts**
