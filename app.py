from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query,get_KGQA_answer,get_answer_profile
from KGQA.spacy_qa import get_target_array
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index(name=None):
    return render_template('index.html', name = name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')
@app.route('/get_profile',methods=['GET','POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)

@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    extracted_info = get_target_array(str(question))
    
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
        error_msg = "<p>抱歉，无法准确解析您的问题。</p><p>请尝试提问，如：\"贾宝玉的父亲是谁？\"</p>"
        empty_data = {"data": [], "links": []}
        return jsonify([empty_data, error_msg, ""])
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data=query(str(name))
    return jsonify(json_data)

@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')

if __name__ == '__main__':
    app.debug=True
    app.run()
