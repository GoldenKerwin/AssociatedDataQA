# 《红楼梦》人物关系知识图谱与智能问答系统

![红楼梦知识图谱](static/images/bg.jpg)

## 项目简介

本项目基于知识图谱技术，构建了《红楼梦》小说中人物关系的可视化展示和智能问答系统。通过整合Neo4j图数据库、自然语言处理和Web前端技术，实现了对复杂人物关系的直观展示和智能查询功能。

主要特点：
- 基于Neo4j图数据库构建人物关系知识图谱
- 使用自然语言处理技术进行问句解析
- 交互式关系图可视化展示
- 人物详细资料和图片显示
- 支持自然语言问答查询

## 在线体验

访问以下地址体验系统功能：
- 项目主页: http://localhost:5000/
- 人物关系检索: http://localhost:5000/search
- 关系全貌: http://localhost:5000/get_all_relation
- 智能问答: http://localhost:5000/KGQA

## 技术架构

![架构图](图片%201.png)

### 核心组件

1. **知识图谱层**
   - Neo4j图数据库存储人物实体与关系
   - 人物属性、图片等信息的结构化存储

2. **数据处理层**
   - 人物实体和关系数据爬取与处理
   - 知识图谱构建与查询接口

3. **自然语言处理层**
   - 基于SpaCy的中文分词和实体识别
   - 问句解析与查询意图转换

4. **Web应用层**
   - Flask后端提供API接口
   - 基于ECharts的关系图可视化
   - 响应式Web前端界面

## 功能介绍

### 1. 主页
展示系统概览，提供各功能模块的入口。

### 2. 人物关系检索
输入人物名称，查看与该人物直接相关的所有关系，以关系图形式展示。

### 3. 关系全貌
展示整个《红楼梦》知识图谱中的所有人物关系，可交互缩放、拖拽。

### 4. 智能问答
通过自然语言提问，查询人物关系，例如：
- "贾宝玉的父亲是谁？"
- "林黛玉的母亲是谁？"
- "王熙凤的丈夫是谁？"

系统会解析问题，查询知识图谱，并以关系图、文字说明和人物图片形式展示答案。

## 安装部署

### 环境要求
- Python 3.6+
- Neo4j 4.0+
- 现代浏览器（Chrome、Firefox、Edge等）

### 安装步骤

1. **克隆代码**
   ```bash
   git clone https://github.com/yourusername/KGQA_HLM.git
   cd KGQA_HLM
   ```

2. **安装依赖**
   ```bash
   pip install -r requirement.txt
   python -m spacy download zh_core_web_sm
   ```

3. **配置Neo4j**
   - 安装并启动Neo4j数据库
   - 修改 `neo_db/config.py` 中的连接配置：
     ```python
     graph = Graph(
         uri="bolt://localhost:7687",
         auth=("neo4j", "your_password")
     )
     ```

4. **构建知识图谱**
   ```bash
   cd neo_db
   python creat_graph.py
   cd ..
   ```

5. **启动应用**
   ```bash
   python app.py
   ```

6. **访问系统**
   打开浏览器，访问 http://localhost:5000/

## 使用指南

### 人物关系检索
1. 点击导航栏的"人物关系检索"
2. 在搜索框中输入人物名称（如"贾宝玉"）
3. 点击搜索按钮，查看关系图
4. 可点击图中节点，查看详细信息

### 智能问答
1. 点击导航栏的"智能问答"
2. 在输入框中输入问题（如"贾宝玉的父亲是谁？"）
3. 点击搜索按钮，查看结果
4. 关系图会展示相关人物关系，右侧显示人物信息和图片

## 项目结构

```
KGQA_HLM/
├── app.py                  # Flask应用主程序
├── requirement.txt         # 项目依赖
├── README.md               # 项目说明文档
│
├── templates/              # 前端HTML模板
│   ├── index.html          # 主页
│   ├── search.html         # 人物关系检索页
│   ├── all_relation.html   # 关系全貌页
│   └── KGQA.html           # 智能问答页
│
├── static/                 # 静态资源
│   ├── css/                # CSS样式文件
│   ├── js/                 # JavaScript文件
│   ├── images/             # 图片资源
│   └── fonts/              # 字体资源
│
├── neo_db/                 # Neo4j知识图谱模块
│   ├── config.py           # 数据库连接配置
│   ├── creat_graph.py      # 知识图谱构建
│   └── query_graph.py      # 图谱查询功能
│
├── KGQA/                   # 问答系统模块
│   └── spacy_qa.py         # 基于SpaCy的问句处理
│
├── spider/                 # 数据爬取与处理
│   ├── images/             # 人物图片
│   ├── json/               # 人物资料JSON
│   ├── get_hlm_character.py # 人物数据爬取
│   └── show_profile.py     # 人物资料展示
│
└── raw_data/               # 原始数据
    └── relation.txt        # 人物关系数据
```

## 关键技术点

1. **知识图谱构建**
   - 人物与关系的三元组结构设计
   - Neo4j Cypher查询语言的使用

2. **自然语言处理**
   - 中文分词与命名实体识别
   - 问句意图识别与结构化转换

3. **交互式可视化**
   - ECharts图表库的力导向图配置
   - 动态数据加载与更新

4. **前后端交互**
   - AJAX异步数据请求
   - JSON数据格式处理

## 常见问题

1. **系统无法启动或显示错误**
   - 检查Neo4j数据库是否正常运行
   - 确认配置文件中的数据库连接信息是否正确
   - 查看控制台日志获取详细错误信息

2. **关系图不显示或显示不完整**
   - 检查浏览器控制台是否有JavaScript错误
   - 确认数据库中是否包含查询的人物数据
   - 尝试调整浏览器窗口大小或刷新页面

3. **问答系统无法识别某些问题**
   - 确保问题格式符合"人物+关系"模式
   - 检查问题中的人物名是否正确
   - 尝试使用系统支持的关系类型（如"父亲"、"母亲"、"丈夫"等）

## 扩展与改进

1. **添加更多人物和关系**
   - 可扩充 `raw_data/relation.txt`，添加更多人物关系数据
   - 运行 `neo_db/creat_graph.py` 更新知识图谱

2. **增强问答能力**
   - 修改 `KGQA/spacy_qa.py`，添加更复杂的问句处理逻辑
   - 支持多跳关系查询（如"贾宝玉的父亲的兄弟是谁？"）

3. **优化界面与用户体验**
   - 在 `templates/` 和 `static/` 中修改前端代码
   - 添加更多交互功能和视觉效果

## 参考资源

- [Neo4j官方文档](https://neo4j.com/docs/)
- [SpaCy中文模型](https://spacy.io/models/zh)
- [ECharts官方示例](https://echarts.apache.org/examples/zh/index.html)
- [Flask文档](https://flask.palletsprojects.com/)

## 鸣谢

感谢所有为本项目提供支持和帮助的人员。特别感谢以下开源项目：
- Neo4j图数据库
- SpaCy自然语言处理库
- ECharts可视化库
- Flask Web框架

