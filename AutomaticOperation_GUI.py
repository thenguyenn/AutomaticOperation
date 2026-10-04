import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import keyboard
import json
import time
import threading
import os

class AutoOperationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automatic Operation")
        self.root.geometry("350x300")
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
        
        # Save/Load/Clear buttons
        btn_save = ttk.Button(main_frame, text="Lưu cấu hình", command=self.save_config_gui, width=30)
        btn_save.pack(pady=3)
        
        btn_load = ttk.Button(main_frame, text="Tải cấu hình", command=self.load_config_gui, width=30)
        btn_load.pack(pady=3)
        
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
        
        def record_thread():
            self.recording = True
            self.recorded_count = 0
            
            def on_key(event):
                if not self.recording:
                    return
                
                # F4 key to save position
                if event.name == 'f4':
                    try:
                        x, y = pyautogui.position()
                        self.add_step('click', x=x, y=y)
                        self.recorded_count += 1
                        msg = f"✓ Đã lưu vị trí {self.recorded_count}: ({x}, {y}) | F4: Tiếp tục, ESC: Hoàn thành"
                        self.root.after(0, lambda: self.status_label.config(text=msg))
                    except Exception as e:
                        print(f"Error saving position: {e}")
                
                # ESC key to finish
                elif event.name == 'esc':
                    self.recording = False
                    keyboard.unhook_all()
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
        msg = f"Sẽ thực thi:\n\n"
        msg += f"• Số vị trí click: {len(self.steps)}\n"
        msg += f"• Số lần lặp: {loop_count}\n"
        msg += f"• Tự động Copy/Paste từ WPS: CÓ\n"
        msg += f"• Tự động xuống dòng WPS: {next_line_text}\n\n"
        msg += "Bắt đầu sau 3 giây. Nhấn ESC để dừng.\n\n"
        msg += "Bạn có muốn tiếp tục?"
        
        if messagebox.askyesno("Xác nhận thực thi", msg):
            self.run_execution(loop_count, auto_next_line)
    
    def run_execution(self, loop_count, auto_next_line):
        """Run execution in thread"""
        self.executing = True
        self.status_label.config(text=f"Chuẩn bị thực thi... (3 giây)")
        
        def execute_thread():
            try:
                # Countdown
                for i in range(3, 0, -1):
                    if not self.executing:
                        return
                    self.status_label.config(text=f"Bắt đầu sau {i} giây... (Nhấn ESC để hủy)")
                    time.sleep(1)
                
                # Execute loops
                for loop in range(loop_count):
                    if not self.executing:
                        break
                    
                    self.status_label.config(text=f"🔄 Vòng {loop+1}/{loop_count}")
                    
                    # Execute all click steps
                    for i, step in enumerate(self.steps, 1):
                        if not self.executing:
                            break
                        
                        # Click
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Click {i}/{len(self.steps)}")
                        pyautogui.click(step['x'], step['y'])
                        time.sleep(0.3)
                        
                        # Auto Copy/Paste from WPS after each click
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} - Copy/Paste {i}/{len(self.steps)}")
                        
                        # Switch to WPS
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.5)
                        
                        # Copy
                        pyautogui.hotkey('ctrl', 'c')
                        time.sleep(0.3)
                        
                        # Switch back to browser
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.5)
                        
                        # Paste
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.3)
                    
                    # Auto next line in WPS after each loop (except last one)
                    if auto_next_line and loop < loop_count - 1:
                        self.status_label.config(text=f"Vòng {loop+1}/{loop_count} hoàn thành - Xuống dòng WPS...")
                        
                        # Switch to WPS
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.5)
                        
                        # Press Down arrow to go to next line
                        pyautogui.press('down')
                        time.sleep(0.3)
                        
                        # Switch back to browser
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(0.5)
                
                self.executing = False
                self.status_label.config(text=f"✅ Hoàn thành {loop_count} vòng lặp!")
                messagebox.showinfo("Thành công", f"Đã hoàn thành {loop_count} vòng lặp!")
                
            except Exception as e:
                self.executing = False
                self.status_label.config(text=f"❌ Lỗi: {str(e)}")
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        
        thread = threading.Thread(target=execute_thread, daemon=True)
        thread.start()
        
        # ESC to stop
        def on_esc(key):
            if key == keyboard.Key.esc and self.executing:
                self.executing = False
                self.status_label.config(text="Đã dừng bởi người dùng")
                messagebox.showinfo("Thông báo", "Đã dừng thực thi")
                return False
        
        keyboard.on_press(on_esc)
    
    def run(self):
        """Run GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoOperationGUI()
    app.run()
