import tkinter as tk
import os


class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.is_fullscreen = False  # وضعیت تمام‌صفحه
        self.normal_size = (600, 500)  # اندازه معمولی پنجره (عرض x ارتفاع)
        self.current_path = os.getcwd()  # مسیر فعلی (شروع از مسیر کاری)

        # پیکربندی پنجره اصلی
        self.root.geometry(f"{self.normal_size[0]}x{self.normal_size[1]}+100+100")

        # ایجاد و تنظیم نوار عنوان سفارشی
        self.title_bar = tk.Frame(self.root, bg='#004466', relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X)
        self.title_bar.bind('<ButtonPress-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)
        self.title_bar.bind('<Double-Button-1>', self.toggle_fullscreen)

        # عنوان اپلیکیشن در نوار عنوان
        self.title_label = tk.Label(self.title_bar, text="مدیریت فایل", bg='#004466', fg='white')
        self.title_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.title_label.bind('<ButtonPress-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.do_move)
        self.title_label.bind('<Double-Button-1>', self.toggle_fullscreen)

        # دکمه بستن (X) در نوار عنوان
        self.close_button = tk.Button(self.title_bar, text='✕', command=self.root.destroy,
                                      bg='#004466', fg='white', bd=0, padx=5, pady=2)
        self.close_button.pack(side=tk.RIGHT, padx=5)

        # نمایش مسیر فعلی
        self.path_label = tk.Label(self.root, text=self.current_path, anchor='w')
        self.path_label.pack(fill=tk.X, padx=5, pady=5)

        # ایجاد فریم برای لیست فایل‌ها و فولدرها
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # اسکرول بار برای لیست
        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # لیست فایل‌ها
        self.listbox = tk.Listbox(list_frame, yscrollcommand=self.scrollbar.set, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # دابل کلیک روی لیست (ورود به پوشه‌ها)
        self.listbox.bind('<Double-1>', self.open_folder)

        # دکمه‌های اضافه، حذف و سرچ
        self.add_button = tk.Button(self.root, text="➕ اضافه کردن فایل", command=self.create_folder)
        self.add_button.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.delete_button = tk.Button(self.root, text="➖ حذف فایل", command=self.delete_item)
        self.delete_button.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.search_button = tk.Button(self.root, text="🔍 جستجو", command=self.search_files)
        self.search_button.pack(fill=tk.X, padx=5, pady=(0, 5))

        # دکمه بازگشت (Back)
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(fill=tk.X, padx=5, pady=(0, 5))

        # پر کردن اولیه لیست بر اساس مسیر فعلی
        self.populate_list()

    def start_move(self, event):
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", False)
            self.root.geometry(f"{self.normal_size[0]}x{self.normal_size[1]}")
            self.is_fullscreen = False

        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        new_x = event.x_root - self.offset_x
        new_y = event.y_root - self.offset_y
        self.root.geometry(f"+{new_x}+{new_y}")

    def toggle_fullscreen(self, event=None):
        if not self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
            self.is_fullscreen = True
        else:
            self.root.attributes("-fullscreen", False)
            self.root.geometry(f"{self.normal_size[0]}x{self.normal_size[1]}")
            self.is_fullscreen = False

    def populate_list(self):
        self.listbox.delete(0, tk.END)
        try:
            items = os.listdir(self.current_path)
        except PermissionError:
            items = []

        items.sort(key=lambda s: s.lower())

        for item in items:
            full_path = os.path.join(self.current_path, item)
            if os.path.isdir(full_path):
                self.listbox.insert(tk.END, item + "/")
        for item in items:
            full_path = os.path.join(self.current_path, item)
            if not os.path.isdir(full_path):
                self.listbox.insert(tk.END, item)

    def open_folder(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        item_text = self.listbox.get(selection[0])
        if item_text.endswith('/'):
            folder_name = item_text.rstrip('/')
            new_path = os.path.join(self.current_path, folder_name)
            if os.path.isdir(new_path):
                self.current_path = new_path
                self.path_label.config(text=self.current_path)
                self.populate_list()

    def go_back(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.current_path = parent
            self.path_label.config(text=self.current_path)
            self.populate_list()

    def create_folder(self):
        new_folder_name = "New Folder"
        os.makedirs(os.path.join(self.current_path, new_folder_name), exist_ok=True)
        self.populate_list()

    def delete_item(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        item_text = self.listbox.get(selection[0])
        full_path = os.path.join(self.current_path, item_text)
        if os.path.isdir(full_path):
            os.rmdir(full_path)
        else:
            os.remove(full_path)
        self.populate_list()

    def search_files(self):
        search_query = "test"  # برای تست می‌توانید ورودی دلخواه بگذارید
        results = [f for f in os.listdir(self.current_path) if search_query.lower() in f.lower()]
        self.listbox.delete(0, tk.END)
        for result in results:
            self.listbox.insert(tk.END, result)
