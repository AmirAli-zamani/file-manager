import os
import shutil
from utils import exists
from config import DEFAULT_PATH


# لیست کردن فایل‌ها و پوشه‌ها
def list_files(path=DEFAULT_PATH):
    try:
        if not os.path.exists(path):
            return [f"⚠️ Error: Path '{path}' does not exist."]

        return [f"📁 {item}" if os.path.isdir(os.path.join(path, item)) else f"📄 {item}" for item in os.listdir(path)]
    except Exception as e:
        return [f"⚠️ Error: {str(e)}"]


# ایجاد یک پوشه جدید
def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        return f"⚠️ Error creating folder: {str(e)}"


# حذف فایل یا پوشه
def delete_item(path):
    try:
        if not exists(path):
            return f"⚠️ Error: Path '{path}' does not exist."

        if os.path.isdir(path):
            shutil.rmtree(path)  # حذف پوشه
        else:
            os.remove(path)  # حذف فایل
        return f"✅ {path} deleted successfully."
    except PermissionError:
        return f"⚠️ Error: Permission denied to delete {path}."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# جستجو در فایل‌ها
def search_files(query, path="."):
    try:
        if not os.path.exists(path):
            return [f"⚠️ Error: Path '{path}' does not exist."]

        results = []
        for item in os.listdir(path):
            if query.lower() in item.lower():
                full_path = os.path.join(path, item)
                prefix = "📁" if os.path.isdir(full_path) else "📄"
                results.append(f"{prefix} {item}")

        if not results:
            return ["❌ No matching files found."]
        return results
    except Exception as e:
        return [f"⚠️ Error: {str(e)}"]
