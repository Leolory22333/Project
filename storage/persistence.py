import os
import shutil
from typing import List, Dict

class PersistenceManager:
    """原子化持久化管理类：负责数据加载和保存，保证一致性"""
    def __init__(self, filepath: str = "address_book.dat"):
        self.filepath = filepath  # 正式数据文件
        self.tmp_filepath = f"{filepath}.tmp"  # 临时文件（原子写入用）

    def save(self, contacts: List[object]) -> bool:
        """保存联系人数据到文件（原子操作）"""
        try:
            # 1. 先写入临时文件
            with open(self.tmp_filepath, "w", encoding="utf-8") as f:
                for contact in contacts:
                    # 格式：姓名|电话|备注
                    line = f"{contact.name}|{contact.phone}|{contact.remark}\n"
                    f.write(line)
            # 2. 原子重命名替换正式文件
            shutil.move(self.tmp_filepath, self.filepath)
            print(f"✅ 持久化成功：写入 {len(contacts)} 条记录到 {self.filepath}")
            return True
        except Exception as e:
            print(f"❌ 持久化失败：{e}")
            return False

    def load(self) -> List[Dict]:
        """加载数据：优先读正式文件，失败则读临时文件"""
        # 确定加载路径
        load_path = self.filepath if os.path.exists(self.filepath) else self.tmp_filepath
        contacts_data = []
        
        if not os.path.exists(load_path):
            return contacts_data
        
        try:
            with open(load_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # 解析行数据（兼容缺失备注的情况）
                    parts = line.split("|", 2)
                    contact_dict = {
                        "name": parts[0],
                        "phone": parts[1],
                        "remark": parts[2] if len(parts) > 2 else ""
                    }
                    contacts_data.append(contact_dict)
            
            # 临时文件加载成功后，同步到正式文件
            if load_path == self.tmp_filepath:
                shutil.move(self.tmp_filepath, self.filepath)
            print(f"✅ 加载成功：从 {load_path} 读取 {len(contacts_data)} 条记录")
        except Exception as e:
            print(f"❌ 加载失败：{e}")
        
        return contacts_data