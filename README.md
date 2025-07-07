

# 基于知识图谱的《红楼梦》人物关系可视化及问答系统

## 项目简介

本项目旨在通过知识图谱技术，对《红楼梦》中的人物关系进行结构化建模、可视化展示，并实现基于知识图谱的智能问答。系统集成了数据爬取、知识图谱构建、自然语言处理、Web前端展示等模块，支持人物关系查询、全谱可视化、智能问答等功能。

---

## 目录结构与文件说明

```
KGQA_HLM/
│
├── app.py                    # Flask主程序入口，定义Web路由和接口
├── requirement.txt           # Python依赖库列表
├── README.md                 # 项目说明文档
│
├── templates/                # 前端HTML模板
│   ├── index.html            # 欢迎界面
│   ├── search.html           # 人物关系搜索页面
│   ├── all_relation.html     # 所有人物关系可视化页面
│   ├── KGQA.html             # 知识问答页面
│   └── ...                   # 其他模板文件
│
├── static/                   # 前端静态资源
│   ├── css/                  # 样式文件
│   ├── js/                   # 脚本文件
│   ├── images/               # 图片资源
│   ├── fonts/                # 字体资源
│   ├── data.json             # 前端可视化用数据
│   └── ...                   # 其他静态资源
│
├── raw_data/                 # 原始及处理后数据
│   └── relation.txt          # 处理后的人物关系三元组数据
│
├── neo_db/                   # 知识图谱数据库相关模块
│   ├── config.py             # Neo4j数据库连接配置
│   ├── creat_graph.py        # 知识图谱构建脚本
│   ├── query_graph.py        # 知识图谱查询与问答接口
│   └── __pycache__/          # Python缓存
│
├── KGQA/                     # 问答系统相关模块
│   ├── ltp.py                # LTP分词、词性标注、命名实体识别
│   └── __pycache__/          # Python缓存
│
├── spider/                   # 数据爬虫与资料处理
│   ├── get_hlm_character.py  # 爬取人物资料与图片
│   ├── get_character_array.py# 解析人物列表
│   ├── show_profile.py       # 人物资料展示接口
│   ├── images/               # 爬取的人物图片
│   ├── json/                 # 爬取的人物资料json
│   └── __pycache__/          # Python缓存
│
└── ...                       # 其他文件（如图片示例等）
```

---

## 各模块与文件详细说明

### 1. 主程序与Web接口

- **app.py**  
  Flask应用主入口，定义了各页面路由和后端API接口。主要功能包括：
  - 首页、搜索页、问答页、全谱可视化页的渲染
  - 提供人物资料、知识问答、关系查询等API接口
  - 通过调用 `neo_db`、`KGQA`、`spider` 等模块实现后端逻辑

### 2. 前端页面与静态资源

- **templates/**  
  存放所有HTML模板，配合Flask渲染。  
  - `index.html`：欢迎页  
  - `search.html`：输入人物名查询关系  
  - `all_relation.html`：全谱关系可视化  
  - `KGQA.html`：知识问答交互页

- **static/**  
  存放前端静态资源，包括CSS、JS、图片、字体等。  
  - `data.json`：部分可视化数据

### 3. 数据与知识图谱

- **raw_data/relation.txt**  
  结构化的人物关系三元组数据（如“贾演,贾代化,父亲,贾家宁国府,贾家宁国府”），为知识图谱构建和问答提供基础。

- **neo_db/**  
  - `config.py`：Neo4j数据库连接配置（需根据实际环境修改账号密码）
  - `creat_graph.py`：读取 `relation.txt`，自动构建Neo4j知识图谱
  - `query_graph.py`：提供知识图谱的查询、问答、人物资料API，供主程序调用

### 4. 问答系统

- **KGQA/ltp.py**  
  基于LTP（语言技术平台）实现分词、词性标注、命名实体识别等NLP功能，为自然语言问题转化为结构化查询提供支持。

### 5. 数据爬虫与资料处理

- **spider/get_hlm_character.py**  
  爬取百度百科等来源的人物资料和图片，生成json和图片文件。

- **spider/get_character_array.py**  
  解析 `relation.txt`，获取所有人物名列表，供爬虫和知识图谱构建使用。

- **spider/show_profile.py**  
  读取 `spider/json/data.json`，根据人物名返回详细资料HTML片段，供前端展示。

- **spider/json/data.json**  
  爬取后的人物详细资料，结构为“人物名: 属性字典”。

- **spider/images/**  
  爬取的人物图片资源。

---

## 各模块之间的关系

- **数据流**：  
  1. `raw_data/relation.txt` 提供基础三元组数据  
  2. `spider/get_character_array.py` 解析人物名，`spider/get_hlm_character.py` 爬取资料和图片，生成 `spider/json/data.json` 和图片
  3. `neo_db/creat_graph.py` 读取三元组，构建Neo4j知识图谱
  4. `neo_db/query_graph.py` 提供知识图谱查询、问答、资料API
  5. `KGQA/ltp.py` 负责自然语言处理，辅助问答
  6. `app.py` 作为主控，整合各模块，提供Web服务和API
  7. 前端页面通过AJAX等方式调用后端API，展示查询、问答和可视化结果

---

## 程序部署与启动流程

1. **安装依赖库**  
   在项目根目录下执行：
   ```
   pip install -r requirement.txt
   ```

2. **准备Neo4j数据库**  
   - 下载并安装 [Neo4j](https://neo4j.com/download/)，建议使用JDK8环境
   - 启动Neo4j服务 `neo4j console`
   - 修改 `neo_db/config.py`，设置正确的数据库地址、账号和密码

3. **构建知识图谱**  
   进入 `neo_db` 目录，执行：
   ```
   python creat_graph.py
   ```
   该脚本会自动读取 `raw_data/relation.txt`，在Neo4j中建立人物关系图谱

4. **准备模型**  
   - `python -m spacy download zh_core_web_sm`

5. **（可选）爬取人物资料**  
   - 若需更新人物资料和图片，可运行 `spider/get_hlm_character.py`
   - 该脚本会自动生成 `spider/json/data.json` 和图片资源

6. **启动Web服务**  
   在项目根目录下执行：
   ```
   python app.py
   ```
   默认启动在 `localhost:5000`，用浏览器访问即可体验系统

---

## 示例界面

- 欢迎页、主界面、全谱可视化、问答交互等页面，详见 `templates/` 目录和项目内图片示例。

---

如需进一步扩展或定制功能，请参考各模块源码及注释。欢迎交流与反馈！

---

如果你需要更详细的某一部分说明或有其他定制需求，请随时告知！