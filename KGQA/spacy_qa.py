import spacy

# 加载预训练的中文模型
# disable=["parser", "attribute_ruler"] 可以禁用不需要的组件，提高加载和处理速度
nlp = spacy.load("zh_core_web_sm", disable=["parser", "attribute_ruler"])
try:
    nlp = spacy.load("zh_core_web_sm", disable=["parser", "attribute_ruler"])
except Exception:
    # 提供后备处理方案
    nlp = None

# 定义一个关系关键词列表，用于从问题中识别关系
# 这个列表基于neo_db/config.py中的similar_words字典，确保涵盖所有可能的关系
RELATIONSHIP_KEYWORDS = [
    "父亲", "母亲", "儿子", "女儿", "丈夫", "妻子", "哥哥", "弟弟", 
    "姐姐", "妹妹", "爷爷", "奶奶", "外祖母", "朋友", "老师", "丫环", "妾",
    "爸爸", "妈妈", "爸", "妈", "兄弟", "老婆", "表妹", "养父", "娘", 
    "爹", "father", "mother", "孙子", "老公", "岳母", "表兄妹", "孙女", "嫂子", "暧昧"
]

# 红楼梦常见人物名单，帮助更准确地提取人名
HLM_CHARACTERS = [
    "贾宝玉", "林黛玉", "薛宝钗", "王熙凤", "贾母", "贾政", "贾赦", "贾珍", "贾环",
    "贾迎春", "贾探春", "贾惜春", "贾元春", "秦可卿", "史湘云", "妙玉", "王夫人",
    "薛姨妈", "贾琏", "贾蓉", "贾蔷", "贾芸", "贾兰", "贾芹", "尤氏", "平儿",
    "鸳鸯", "袭人", "晴雯", "麝月", "紫鹃", "李纨", "香菱", "甄士隐", "贾雨村"
]

def extract_entity_and_relation(question: str):
    """
    使用 spaCy 从问题中提取人物实体和关系关键词。
    
    Args:
        question: 用户输入的自然语言问题，例如 "贾宝玉的父亲是谁？"

    Returns:
        一个包含实体和关系的列表，例如 ['贾宝玉', '父亲', 'n']。
        如果找不到，则返回 None。
    """
    person = None
    relation = None

    # 方法1: 直接检查问题中是否包含已知人物名称
    for character in HLM_CHARACTERS:
        if character in question:
            person = character
            break

    # 方法2: 使用 spaCy 处理问题文本
    if not person and nlp:
        try:
            doc = nlp(question)
            # 提取人物实体 (Named Entity Recognition)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    person = ent.text
                    break  # 找到第一个人名后就停止
        except Exception:
            pass
    
    # 方法3: 通过简单的字符分割尝试提取
    if not person and "的" in question:
        possible_person = question.split("的")[0].strip()
        if possible_person and len(possible_person) >= 2:  # 确保人名至少有两个字
            person = possible_person

    # 提取关系关键词
    for keyword in RELATIONSHIP_KEYWORDS:
        if keyword in question:
            relation = keyword
            break  # 找到第一个关系后就停止
    
    # 如果成功找到了人物和关系，则返回一个列表，以兼容旧的图谱查询函数
    if person and relation:
        result = [person, relation, "n"]  # 添加一个补位元素"n"，兼容旧函数长度要求
        return result
    
    return None

# 为了完全兼容旧代码，我们可以提供与原ltp.py相同的函数名
def get_target_array(question: str):
    """
    兼容旧代码的函数名，实际调用extract_entity_and_relation
    """
    if not question or len(question.strip()) == 0:
        return None
        
    return extract_entity_and_relation(question)