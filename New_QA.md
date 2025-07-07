# 使用 spaCy 替代 Pyltp 实现问答功能方案

## 1. 目标与背景

本项目原有的问答功能依赖于 `pyltp` 库进行自然语言处理（NLP），以从用户提问中抽取出实体（如人名）和关系。然而，`pyltp` 存在以下问题：
- **安装复杂**：需要C++编译环境，对Windows用户尤其不友好。
- **模型陈旧**：官方提供的模型已久未更新。
- **维护不便**：社区活跃度较低。

为了解决这些问题，我们提出使用 `spaCy` 这一现代化、高性能的NLP库来替代 `pyltp`。

## 2. 为什么选择 spaCy？

- **安装简单**：通过 `pip` 即可轻松安装，无需复杂的环境配置。
- **模型先进**：提供高质量的预训练中文模型，能够准确地进行分词、词性标注和命名实体识别（NER）。
- **性能优异**：运行速度快，内存占用合理。
- **社区活跃**：拥有丰富的文档和活跃的社区支持。

本方案将利用 `spaCy` 的命名实体识别（NER）功能直接从问题中抽取出人名，并通过关键词匹配来识别关系，从而实现对原有问答功能的无缝替换，且无需改动图数据库的查询逻辑。

## 3. 详细实现步骤

### 第一步：环境准备

首先，需要安装 `spaCy` 库并下载其预训练的中文模型。

1.  **更新 `requirement.txt`**：
    将 `spacy` 添加到你的 `requirement.txt` 文件中，方便环境迁移。

2.  **安装 `spaCy`**：
    打开终端，执行以下命令：
    ```bash
    pip install -U spacy
    ```

3.  **下载中文模型**：
    继续在终端中执行以下命令，下载小版本的中文模型（`zh_core_web_sm`），它体积小，性能足够满足我们项目的需求。
    ```bash
    python -m spacy download zh_core_web_sm
    ```

### 第二步：创建新的问答处理模块 (`spacy_qa.py`)

在 `KGQA` 目录下创建一个新文件 `spacy_qa.py`，用于封装所有与 `spaCy` 相关的处理逻辑。这将保持代码的整洁性。

**文件路径**: `KGQA/spacy_qa.py`

**代码内容**:
```python
import spacy

# 加载预训练的中文模型
# disable=["parser", "attribute_ruler"] 可以禁用不需要的组件，提高加载和处理速度
nlp = spacy.load("zh_core_web_sm", disable=["parser", "attribute_ruler"])

# 定义一个关系关键词列表，用于从问题中识别关系
# 这个列表可以根据需要进行扩充
RELATIONSHIP_KEYWORDS = [
    "父亲", "母亲", "儿子", "女儿", "丈夫", "妻子", "哥哥", "弟弟", 
    "姐姐", "妹妹", "爷爷", "奶奶", "外祖母", "朋友", "老师", "丫环", "妾"
]

def extract_entity_and_relation(question: str):
    """
    使用 spaCy 从问题中提取人物实体和关系关键词。
    
    Args:
        question: 用户输入的自然语言问题，例如 "贾宝玉的父亲是谁？"

    Returns:
        一个包含实体和关系的列表，例如 ['贾宝玉', '父亲']。
        如果找不到，则返回 None。
    """
    person = None
    relation = None

    # 使用 spaCy 处理问题文本
    doc = nlp(question)

    # 1. 提取人物实体 (Named Entity Recognition)
    # 遍历识别出的实体，找到第一个被标记为"人名"的实体
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person = ent.text
            break # 找到第一个人名后就停止

    # 2. 提取关系关键词
    # 遍历问题中的每一个词，看它是否在我们的关键词列表中
    for token in doc:
        if token.text in RELATIONSHIP_KEYWORDS:
            relation = token.text
            break # 找到第一个关系后就停止
    
    # 如果成功找到了人物和关系，则返回一个列表，以兼容旧的图谱查询函数
    if person and relation:
        # 返回的格式与旧的 get_target_array 函数保持一致
        return [person, relation, "n"] # 添加一个补位元素"n"，兼容旧函数长度要求
    
    return None

```

### 第三步：修改主应用 `app.py`

现在，我们需要修改 `app.py`，让它调用我们新的 `spacy_qa.py` 模块，而不是已经废弃的 `ltp.py`。

**修改内容**:

1.  **替换导入语句**：
    将 `from KGQA.ltp import get_target_array` 替换为 `from KGQA.spacy_qa import extract_entity_and_relation`。

2.  **修改 `/KGQA_answer` 路由**：
    调用新的 `extract_entity_and_relation` 函数，并处理无法解析问题时的逻辑。

**修改后的 `app.py` 核心代码**:
```python
# ... 其他 flask 导入 ...
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile
# 1. 替换为新的模块导入
from KGQA.spacy_qa import extract_entity_and_relation

app = Flask(__name__)

# ... 其他路由保持不变 ...

@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name', '') # 获取问题

    # 2. 调用新的处理函数
    extracted_info = extract_entity_and_relation(question)

    # 如果成功提取到信息
    if extracted_info:
        try:
            # 调用图数据库查询函数，获取答案
            json_data = get_KGQA_answer(extracted_info)
            return jsonify(json_data)
        except Exception as e:
            # 如果查询出错，返回通用错误信息
            return jsonify([{"data": [], "links": []}, f"<p>查询出错: {e}</p>", ""])
    
    # 如果无法从问题中提取实体和关系
    else:
        # 返回友好的提示信息
        error_msg = "<p>抱歉，无法准确解析您的问题。</p><p>请尝试提问，如："贾宝玉的父亲是谁？"</p>"
        empty_data = {"data": [], "links": []}
        return jsonify([empty_data, error_msg, ""])

# ... 其他代码 ...

if __name__ == '__main__':
    app.debug = True
    app.run()
```

## 4. 总结

通过以上三个步骤，我们就可以实现：

1.  **移除对 `pyltp` 的依赖**：彻底解决安装和环境配置的难题。
2.  **引入 `spaCy`**：使用更现代、更易于维护的NLP工具链。
3.  **无缝集成**：新的 `spacy_qa.py` 模块的输出与旧系统兼容，最大限度地减少了对 `app.py` 和数据库查询代码的改动。
4.  **功能保留**：核心的"实体+关系"问答功能得以保留和实现，保证了项目的完整性。

这个方案具有很高的可操作性，你可以按照步骤轻松完成改造。 