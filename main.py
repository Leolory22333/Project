from address_book import AddressBook

def print_help():
    print("=" * 50)
    print("📖 通讯录管理系统 - 导航菜单")
    print("=" * 50)
    print("ADD <姓名> <电话> [备注]  - 添加联系人")
    print("DEL <电话>               - 根据手机号删除联系人")
    print("FIND_NAME <前缀>         - 按姓名前缀检索")
    print("FIND_PHONE <前缀>        - 按电话前缀检索")
    print("LIST                     - 列出所有联系人")
    print("SAVE                     - 手动触发持久化")
    print("HELP                     - 查看帮助")
    print("EXIT                     - 退出系统")
    print("=" * 50)

def main():
    # 初始化通讯录
    print("🔧 初始化通讯录")
    address_book = AddressBook()
    
    print("\n🎉 欢迎使用通讯录管理系统！输入 HELP 查看命令说明")
    print_help()

    # 交互循环
    while True:
        try:
            cmd = input("\n请输入命令 > ").strip()
            if not cmd:
                continue
            parts = cmd.split(maxsplit=3)
            main_cmd = parts[0].upper()

            # 命令解析
            if main_cmd == "ADD":
                if len(parts) < 3:
                    print("❌ 参数错误：ADD 需要 姓名、电话，可选备注")
                    continue
                name = parts[1]
                phone = parts[2]
                remark = parts[3] if len(parts) >=4 else ""
                print(address_book.add_contact(name, phone, remark))

            elif main_cmd == "DEL":
                if len(parts) < 2:
                    print("❌ 参数错误：DEL 需要 手机号")
                    continue
                phone = parts[1]
                print(address_book.delete_contact(phone))

            elif main_cmd == "FIND_NAME":
                if len(parts) < 2:
                    print("❌ 参数错误：FIND_NAME 需要 姓名前缀")
                    continue
                prefix = parts[1]
                contacts = address_book.find_by_name_prefix(prefix)
                if not contacts:
                    print("📭 未找到匹配的联系人")
                else:
                    print(f"🔍 找到 {len(contacts)} 条匹配结果：")
                    for i, c in enumerate(contacts, 1):
                        print(f"  {i}. {c}")

            elif main_cmd == "FIND_PHONE":
                if len(parts) < 2:
                    print("❌ 参数错误：FIND_PHONE 需要 电话前缀")
                    continue
                prefix = parts[1]
                contacts = address_book.find_by_phone_prefix(prefix)
                if not contacts:
                    print("📭 未找到匹配的联系人")
                else:
                    print(f"🔍 找到 {len(contacts)} 条匹配结果：")
                    for i, c in enumerate(contacts, 1):
                        print(f"  {i}. {c}")

            elif main_cmd == "LIST":
                all_contacts = address_book.get_all_contacts()
                if not all_contacts:
                    print("📂 通讯录为空")
                else:
                    print(f"📂 通讯录共 {len(all_contacts)} 条记录：")
                    for idx, contact in enumerate(all_contacts, 1):
                        print(f"  {idx}. {contact}")

            elif main_cmd == "SAVE":
                address_book.persistence.save(address_book.get_all_contacts())

            elif main_cmd == "HELP":
                print_help()

            elif main_cmd == "EXIT":
                print("👋 退出系统，已自动持久化数据！")
                address_book.persistence.save(address_book.get_all_contacts())
                break

            else:
                print(f"❌ 未知命令：{main_cmd}，输入 HELP 查看帮助")

        except Exception as e:
            print(f"❌ 命令执行失败：{e}")

if __name__ == "__main__":
    main()