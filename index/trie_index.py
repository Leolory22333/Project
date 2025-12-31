class TrieNode:
    """Trie树节点：存储子节点和关联的联系人"""
    def __init__(self):
        self.children = {}  # 子节点：{字符: TrieNode}
        self.contacts = set()  # 匹配当前前缀的联系人集合

class TrieIndex:
    """基于Trie树的前缀索引，支持插入、删除、前缀检索"""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, keyword: str, contact: object):
        """插入关键词（姓名/电话）关联的联系人"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.contacts.add(contact)

    def delete(self, keyword: str, contact: object):
        """删除关键词关联的联系人"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                return
            node = node.children[char]
            if contact in node.contacts:
                node.contacts.remove(contact)

    def search(self, prefix: str) -> list:
        """前缀检索，返回匹配的联系人列表"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.contacts)