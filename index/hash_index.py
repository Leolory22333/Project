class HashPrefixIndex:
    """基于散列表的前缀索引，支持插入、删除、前缀检索"""
    def __init__(self):
        # 键：前缀字符串；值：联系人集合（去重）
        self.index = {}

    def insert(self, keyword: str, contact: object):
        """插入关键词（姓名/电话）关联的联系人，生成所有前缀"""
        prefixes = [keyword[:i+1] for i in range(len(keyword))] if keyword else []
        for prefix in prefixes:
            if prefix not in self.index:
                self.index[prefix] = set()
            self.index[prefix].add(contact)

    def delete(self, keyword: str, contact: object):
        """删除关键词关联的联系人，清理空前缀键"""
        prefixes = [keyword[:i+1] for i in range(len(keyword))] if keyword else []
        for prefix in prefixes:
            if prefix in self.index and contact in self.index[prefix]:
                self.index[prefix].remove(contact)
                # 空集合清理，减少内存占用
                if not self.index[prefix]:
                    del self.index[prefix]

    def search(self, prefix: str) -> list:
        """前缀检索，返回匹配的联系人列表"""
        return list(self.index.get(prefix, set()))