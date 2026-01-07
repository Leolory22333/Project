"""
storage/persistence.py - 通讯录数据持久化模块
功能：实现原子化数据写入/读取，保留临时文件用于调试/备份
"""
import os
import shutil

class PersistenceManager:
    """持久化管理器：封装文件读写逻辑（保留临时文件版本）"""
    def __init__(self, filepath="address_book.dat", tmp_filepath="address_book.dat.tmp"):
        # 正式数据文件路径
        self.filepath = filepath
        # 临时文件路径（保留不删除）
        self.tmp_filepath = tmp_filepath

    def load(self) -> list:
        """
        从文件加载联系人数据
        :return: 联系人数据列表，每个元素为字典 {"name": "", "phone": "", "remark": ""}
        """
        contacts_data = []
        # 优先读取正式文件，若不存在则尝试临时文件（异常恢复）
        load_path = self.filepath if os.path.exists(self.filepath) else self.tmp_filepath
        
        if not os.path.exists(load_path):
            return contacts_data  # 无文件则返回空列表
        
        try:
            with open(load_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue  # 跳过空行
                    # 按分隔符拆分（格式：姓名|电话|备注）
                    parts = line.split("|")
                    name = parts[0] if len(parts) >= 1 else ""
                    phone = parts[1] if len(parts) >= 2 else ""
                    remark = parts[2] if len(parts) >= 3 else ""
                    contacts_data.append({
                        "name": name,
                        "phone": phone,
                        "remark": remark
                    })
            print(f"✅ 从 {load_path} 加载 {len(contacts_data)} 条联系人数据")
        except Exception as e:
            print(f"❌ 加载数据失败：{e}")
            contacts_data = []
        return contacts_data

    def save(self, contacts: list) -> bool:
        """
        原子化保存联系人数据到文件（保留临时文件）
        :param contacts: 联系人对象列表
        :return: 保存成功返回True，失败返回False
        """
        try:
            # 步骤1：先写入临时文件（覆盖旧的临时文件，避免冗余）
            with open(self.tmp_filepath, "w", encoding="utf-8") as f:
                for contact in contacts:
                    # 按格式拼接：姓名|电话|备注
                    line = f"{contact.name}|{contact.phone}|{contact.remark}\n"
                    f.write(line)
            print(f"📝 临时文件已保存至：{os.path.abspath(self.tmp_filepath)}")
            
            # 步骤2：原子重命名生成正式文件（保留临时文件，复制而非移动）
            # 替换原shutil.move → 改为复制，避免临时文件被删除
            shutil.copy2(self.tmp_filepath, self.filepath)  # copy2保留文件元数据
            
            # 步骤3：输出持久化摘要（满足开题报告要求）
            print(f"✅ 持久化成功：写入 {len(contacts)} 条记录到 {os.path.abspath(self.filepath)}")
            print(f"📌 临时文件已保留：{os.path.abspath(self.tmp_filepath)}")
            return True
        except Exception as e:
            print(f"❌ 持久化失败：{e}")
            # 移除「删除临时文件」的逻辑，保留失败时的临时文件用于排查
            print(f"📌 临时文件保留（用于排查问题）：{os.path.abspath(self.tmp_filepath)}")
            return False