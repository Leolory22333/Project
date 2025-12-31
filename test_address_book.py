import unittest
import os
from address_book import AddressBook
from contact import Contact

class TestAddressBook(unittest.TestCase):
    """通讯录单元测试（散列表索引版）"""
    # 测试前初始化
    def setUp(self):
        # 临时测试文件，避免污染正式数据
        self.test_file = "test_address_book.dat"
        self.test_tmp_file = f"{self.test_file}.tmp"
        
        # 清理旧测试文件
        for f in [self.test_file, self.test_tmp_file]:
            if os.path.exists(f):
                os.remove(f)
        
        # 初始化通讯录（固定散列表索引）
        self.ab = AddressBook()
        # 替换持久化文件路径为测试文件
        self.ab.persistence.filepath = self.test_file
        self.ab.persistence.tmp_filepath = self.test_tmp_file

    # 测试后清理
    def tearDown(self):
        for f in [self.test_file, self.test_tmp_file]:
            if os.path.exists(f):
                os.remove(f)

    # 测试添加联系人
    def test_add_contact(self):
        result = self.ab.add_contact("张三", "13800138000", "同事")
        self.assertIn("添加成功", result)
        self.assertEqual(len(self.ab.get_all_contacts()), 1)
        self.assertEqual(self.ab.phone_map["13800138000"].name, "张三")

    # 测试重复添加（覆盖）
    def test_add_duplicate_phone(self):
        self.ab.add_contact("张三", "13800138000")
        result = self.ab.add_contact("张三2", "13800138000", "家人")
        self.assertIn("添加成功", result)
        self.assertEqual(len(self.ab.get_all_contacts()), 1)
        self.assertEqual(self.ab.phone_map["13800138000"].name, "张三2")

    # 测试删除联系人
    def test_delete_contact(self):
        self.ab.add_contact("李四", "13900139000")
        result = self.ab.delete_contact("13900139000")
        self.assertIn("删除成功", result)
        self.assertEqual(len(self.ab.get_all_contacts()), 0)
        self.assertNotIn("13900139000", self.ab.phone_map)

    # 测试姓名前缀检索（散列表）
    def test_find_name_prefix(self):
        # 添加测试数据
        self.ab.add_contact("张三", "13800138000")
        self.ab.add_contact("张四", "13800138001")
        self.ab.add_contact("李四", "13900139000")
        
        # 检索"张"前缀
        contacts = self.ab.find_by_name_prefix("张")
        self.assertEqual(len(contacts), 2)
        # 检索"李"前缀
        contacts = self.ab.find_by_name_prefix("李")
        self.assertEqual(len(contacts), 1)
        # 检索不存在的前缀
        contacts = self.ab.find_by_name_prefix("王")
        self.assertEqual(len(contacts), 0)

    # 测试电话前缀检索（散列表）
    def test_find_phone_prefix(self):
        self.ab.add_contact("王五", "13700137000")
        self.ab.add_contact("赵六", "13700137001")
        self.ab.add_contact("孙七", "13800138000")
        
        # 检索"137"前缀
        contacts = self.ab.find_by_phone_prefix("137")
        self.assertEqual(len(contacts), 2)
        # 检索"138"前缀
        contacts = self.ab.find_by_phone_prefix("138")
        self.assertEqual(len(contacts), 1)

    # 测试持久化和加载
    def test_persistence(self):
        # 添加数据并保存
        self.ab.add_contact("周八", "13600136000", "朋友")
        self.ab.persistence.save(self.ab.get_all_contacts())
        
        # 新建通讯录实例，加载测试文件
        new_ab = AddressBook()
        new_ab.persistence.filepath = self.test_file
        new_ab._load_from_file()
        
        # 验证加载成功
        self.assertEqual(len(new_ab.get_all_contacts()), 1)
        self.assertEqual(new_ab.phone_map["13600136000"].name, "周八")

if __name__ == "__main__":
    unittest.main(verbosity=2)