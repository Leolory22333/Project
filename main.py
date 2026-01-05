import time
from address_book import AddressBook

def print_help():
    print("=" * 50)
    print("📖 通讯录管理系统 - 命令说明（散列表索引版）")
    print("=" * 50)
    print("ADD <姓名> <电话> [备注]  - 添加联系人（手机号唯一）")
    print("DEL <电话>               - 根据手机号删除联系人")
    print("FIND_NAME <前缀>         - 按姓名前缀检索")
    print("FIND_PHONE <前缀>        - 按电话前缀检索")
    print("LIST                     - 列出所有联系人")
    print("SAVE                     - 手动触发持久化")
    print("HELP                     - 查看帮助")
    print("EXIT                     - 退出系统")
    print("📌 检索后可输入 NEXT/PREV 翻页，输入 BACK 返回主菜单")
    print("📌 检索结果将显示本次查询耗时（单位：秒）")
    print("=" * 50)

# 计时器函数
def calculate_search_time(func):
    """
    计算检索函数执行时间的装饰器
    :param func: 检索函数
    :return: 包装后的函数，返回 (结果, 耗时)
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 高精度
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time  # 耗时
        return result, elapsed_time
    return wrapper

# 分页交互函数
def pagination_interaction(contacts: list, search_type: str, elapsed_time: float):
    """
    检索结果分页交互（新增耗时展示）
    :param contacts: 全部匹配的联系人列表
    :param search_type: 检索类型（姓名/电话/全部）
    :param elapsed_time: 检索耗时（秒）
    """
    if not contacts:
        print(f"\n🔍 {search_type}前缀检索结果 | 耗时：{elapsed_time:.6f} 秒")
        print("📭 未找到匹配的联系人")
        return
    
    page = 1
    page_size = 10
    total = len(contacts)
    paginated_data, total_pages, _, page = address_book.get_paginated_contacts(contacts, page, page_size)
    
    # 首次展示时打印检索耗时
    print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条 | 耗时：{elapsed_time:.6f} 秒")
    print("-" * 60)
    if paginated_data:
        for i, c in enumerate(paginated_data, 1):
            # 计算全局序号
            global_idx = (page - 1) * page_size + i
            print(f"  {global_idx}. {c}")
    else:
        print("  暂无数据")
    print("-" * 60)
    
    # 打印分页提示
    while True:
        if total_pages > 1:
            print("操作提示：输入 NEXT 下一页 | PREV 上一页 | BACK 返回主菜单")
        else:
            print("操作提示：输入 BACK 返回主菜单")
        
        # 接收用户分页指令
        cmd = input("请输入操作指令 > ").strip().upper()
        if cmd == "NEXT":
            page += 1
            paginated_data, total_pages, _, page = address_book.get_paginated_contacts(contacts, page, page_size)
            # 翻页时仅更新页码，不重复计时
            print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条")
            print("-" * 60)
            if paginated_data:
                for i, c in enumerate(paginated_data, 1):
                    global_idx = (page - 1) * page_size + i
                    print(f"  {global_idx}. {c}")
            else:
                print("  暂无数据")
            print("-" * 60)
        elif cmd == "PREV":
            page -= 1
            paginated_data, total_pages, _, page = address_book.get_paginated_contacts(contacts, page, page_size)
            print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条")
            print("-" * 60)
            if paginated_data:
                for i, c in enumerate(paginated_data, 1):
                    global_idx = (page - 1) * page_size + i
                    print(f"  {global_idx}. {c}")
            else:
                print("  暂无数据")
            print("-" * 60)
        elif cmd == "BACK":
            print("🔙 返回主菜单")
            break
        else:
            print("❌ 无效指令，请输入 NEXT/PREV/BACK")

def main():
    """命令行交互主逻辑（仅散列表索引）"""
    # 初始化通讯录
    print("🔧 初始化通讯录（散列表索引）...")
    global address_book  # 全局变量
    address_book = AddressBook()
    
    # 计时器
    timed_find_name = calculate_search_time(address_book.find_by_name_prefix)
    timed_find_phone = calculate_search_time(address_book.find_by_phone_prefix)
    timed_list_all = calculate_search_time(address_book.get_all_contacts)
    
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
                # 带计时的检索
                all_contacts, elapsed_time = timed_find_name(prefix)
                # 进入分页交互
                pagination_interaction(all_contacts, "姓名", elapsed_time)

            elif main_cmd == "FIND_PHONE":
                if len(parts) < 2:
                    print("❌ 参数错误：FIND_PHONE 需要 电话前缀")
                    continue
                prefix = parts[1]
                # 带计时的检索
                all_contacts, elapsed_time = timed_find_phone(prefix)
                # 进入分页交互
                pagination_interaction(all_contacts, "电话", elapsed_time)

            elif main_cmd == "LIST":
                # 带计时的全量检索
                all_contacts, elapsed_time = timed_list_all()
                # 进入分页交互
                pagination_interaction(all_contacts, "全部", elapsed_time)

            elif main_cmd == "SAVE":
                address_book.persistence.save(address_book.get_all_contacts())
                print("✅ 手动持久化完成")

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