class Contact:
    """联系人实体类，封装属性和双向链表节点指针"""
    def __init__(self, name: str, phone: str, remark: str = ""):
        self.name = name
        self.phone = phone
        self.remark = remark
        self.prev = None  # 前驱节点
        self.next = None  # 后继节点

    def to_dict(self) -> dict:
        """转换为字典，便于持久化/序列化"""
        return {"name": self.name, "phone": self.phone, "remark": self.remark}

    @staticmethod
    def from_dict(data: dict) -> "Contact":
        """从字典重建联系人对象"""
        return Contact(data["name"], data["phone"], data.get("remark", ""))

    def __str__(self) -> str:
        """自定义打印格式"""
        return f"{self.name} | {self.phone} | 备注：{self.remark}"