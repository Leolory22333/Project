import re
from typing import List
def generate_all_prefixes(s: str) -> List[str]:
    """生成字符串的所有前缀（如"138" → ["1", "13", "138"]）"""
    return [s[:i+1] for i in range(len(s))] if s else []

def validate_phone(phone: str) -> bool:
    """
    校验手机号合法性（核心：11位数字 + 国内手机号格式）
    :param phone: 待校验的手机号字符串
    :return: 合法返回True，否则False
    """
    if not isinstance(phone, str):
        return False
    
    # 步骤1：先做位数检查（必须11位）
    if len(phone.strip()) != 11:
        return False
    
    # 步骤2：再做格式检查（1开头，第二位3-9，后9位为数字）
    phone_pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(phone_pattern, phone.strip()))

def sanitize_input(text: str) -> str:
    """
    清洗用户输入，去除空格、特殊字符
    """
    if not isinstance(text, str):
        return ""
    return text.strip().replace("|", "").replace("\n", "").replace("\r", "")