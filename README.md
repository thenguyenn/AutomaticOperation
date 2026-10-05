# 🤖 Automatic Operation

Công cụ tự động hóa thao tác click, copy, paste giữa các ứng dụng (WPS, trình duyệt...).

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

## ✨ Tính năng

- ✅ **Tự động nhận diện cửa sổ** (WPS hay Browser)
- ✅ Ghi vị trí click đơn giản (F4 để lưu)
- ✅ Tự động xóa text cũ trước khi paste
- ✅ Tự động Copy/Paste từ WPS
- ✅ Lặp lại workflow nhiều lần
- ✅ Dừng loop bằng phím Space
- ✅ Tự động xuống dòng trong WPS
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
- Cửa sổ nhỏ hiện tọa độ real-time
- Di chuyển chuột đến vị trí, nhấn **F4** để lưu
- Nhấn **ESC** khi hoàn tất

### 2. Chuẩn bị dữ liệu
- **WPS**: Mở file, đặt con trỏ ở **đầu dòng đầu tiên**
- **Browser**: Mở trang/form cần điền
- Đảm bảo cả 2 đang mở
- **Bạn có thể ở bất kỳ cửa sổ nào** - chương trình sẽ tự nhận diện!

### 3. Cài đặt
- Nhập số lần lặp (ví dụ: 10, 100...)
- Tick "Tự động xuống dòng WPS" nếu muốn

### 4. Thực thi
- Click **"THỰC THI"**
- Đọc thông báo xác nhận
- Nhấn **OK**
- **Chương trình tự động nhận diện** cửa sổ hiện tại:
  - Nếu đang ở **WPS**: Copy → Tab Browser → Steps
  - Nếu đang ở **Browser**: Tab WPS → Copy → Tab Browser → Steps
  - Nếu không xác định: Tự động tab đến WPS

### 5. Dừng (nếu cần)
- Nhấn **SPACE** để dừng bất cứ lúc nào

## 🎬 Workflow

**Tự động nhận diện cửa sổ:**
- 🔍 Phát hiện đang ở WPS hay Browser
- 🎯 Tự động điều hướng đến đúng cửa sổ
- ⚡ Không cần lo đang ở đâu!

**Mỗi vòng lặp:**
```
0. Nhận diện cửa sổ hiện tại (WPS/Browser/Unknown)
1. Điều hướng đến WPS (nếu cần)
2. Copy TOÀN BỘ dòng hiện tại từ WPS (Shift+End → Ctrl+C)
3. Tab sang Browser
4. Với mỗi vị trí click (lần lượt):
   → Click vào vị trí
   → Xóa text cũ
   → Paste (cùng 1 dữ liệu đã copy)
5. Tab về WPS → Home → Down (xuống dòng tiếp)
6. Lặp lại vòng tiếp theo
```

**Ví dụ cụ thể:**
```
WPS dòng 1: "Nguyễn Văn A - 0123456789 - Hà Nội"
          ^cursor

Vòng 1:
  Copy "Nguyễn Văn A - 0123456789 - Hà Nội"
  → Tab Browser
  → Click vị trí 1 → Paste "Nguyễn Văn A - 0123456789 - Hà Nội"
  → Click vị trí 2 → Paste "Nguyễn Văn A - 0123456789 - Hà Nội"
  → Click vị trí 3 → Paste "Nguyễn Văn A - 0123456789 - Hà Nội"
  → Tab WPS → Xuống dòng 2

Vòng 2:
  Copy "Trần Thị B - 0987654321 - TP.HCM"
  → Tab Browser
  → Click vị trí 1 → Paste "Trần Thị B - 0987654321 - TP.HCM"
  → Click vị trí 2 → Paste "Trần Thị B - 0987654321 - TP.HCM"
  → Click vị trí 3 → Paste "Trần Thị B - 0987654321 - TP.HCM"
  → Xong!
```

## 💡 Ví dụ thực tế

**Kịch bản**: Điền cùng 1 thông tin vào 3 ô khác nhau

**Dữ liệu WPS:**
```
Nguyễn Văn A - 0123456789 - Hà Nội
Trần Thị B - 0987654321 - TP.HCM
Lê Văn C - 0111222333 - Đà Nẵng
```

**Bước 1**: Ghi 3 vị trí
- Vị trí 1: Ô "Thông tin 1"
- Vị trí 2: Ô "Thông tin 2"
- Vị trí 3: Ô "Thông tin 3"

**Bước 2**: Chuẩn bị
- WPS: Con trỏ ở **đầu dòng 1**
- Browser: Mở form cần điền
- **Bạn có thể click vào bất kỳ cửa sổ nào!**
- Chương trình sẽ **TỰ ĐỘNG NHẬN DIỆN** và điều hướng

**Bước 3**: Cài đặt
- Số lần lặp: 3
- Tự xuống dòng WPS: ✓

**Bước 4**: Thực thi

Nhấn "THỰC THI" → OK → Chương trình **TỰ ĐỘNG**:
- 🔍 Nhận diện cửa sổ hiện tại (WPS/Browser)
- 🎯 Điều hướng đến WPS (nếu đang ở Browser)
- 📋 Copy dòng từ WPS
- 🌐 Tab sang Browser → Paste vào 3 vị trí
- ↩️ Tab về WPS → Xuống dòng
- 🔄 Lặp lại...

**Kết quả:**
```
Vòng 1:
  Copy "Nguyễn Văn A - 0123456789 - Hà Nội"
  → Paste vào cả 3 ô
  → Xuống dòng 2

Vòng 2:
  Copy "Trần Thị B - 0987654321 - TP.HCM"
  → Paste vào cả 3 ô
  → Xuống dòng 3

Vòng 3:
  Copy "Lê Văn C - 0111222333 - Đà Nẵng"
  → Paste vào cả 3 ô
  → Xong!
```

→ **3 dòng × 3 ô = 9 lần paste tự động!** ⚡

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
| **ESC** | Kết thúc ghi vị trí |
| **SPACE** | Dừng loop đang chạy |

## 📝 Cấu hình

Cấu hình được lưu tự động khi đóng chương trình:
- Tất cả vị trí click
- Số lần lặp
- Cài đặt tự động xuống dòng

## ⚠️ Lưu ý

### Chuẩn bị trước khi chạy:
1. **WPS**: Đặt con trỏ ở **đầu dòng đầu tiên** (nhấn Home để chắc chắn)
2. **Browser**: Mở trang/form cần điền
3. **⚠️ QUAN TRỌNG**: Chỉ mở 2 cửa sổ (WPS + Browser), đóng các cửa sổ khác
4. **Bạn có thể click vào bất kỳ cửa sổ nào** - WPS hay Browser đều được!
5. Nhấn "Thực thi" - Chương trình sẽ **TỰ ĐỘNG NHẬN DIỆN** và điều hướng

### Lưu ý quan trọng:
- **✨ TỰ ĐỘNG NHẬN DIỆN**: Chương trình tự phát hiện bạn đang ở WPS hay Browser
- **🎯 KHÔNG CẦN LO**: Bạn có thể click vào bất kỳ cửa sổ nào trước khi nhấn "Thực thi"
- **⚠️ CHỈ MỞ 2 CỬA SỔ**: WPS và Browser. Đóng các cửa sổ/tab khác để Alt+Tab hoạt động chính xác
- Chương trình sẽ tự động điều hướng đến đúng cửa sổ
- Chỉ cần đảm bảo cả 2 ứng dụng đang mở
- Copy **TOÀN BỘ DÒNG** từ WPS (Shift+End)
- Paste **CÙNG 1 dữ liệu** vào tất cả vị trí

### Trong khi chạy:
- Đợi 3 giây sau khi nhấn "Thực thi" để chuẩn bị
- Có thể dừng loop bằng phím **SPACE** bất cứ lúc nào
- Text cũ trong ô input sẽ tự động xóa trước khi paste
- Độ phân giải màn hình không nên thay đổi sau khi ghi vị trí

### Tips:
- Nếu copy không được text: Tăng delay giữa các bước (hiện tại 0.6s)
- Nếu tab sai cửa sổ: Đảm bảo chỉ có WPS và Browser đang mở
- Mỗi lần copy sẽ tự động tab sang cột tiếp theo trong WPS

## 🐛 Troubleshooting

**Không chuyển được cửa sổ?**
→ Đảm bảo CHỈ mở 2 cửa sổ: WPS và Browser
→ Đóng tất cả cửa sổ/tab khác
→ Alt+Tab chỉ hoạt động tốt khi có đúng 2 cửa sổ

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
