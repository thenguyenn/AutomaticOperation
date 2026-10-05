import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import keyboard
import json
import time
import threading
import os
import pygetwindow as gw

class AutoOperationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automatic Operation")
        self.root.geometry("350x260")
        self.root.resizable(False, False)
        
        # Data
        self.steps = []  # Only store click positions
        self.config_file = "config.json"
        self.recording = False
        self.executing = False
        self.loop_count = 1
        self.auto_next_line = True
        
        # Setup
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        self.load_config()
        
        # GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="AUTOMATIC OPERATION", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Ghi vị trí Click button
        btn_record = ttk.Button(main_frame, text="Ghi vị trí Click", command=self.record_click, width=30)
        btn_record.pack(pady=5)
        
        # Loop number input
        loop_frame = ttk.Frame(main_frame)
        loop_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(loop_frame, text="Số lần lặp:").pack(side=tk.LEFT)
        self.loop_entry = ttk.Entry(loop_frame, width=10)
        self.loop_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.loop_entry.insert(0, "1")
        
        # Checkbox tự động xuống dòng
        self.auto_next_var = tk.BooleanVar(value=True)
        check = ttk.Checkbutton(
            main_frame, 
            text="Tự động xuống dòng WPS",
            variable=self.auto_next_var
        )
        check.pack(pady=5)
        
        # Execute button
        btn_execute = ttk.Button(main_frame, text="THỰC THI", command=self.execute_steps, width=30)
        btn_execute.pack(pady=15)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Clear button only
        btn_clear = ttk.Button(main_frame, text="Xóa tất cả", command=self.clear_all, width=30)
        btn_clear.pack(pady=3)
        
        # Status Bar
        self.status_label = ttk.Label(main_frame, text="Sẵn sàng | Số vị trí: 0", relief=tk.SUNKEN, anchor=tk.CENTER)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
    
    def load_config(self):
        """Load config from JSON"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.steps = config.get('steps', [])
                self.wps_window = config.get('wps_window_title', 'WPS')
                self.browser_window = config.get('browser_window_title', 'Chrome')
                self.loop_count = config.get('loop_count', 1)
                self.auto_next_line = config.get('auto_next_line', True)
        else:
            self.wps_window = 'WPS'
            self.browser_window = 'Chrome'
            self.loop_count = 1
            self.auto_next_line = True
    
    def save_config_file(self):
        """Save config to JSON"""
        config = {
            'steps': self.steps,
            'wps_window_title': self.wps_window,
            'browser_window_title': self.browser_window,
            'loop_count': self.loop_count,
            'auto_next_line': self.auto_next_line
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def update_steps_display(self):
        """Update status only"""
        self.status_label.config(text=f"Sẵn sàng | Số vị trí: {len(self.steps)}")
    
    def add_step(self, step_type, **kwargs):
        """Add step"""
        step = {'type': step_type, **kwargs}
        self.steps.append(step)
        self.update_steps_display()
    
    def record_click(self):
        """Record click position"""
        self.status_label.config(text="Ghi vị trí: Di chuyển chuột, nhấn F4 để lưu, ESC để hoàn thành")
        
        # Create a temporary overlay window to show coordinates
        overlay = tk.Toplevel(self.root)
        overlay.title("Vị trí hiện tại")
        overlay.attributes('-topmost', True)
        overlay.geometry("300x100+10+10")
        
        coord_label = ttk.Label(overlay, text="Di chuyển chuột...", font=('Arial', 12))
        coord_label.pack(pady=20)
        
        count_label = ttk.Label(overlay, text="Đã lưu: 0 vị trí", font=('Arial', 10), foreground='blue')
        count_label.pack(pady=5)
        
        def update_position():
            if self.recording:
                x, y = pyautogui.position()
                coord_label.config(text=f"Vị trí: ({x}, {y})")
                overlay.after(50, update_position)
        
        def record_thread():
            self.recording = True
            self.recorded_count = 0
            update_position()
            
            def on_key(event):
                if not self.recording:
                    return
                
                # F4 key to save position
                if event.name == 'f4':
                    try:
                        x, y = pyautogui.position()
                        self.add_step('click', x=x, y=y)
                        self.recorded_count += 1
                        count_label.config(text=f"✓ Đã lưu: {self.recorded_count} vị trí")
                        msg = f"✓ Đã lưu vị trí {self.recorded_count}: ({x}, {y}) | F4: Tiếp tục, ESC: Hoàn thành"
                        self.root.after(0, lambda: self.status_label.config(text=msg))
                    except Exception as e:
                        print(f"Error saving position: {e}")
                
                # ESC key to finish
                elif event.name == 'esc':
                    self.recording = False
                    keyboard.unhook_all()
                    overlay.destroy()
                    # Show confirmation popup
                    self.root.after(100, lambda: self.show_record_complete_popup(self.recorded_count))
            
            # Listen for keyboard events
            keyboard.on_press(on_key)
            
            # Keep thread alive until recording stops
            while self.recording:
                time.sleep(0.1)
            
            keyboard.unhook_all()
        
        thread = threading.Thread(target=record_thread, daemon=True)
        thread.start()
    
    def show_record_complete_popup(self, count):
        """Show completion popup"""
        msg = f"Đã hoàn thành ghi vị trí!\n\n"
        msg += f"Số vị trí click đã lưu: {count}\n"
        msg += f"Tổng số bước: {len(self.steps)}"
        
        messagebox.showinfo("Hoàn thành ghi vị trí", msg)
        self.status_label.config(text=f"Đã ghi {count} vị trí | Tổng: {len(self.steps)} bước")
    
    def add_copy_wps(self):
        """Add copy from WPS step"""
        self.add_step('switch_to_wps')
        self.add_step('wait', seconds=0.3)
        self.add_step('copy')
        self.add_step('wait', seconds=0.3)
        self.add_step('switch_to_browser')
        messagebox.showinfo("Thành công", "Đã thêm: Chuyển WPS → Copy → Quay lại")
    
    def add_paste(self):
        """Add paste step"""
        self.add_step('paste')
        messagebox.showinfo("Thành công", "Đã thêm bước: Paste")
    
    def add_wait(self):
        """Add wait step"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Delay")
        dialog.geometry("300x120")
        
        ttk.Label(dialog, text="Thời gian chờ (giây):").pack(pady=10)
        entry = ttk.Entry(dialog, width=20)
        entry.pack(pady=5)
        entry.insert(0, "0.5")
        entry.focus()
        
        def ok():
            try:
                seconds = float(entry.get())
                self.add_step('wait', seconds=seconds)
                messagebox.showinfo("Thành công", f"Đã thêm delay: {seconds}s")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=5)
    
    def add_type(self):
        """Add type text step"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Type Text")
        dialog.geometry("400x150")
        
        ttk.Label(dialog, text="Nhập text cần gõ:").pack(pady=10)
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.focus()
        
        def ok():
            text = entry.get()
            if text:
                self.add_step('type', text=text)
                messagebox.showinfo("Thành công", f"Đã thêm: Gõ '{text}'")
                dialog.destroy()
            else:
                messagebox.showwarning("Cảnh báo", "Text không được để trống")
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=5)
    
    def add_hotkey(self):
        """Add hotkey step"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Hotkey")
        dialog.geometry("350x150")
        
        ttk.Label(dialog, text="Phím tắt (vd: ctrl+s, alt+tab):").pack(pady=10)
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=5)
        entry.insert(0, "ctrl+")
        entry.focus()
        
        def ok():
            keys = entry.get()
            if keys:
                self.add_step('hotkey', keys=keys)
                messagebox.showinfo("Thành công", f"Đã thêm: Phím {keys}")
                dialog.destroy()
            else:
                messagebox.showwarning("Cảnh báo", "Phím tắt không được để trống")
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=5)
    
    def delete_step(self):
        """Delete a step"""
        if not self.steps:
            messagebox.showwarning("Cảnh báo", "Chưa có bước nào")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Xóa bước")
        dialog.geometry("300x120")
        
        ttk.Label(dialog, text=f"Xóa bước số (1-{len(self.steps)}):").pack(pady=10)
        entry = ttk.Entry(dialog, width=20)
        entry.pack(pady=5)
        entry.focus()
        
        def ok():
            try:
                index = int(entry.get())
                if 1 <= index <= len(self.steps):
                    removed = self.steps.pop(index - 1)
                    self.update_steps_display()
                    messagebox.showinfo("Thành công", f"Đã xóa bước {index}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", f"Số thứ tự phải từ 1-{len(self.steps)}")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=5)
    
    def clear_all(self):
        """Clear all steps"""
        if not self.steps:
            messagebox.showinfo("Thông báo", "Danh sách đã trống")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả các bước?"):
            self.steps = []
            self.update_steps_display()
            messagebox.showinfo("Thành công", "Đã xóa tất cả các bước")
    
    def config_loop(self):
        """Configure loop settings"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Cài đặt Loop")
        dialog.geometry("400x220")
        
        # Loop count
        ttk.Label(dialog, text="Số lần lặp lại:").pack(pady=(10,5))
        loop_entry = ttk.Entry(dialog, width=20)
        loop_entry.pack(pady=5)
        loop_entry.insert(0, str(self.loop_count))
        loop_entry.focus()
        
        # Auto next line checkbox
        ttk.Label(dialog, text="").pack(pady=5)
        auto_next_var = tk.BooleanVar(value=self.auto_next_line)
        check = ttk.Checkbutton(
            dialog, 
            text="Tự động xuống dòng trong WPS sau mỗi vòng lặp",
            variable=auto_next_var
        )
        check.pack(pady=5)
        
        # Info label
        info_label = ttk.Label(
            dialog, 
            text="(Sau khi hoàn thành 1 vòng, tự động nhấn Down trong WPS\nđể chuyển sang dòng dữ liệu tiếp theo)",
            foreground='gray',
            font=('Arial', 8)
        )
        info_label.pack(pady=5)
        
        def ok():
            try:
                count = int(loop_entry.get())
                if count < 1:
                    messagebox.showerror("Lỗi", "Số lần lặp phải >= 1")
                    return
                
                self.loop_count = count
                self.auto_next_line = auto_next_var.get()
                self.update_loop_display()
                messagebox.showinfo("Thành công", f"Đã cài đặt: Lặp {count} lần, Xuống dòng: {'BẬT' if self.auto_next_line else 'TẮT'}")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=10)
    
    def update_loop_display(self):
        """Update loop info display"""
        next_line_text = "BẬT" if self.auto_next_line else "TẮT"
        self.loop_label.config(text=f"Loop: {self.loop_count} lần | Tự xuống dòng WPS: {next_line_text}")
    
    def save_config_gui(self):
        """Save config"""
        # Update config from entry
        try:
            self.loop_count = int(self.loop_entry.get())
        except:
            self.loop_count = 1
        self.auto_next_line = self.auto_next_var.get()
        
        self.save_config_file()
        messagebox.showinfo("Thành công", f"Đã lưu {len(self.steps)} vị trí click vào {self.config_file}")
    
    def load_config_gui(self):
        """Load config"""
        self.load_config()
        self.loop_entry.delete(0, tk.END)
        self.loop_entry.insert(0, str(self.loop_count))
        self.auto_next_var.set(self.auto_next_line)
        self.update_steps_display()
        messagebox.showinfo("Thành công", f"Đã tải {len(self.steps)} vị trí click từ {self.config_file}")
    
    def execute_steps(self):
        """Execute all steps"""
        if not self.steps:
            messagebox.showwarning("Cảnh báo", "Chưa có vị trí click nào để thực thi")
            return
        
        # Get loop count from entry
        try:
            loop_count = int(self.loop_entry.get())
            if loop_count < 1:
                messagebox.showerror("Lỗi", "Số lần lặp phải >= 1")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho số lần lặp")
            return
        
        # Get auto next line setting
        auto_next_line = self.auto_next_var.get()
        
        # Confirm execution
        next_line_text = "CÓ" if auto_next_line else "KHÔNG"
        msg = f"⚠️ CHUẨN BỊ:\n\n"
        msg += f"Đảm bảo đã mở:\n"
        msg += f"  ✓ WPS (con trỏ ở đầu dòng đầu tiên)\n"
        msg += f"  ✓ Browser (form cần điền)\n\n"
        msg += f"⚠️ QUAN TRỌNG:\n"
        msg += f"  • Chỉ mở 2 cửa sổ: WPS và Browser\n"
        msg += f"  • Đóng tất cả cửa sổ khác để Alt+Tab hoạt động đúng\n\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += f"• Số vị trí click: {len(self.steps)}\n"
        msg += f"• Số lần lặp: {loop_count}\n"
        msg += f"• Tự động xuống dòng WPS: {next_line_text}\n\n"
        msg += f"🔍 TỰ ĐỘNG NHẬN DIỆN:\n"
        msg += f"  • Đang ở WPS → Copy → Tab Browser → Steps\n"
        msg += f"  • Đang ở Browser → Tab WPS → Copy → Tab Browser → Steps\n\n"
        msg += f"Workflow mỗi vòng:\n"
        msg += f"  1. Nhận diện cửa sổ hiện tại\n"
        msg += f"  2. Tự động điều hướng đến WPS\n"
        msg += f"  3. Copy dòng từ WPS\n"
        msg += f"  4. Tab Browser → Paste vào {len(self.steps)} vị trí\n"
        msg += f"  5. Tab WPS → Xuống dòng\n\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "Bạn có thể ở BẤT KỲ cửa sổ nào,\n"
        msg += "chương trình sẽ TỰ ĐỘNG điều hướng!\n\n"
        msg += "Nhấn OK để bắt đầu sau 3 giây.\n"
        msg += "Nhấn SPACE để dừng.\n\n"
        msg += "Sẵn sàng chưa?"
        
        if messagebox.askyesno("Xác nhận thực thi", msg):
            self.run_execution(loop_count, auto_next_line)
    
    def get_active_window_type(self):
        """Detect if current active window is WPS or Browser"""
        try:
            active = gw.getActiveWindow()
            if active:
                title = active.title.lower()
                # Check for WPS keywords
                if 'wps' in title or 'spreadsheet' in title or 'et' in title:
                    return 'WPS'
                # Check for Browser keywords
                elif 'chrome' in title or 'firefox' in title or 'edge' in title or 'browser' in title:
                    return 'Browser'
            return 'Unknown'
        except:
            return 'Unknown'
    
    def run_execution(self, loop_count, auto_next_line):
        """Run execution in thread"""
        self.executing = True
        self.status_label.config(text=f"Chuẩn bị thực thi... (3 giây)")
        
        def execute_thread():
            try:
                # Setup Space key listener to stop execution
                def on_space(event):
                    if event.name == 'space' and self.executing:
                        self.executing = False
                        self.root.after(0, lambda: messagebox.showinfo("Dừng", "Đã dừng loop bởi người dùng (Space)"))
                
                keyboard.on_press(on_space)
                
                # Countdown
                for i in range(3, 0, -1):
                    if not self.executing:
                        keyboard.unhook_all()
                        return
                    self.status_label.config(text=f"Bắt đầu sau {i} giây... Đang nhận diện cửa sổ...")
                    time.sleep(1)
                
                # Execute loops
                for loop in range(loop_count):
                    if not self.executing:
                        break
                    
                    # BƯỚC 1: DETECT cửa sổ hiện tại mỗi vòng lặp
                    current_window = self.get_active_window_type()
                    self.status_label.config(text=f"🔄 Vòng {loop+1}/{loop_count} - Phát hiện: {current_window}")
                    time.sleep(0.3)
                    
                    # BƯỚC 2: Điều hướng đến WPS nếu cần
                    if current_window == 'Browser':
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Đang ở Browser → Tab sang WPS...")
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.8)
                    elif current_window == 'WPS':
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Đã ở WPS → Copy ngay!")
                        time.sleep(0.3)
                    else:
                        # Unknown - giả định cần tab sang WPS
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Không xác định → Tab sang WPS...")
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.8)
                    
                    # BƯỚC 3: Copy TOÀN BỘ từ WPS (giờ chắc chắn đang ở WPS)
                    self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Đang copy từ WPS...")
                    
                    # Chọn toàn bộ dòng hiện tại (Shift+End để chọn đến cuối dòng)
                    pyautogui.hotkey('shift', 'end')
                    time.sleep(0.3)
                    
                    # Copy
                    pyautogui.hotkey('ctrl', 'c')
                    time.sleep(0.4)
                    
                    # Bỏ chọn (nhấn phím mũi tên phải)
                    pyautogui.press('right')
                    time.sleep(0.2)
                    
                    # BƯỚC 4: Tab sang Browser
                    self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Tab sang Browser...")
                    time.sleep(0.3)
                    
                    # Tab và verify
                    for attempt in range(2):  # Thử tối đa 2 lần
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(1.0)
                        
                        verify_window = self.get_active_window_type()
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Phát hiện: {verify_window}")
                        
                        if verify_window == 'Browser':
                            self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - ✓ Đã ở Browser, bắt đầu paste...")
                            time.sleep(0.3)
                            break
                        elif verify_window == 'WPS' and attempt < 1:
                            # Vẫn ở WPS, thử tab lần nữa
                            self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Vẫn ở WPS, tab lại...")
                            time.sleep(0.3)
                        else:
                            # Unknown hoặc hết lần thử
                            self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Giả định đã tab xong, tiếp tục...")
                            time.sleep(0.3)
                            break
                    
                    # BƯỚC 5: Thực hiện TẤT CẢ các step với dữ liệu đã copy
                    for i, step in enumerate(self.steps, 1):
                        if not self.executing:
                            break
                        
                        # Click vào vị trí
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Step {i}/{len(self.steps)}: Click ({step['x']}, {step['y']})")
                        pyautogui.click(step['x'], step['y'])
                        time.sleep(0.3)
                        
                        # Xóa text cũ
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(0.1)
                        pyautogui.press('delete')
                        time.sleep(0.2)
                        
                        # Paste (cùng 1 dữ liệu đã copy từ WPS)
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Step {i}/{len(self.steps)}: Paste")
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.3)
                    
                    # BƯỚC 6: Sau khi hoàn thành tất cả steps, tab về WPS và xuống dòng
                    if loop < loop_count - 1 or auto_next_line:
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} hoàn thành - Tab về WPS...")
                        time.sleep(0.3)
                        
                        # Tab về WPS
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(1.0)  # Tăng thời gian chờ
                        
                        # Nhấn Home để về đầu dòng
                        pyautogui.press('home')
                        time.sleep(0.2)
                        
                        # Nhấn Down để xuống dòng tiếp theo
                        if auto_next_line:
                            pyautogui.press('down')
                            time.sleep(0.3)
                
                self.executing = False
                keyboard.unhook_all()
                self.status_label.config(text=f"✅ Hoàn thành {loop_count} vòng lặp!")
                messagebox.showinfo("Thành công", f"Đã hoàn thành {loop_count} vòng lặp!")
                
            except Exception as e:
                self.executing = False
                keyboard.unhook_all()
                self.status_label.config(text=f"❌ Lỗi: {str(e)}")
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        
        thread = threading.Thread(target=execute_thread, daemon=True)
        thread.start()
    
    def run(self):
        """Run GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoOperationGUI()
    app.run()
