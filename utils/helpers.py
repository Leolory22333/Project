def generate_all_prefixes(s: str) -> List[str]:
    """生成字符串的所有前缀（如"138" → ["1", "13", "138"]）"""
    return [s[:i+1] for i in range(len(s))] if s else []