from neo_db.config import graph, CA_LIST, similar_words
from spider.show_profile import get_profile
import codecs
import os
import json
import base64

def query(name):
    data = graph.run(
        "match(p )-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
        Union all\
        match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name,name)
    )
    data = list(data)
    return get_json_data(data)

def get_json_data(data):
    # 创建适合ECharts图形显示的数据格式
    json_data = {'data': [], "links": []}
    d = []
    
    # 收集所有节点信息
    for i in data:
        d.append(i['p.Name']+"_"+i['p.cate'])
        d.append(i['n.Name']+"_"+i['n.cate'])
        d = list(set(d))
    
    # 创建节点ID映射
    name_dict = {}
    count = 0
    
    # 创建节点数组
    for j in d:
        j_array = j.split("_")
        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        # 添加额外的显示属性
        data_item['symbolSize'] = 60
        data_item['draggable'] = True
        json_data['data'].append(data_item)
    
    # 创建链接数组
    for i in data:
        link_item = {}
        link_item['source'] = name_dict[i['p.Name']]
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data

def get_KGQA_answer(array):
    data_array = []
    try:
        for i in range(len(array)-2):
            if i == 0:
                name = array[0]
            else:
                name = data_array[-1]['p.Name']
           
            data = graph.run(
                "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
                    similar_words[array[i+1]], similar_words[array[i+1]], name)
            )
       
            data = list(data)
            data_array.extend(data)
        
        if not data_array:
            # 如果没有找到数据，返回空结果
            return [{'data': [], 'links': []}, "<p>未找到相关信息</p>", ""]
        
        # 获取图片数据
        try:
            with open("./spider/images/"+"%s.jpg" % (str(data_array[-1]['p.Name'])), "rb") as image:
                base64_data = base64.b64encode(image.read())
                b = str(base64_data)
                img_data = b.split("'")[1]
        except Exception:
            img_data = ""
        
        # 返回结果
        return [get_json_data(data_array), get_profile(str(data_array[-1]['p.Name'])), img_data]
    
    except Exception as e:
        return [{'data': [], 'links': []}, f"<p>查询处理出错: {str(e)}</p>", ""]

def get_answer_profile(name):
    try:
        with open("./spider/images/"+"%s.jpg" % (str(name)), "rb") as image:
            base64_data = base64.b64encode(image.read())
            b = str(base64_data)
        return [get_profile(str(name)), b.split("'")[1]]
    except Exception as e:
        return [f"<p>获取信息失败: {str(e)}</p>", ""]