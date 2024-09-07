import json
import xml.etree.ElementTree as ET

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
   return "<p>Hello!</p>"

@app.post("/api/xml/data")
def post_xml_order():
   try:       
       root = ET.fromstring(request.data)
       if root.tag != 'student':
           return "неверный корневой тег", 400

       student = root.get('fio')
       if not student:
           return "friends не передано или передано с ошибкой", 400

       email_list = set()
       total_age = 0
       for p in root:
           if p.tag == 'friend':
               email_list.add(p.get('email'))
               total_age += int(p.get('age'))

           if p.tag == 'weight':
               if not p.text.endswith('кг'):
                   return 'weight передан некорректно', 400
           
               weight = float(p.text[:-2])               
       
       email_list = list(email_list)
       print(len(email_list))
       if len(email_list)<3:
        return 'укажите хотя бы пятерых друзей с разной почтой!', 400    
       xml = ET.Element("student", total=str(int(total_age)), friends=",".join(email_list), 
                        fio=student, weight=str(weight)+" кг")
       return ET.tostring(xml, encoding='unicode')
   except Exception as e:
       return str(e), 500


@app.post("/api/json/data")
def post_json_student():
   try:
       student = request.json.get("fio")
       if student is None:
           return "fio не передано", 400

       friends = request.json.get("friends")
       if friends is None or not isinstance(friends, list):
           return "friends не передано или передано с ошибкой", 400

       email_list = set()
       total_age = 0
       for p in friends:
           email_list.add(p.get('email'))
           total_age += p.get('age')

       if email_list is None:
           return "friends не передано или передано с ошибкой", 400

       if len(email_list)<3:
           return "требуется информация хотя бы о 3 друзьях", 400

       weight = request.json.get("weight")
       if weight is None:
           return "weight не передано или передано с ошибкой", 400

       result = json.dumps(dict(
           student=student,
           total=total_age,
           friends_emails=list(email_list)
       ))
       
       print(result)
       return result
   
   except Exception as e:
       return str(e), 500 


"""
- установить python
- создать вирутальное окружение `python -m venv venv`
- активировать `.\venv\Scripts\activate` и установить flask `pip install flask`
- запустить сервер `flask --app main run`
- открыть консоль разработчика и сформировать посылки json/xml
"""