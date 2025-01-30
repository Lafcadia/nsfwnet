from flask import Flask, render_template_string, request, redirect, url_for
import json
import requests

app = Flask(__name__)

template_root = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='favicon.png') }}" />
    <title>鉴黄</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .form-container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .form-container input[type="file"] {
            margin-bottom: 10px;
        }
        .form-container input[type="submit"] {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
        .form-container input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="center">
        <div class="form-container">
            <form action="/submission" method="post" enctype="multipart/form-data">
                <input type="file" name="image" required>
                <input type="submit" value="上传">
            </form>
        </div>
    </div>
</body>
</html>
"""

# <form action="/submission" method="post" enctype="multipart/form-data">


template_result = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鉴黄结果</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .result-container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .result-container img {
            width: 100%;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="center">
        <div class="result-container">
            <div>
                <p>性感指数: {{sexy}}</p>
                <p>瑟琴指数: {{porn}}</p>
                <p>SFW指数: {{drawing}}</p>
                <p>变态指数: {{hentai}}</p>
                <p>测量偏差: {{neutral}}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(template_root)

@app.route('/submission', methods=['POST'])
def submission():
    image = request.files['image']
    c = requests.post("http://nsfw.chuishen.xyz:3000/classify", files={"image": image})
    print(c)
    c = c.content.decode()
    print(c)
    dic = json.loads(c)
    return render_template_string(template_result, **dic)

@app.route('/submit', methods=['POST'])
def submit():
    image = request.data
    print(image)
    c = requests.post("http://nsfw.chuishen.xyz:3000/classify", files={"image": image})
    print(c)
    c = c.content.decode()
    print(c)
    dic = json.loads(c)
    return dic, 200, {"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run()