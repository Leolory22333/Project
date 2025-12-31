from contact import Contact
from index import HashPrefixIndex  # 仅导入散列表索引
from storage import PersistenceManager

class AddressBook:
    """通讯录核心管理类：双向链表+散列表索引+原子持久化"""
    def __init__(self):
        # 双向链表：哨兵头节点
        self.head = Contact("", "")
        self.head.prev = self.head
        self.head.next = self.head
        
        # 手机号映射
        self.phone_map = {}
        
        # 仅使用散列表索引
        self.name_index = HashPrefixIndex()
        self.phone_index = HashPrefixIndex()
        
        # 持久化管理器
        self.persistence = PersistenceManager()
        
        # 初始化：从文件加载数据
        self._load_from_file()

    def _load_from_file(self):
        """从文件加载联系人数据到内存"""
        contacts_data = self.persistence.load()
        for data in contacts_data:
            # 加载时不重复持久化（避免循环写入）
            self.add_contact(
                name=data["name"],
                phone=data["phone"],
                remark=data["remark"],
                persist=False
            )

    def add_contact(self, name: str, phone: str, remark: str = "", persist: bool = True) -> str:
        """添加联系人：手机号唯一，重复则覆盖"""
        # 1. 手机号已存在 → 删除旧联系人
        if phone in self.phone_map:
            self.delete_contact(phone, persist=False)
        
        # 2. 创建新联系人，插入双向链表尾部
        new_contact = Contact(name, phone, remark)
        tail = self.head.prev
        tail.next = new_contact
        new_contact.prev = tail
        new_contact.next = self.head
        self.head.prev = new_contact
        
        # 3. 更新映射和散列表索引
        self.phone_map[phone] = new_contact
        self.name_index.insert(name, new_contact)
        self.phone_index.insert(phone, new_contact)
        
        # 4. 持久化（可选）
        if persist:
            self.persistence.save(self.get_all_contacts())
        
        return f"✅ 添加成功：{new_contact}"

    def delete_contact(self, phone: str, persist: bool = True) -> str:
        """根据手机号删除联系人"""
        #手机号不存在
        if phone not in self.phone_map:
            return f"❌ 删除失败：手机号 {phone} 不存在"
        
        #从链表移除
        contact = self.phone_map[phone]
        contact.prev.next = contact.next
        contact.next.prev = contact.prev
        
        #从散列表索引和映射移除
        self.name_index.delete(contact.name, contact)
        self.phone_index.delete(contact.phone, contact)
        del self.phone_map[phone]
        
        #持久化
        if persist:
            self.persistence.save(self.get_all_contacts())
        
        return f"✅ 删除成功：{contact}"

    def find_by_name_prefix(self, prefix: str, max_limit: int = 10) -> list:
        """按姓名前缀检索，返回最多max_limit条结果"""
        contacts = self.name_index.search(prefix)
        # 截断并提示
        if len(contacts) > max_limit:
            print(f"💡 提示：匹配结果共 {len(contacts)} 条，仅展示前 {max_limit} 条")
            return contacts[:max_limit]
        return contacts

    def find_by_phone_prefix(self, prefix: str, max_limit: int = 10) -> list:
        """按电话前缀检索，返回最多max_limit条结果"""
        contacts = self.phone_index.search(prefix)
        if len(contacts) > max_limit:
            print(f"💡 提示：匹配结果共 {len(contacts)} 条，仅展示前 {max_limit} 条")
            return contacts[:max_limit]
        return contacts

    def get_all_contacts(self) -> list:
        """遍历所有联系人，返回列表"""
        contacts_list = []
        current_node = self.head.next
        while current_node != self.head:
            contacts_list.append(current_node)
            current_node = current_node.next
        return contacts_list