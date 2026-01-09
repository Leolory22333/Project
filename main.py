#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from address_book import AddressBook
from utils.helpers import validate_phone, sanitize_input

# 全局变量：通讯录核心实例，供分页函数和输入函数调用
address_book = None

def print_help() -> None:
    """
    打印命令帮助信息，引导用户正确操作
    """
    help_text = """
=====================================================
📖 通讯录管理系统 - 命令说明
=====================================================
1. ADD <姓名> <电话> [备注]  - 添加/更新联系人（手机号唯一，需11位合法格式）
   示例：ADD 张三 13800138000 同事
2. DEL <电话>               - 根据手机号删除联系人（需11位合法格式）
   示例：DEL 13800138000
3. FIND_NAME <前缀>         - 按姓名前缀检索联系人
   示例：FIND_NAME 李
4. FIND_PHONE <前缀>        - 按手机号前缀检索联系人
   示例：FIND_PHONE 138
5. LIST                     - 列出所有联系人（按添加顺序）
6. SAVE                     - 手动触发数据持久化
7. HELP                     - 查看本帮助信息
8. EXIT                     - 退出系统（自动持久化）
=====================================================
📌 提示：检索结果最多展示10条，支持NEXT/PREV翻页，BACK返回主菜单
📌 所有操作自动持久化，临时文件保留在当前目录（address_book.dat.tmp）
📌 手机号必须为11位国内合法格式（以13/14/15/17/18/19开头）
=====================================================
    """
    print(help_text)

def get_valid_phone(prompt_tip: str) -> str:
    """
    核心新增：获取合法的11位手机号，不满足要求则强制重新输入
    :param prompt_tip: 输入提示文案（提升用户体验）
    :return: 清洗后的11位合法手机号字符串
    """
    while True:
        # 1. 接收用户原始输入
        phone_input = input(prompt_tip).strip()
        
        # 2. 清洗输入数据（去除空格、分隔符、换行符等非法字符）
        cleaned_phone = sanitize_input(phone_input)
        
        # 3. 校验手机号合法性（优先检查11位位数，再检查格式）
        if validate_phone(cleaned_phone):
            # 校验通过，直接返回合法手机号
            return cleaned_phone
        else:
            # 校验失败，提示详细原因并重新循环输入
            print("\n❌ 输入无效！手机号需满足以下两个条件：")
            print("  1. 长度必须为11位纯数字（无空格、无特殊字符）")
            print("  2. 符合国内手机号格式（以13/14/15/17/18/19开头）")
            print("🔔 请重新输入正确的11位手机号\n")

def pagination_interaction(contacts: list, search_type: str, elapsed_time: float) -> None:
    """
    分页交互逻辑：展示检索结果，支持NEXT/PREV翻页、BACK返回主菜单
    :param contacts: 匹配的联系人完整列表
    :param search_type: 检索类型（姓名/电话/全部）
    :param elapsed_time: 检索耗时（秒），用于展示性能
    """
    # 无匹配结果的处理
    if not contacts:
        print(f"\n🔍 {search_type}前缀检索结果 | 耗时：{elapsed_time:.6f} 秒")
        print("📭 未找到匹配的联系人")
        return

    # 初始化分页参数
    page = 1
    page_size = 10  # 每页默认展示10条数据

    # 首次获取分页数据（自动修正越界页码）
    paginated_data, total_pages, total, page = address_book.get_paginated_contacts(
        contacts, page, page_size
    )

    # 打印首次分页结果（含核心信息）
    print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条 | 耗时：{elapsed_time:.6f} 秒")
    print("-" * 60)
    for i, contact in enumerate(paginated_data, 1):
        # 计算全局连续序号（符合用户认知，不每页重新从1开始）
        global_idx = (page - 1) * page_size + i
        print(f"  {global_idx}. {contact}")
    print("-" * 60)

    # 多页场景下的翻页交互循环
    while True:
        # 根据总页数展示不同的操作提示
        if total_pages > 1:
            prompt = "操作提示：输入 NEXT 下一页 | PREV 上一页 | BACK 返回主菜单\n请输入操作指令 > "
        else:
            prompt = "操作提示：输入 BACK 返回主菜单\n请输入操作指令 > "
        
        # 接收用户翻页指令并统一转大写（兼容大小写输入）
        cmd = input(prompt).strip().upper()

        if cmd == "NEXT":
            # 下一页：页码+1，自动修正越界
            page += 1
            paginated_data, total_pages, total, page = address_book.get_paginated_contacts(
                contacts, page, page_size
            )
            # 重新打印当前页数据
            print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条")
            print("-" * 60)
            for i, contact in enumerate(paginated_data, 1):
                global_idx = (page - 1) * page_size + i
                print(f"  {global_idx}. {contact}")
            print("-" * 60)

        elif cmd == "PREV":
            # 上一页：页码-1，自动修正越界
            page -= 1
            paginated_data, total_pages, total, page = address_book.get_paginated_contacts(
                contacts, page, page_size
            )
            # 重新打印当前页数据
            print(f"\n🔍 {search_type}前缀检索结果 - 第 {page}/{total_pages} 页 | 共 {total} 条")
            print("-" * 60)
            for i, contact in enumerate(paginated_data, 1):
                global_idx = (page - 1) * page_size + i
                print(f"  {global_idx}. {contact}")
            print("-" * 60)

        elif cmd == "BACK":
            # 返回主菜单，退出分页交互循环
            print("🔙 返回主菜单")
            break

        else:
            # 无效指令提示，保持循环不退出
            print("❌ 无效指令！仅支持输入 NEXT/PREV/BACK（大小写均可）")

def main() -> None:
    """
    程序主入口：初始化系统，处理命令行交互循环
    核心修改：ADD/DEL命令集成手机号合法输入逻辑，强制重新输入非法手机号
    """
    global address_book

    # 1. 初始化通讯录系统
    print("🔧 初始化通讯录管理系统（散列表索引+手机号严格校验版）...")
    address_book = AddressBook()

    # 2. 打印欢迎信息和帮助文档
    print("\n🎉 欢迎使用通讯录管理系统！输入 HELP 查看命令说明")
    print_help()

    # 3. 命令行交互主循环
    while True:
        try:
            # 接收用户原始命令输入
            cmd_input = input("\n请输入命令 > ").strip()
            if not cmd_input:
                # 空输入直接跳过，重新等待命令
                continue

            # 拆分命令（maxsplit=3 保留备注中的空格字符）
            cmd_parts = cmd_input.split(maxsplit=3)
            main_cmd = cmd_parts[0].upper()  # 主命令转大写，兼容大小写输入

            # ========== 1. ADD 命令：添加/更新联系人（集成手机号合法输入） ==========
            if main_cmd == "ADD":
                # 步骤1：获取并清洗联系人姓名（非空校验）
                name = input("请输入联系人姓名 > ").strip()
                name = sanitize_input(name)
                if not name:
                    print("❌ 添加失败：姓名不能为空，请重新执行ADD命令")
                    continue

                # 步骤2：获取合法手机号（核心修改：非法则重新输入）
                phone = get_valid_phone("请输入联系人手机号（11位合法格式） > ")

                # 步骤3：获取并清洗联系人备注（可选，允许空值）
                remark = input("请输入联系人备注（可选，直接回车留空） > ").strip()
                remark = sanitize_input(remark)

                # 步骤4：调用后端核心逻辑，执行添加操作
                result = address_book.add_contact(name, phone, remark)
                print(result)

            # ========== 2. DEL 命令：删除联系人（集成手机号合法输入） ==========
            elif main_cmd == "DEL":
                # 步骤1：获取合法手机号（核心修改：非法则重新输入）
                phone = get_valid_phone("请输入要删除的联系人手机号（11位合法格式） > ")

                # 步骤2：调用后端核心逻辑，执行删除操作
                result = address_book.delete_contact(phone)
                print(result)

            # ========== 3. FIND_NAME 命令：按姓名前缀检索 ==========
            elif main_cmd == "FIND_NAME":
                if len(cmd_parts) < 2:
                    print("❌ 参数错误：FIND_NAME 命令格式为 FIND_NAME <前缀>")
                    continue
                prefix = cmd_parts[1]
                # 调用后端检索函数（返回结果+耗时）
                contacts, elapsed_time = address_book.find_by_name_prefix(prefix)
                # 进入分页交互展示结果
                pagination_interaction(contacts, "姓名", elapsed_time)

            # ========== 4. FIND_PHONE 命令：按手机号前缀检索 ==========
            elif main_cmd == "FIND_PHONE":
                if len(cmd_parts) < 2:
                    print("❌ 参数错误：FIND_PHONE 命令格式为 FIND_PHONE <前缀>")
                    continue
                prefix = cmd_parts[1]
                # 调用后端检索函数（返回结果+耗时）
                contacts, elapsed_time = address_book.find_by_phone_prefix(prefix)
                # 进入分页交互展示结果
                pagination_interaction(contacts, "电话", elapsed_time)

            # ========== 5. LIST 命令：全量列出所有联系人 ==========
            elif main_cmd == "LIST":
                contacts, elapsed_time = address_book.get_all_contacts()
                # 进入分页交互展示结果
                pagination_interaction(contacts, "全部", elapsed_time)

            # ========== 6. SAVE 命令：手动触发数据持久化 ==========
            elif main_cmd == "SAVE":
                success = address_book.persistence.save(address_book.get_all_contacts())
                if not success:
                    print("❌ 手动持久化失败，请检查文件写入权限")

            # ========== 7. HELP 命令：打印帮助信息 ==========
            elif main_cmd == "HELP":
                print_help()

            # ========== 8. EXIT 命令：退出系统（自动持久化） ==========
            elif main_cmd == "EXIT":
                print("👋 正在退出系统，自动持久化数据...")
                # 退出前触发最后一次持久化，保证数据不丢失
                address_book.persistence.save(address_book.get_all_contacts())
                print("✅ 数据已成功持久化，系统安全退出！")
                break

            # ========== 未知命令处理 ==========
            else:
                print(f"❌ 未知命令：{main_cmd}，输入 HELP 查看支持的命令列表")

        # ========== 全局异常捕获：避免程序崩溃 ==========
        except Exception as e:
            print(f"❌ 命令执行失败：{str(e)}（请检查输入格式或联系开发者）")

# 程序入口保护：仅直接运行该文件时执行主逻辑
if __name__ == "__main__":
    main()