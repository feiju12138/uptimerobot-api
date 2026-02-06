import os, json
from urllib import request, error
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def root():
    return 'ok'

@app.route('/api')
def api():
    try:
        # 读取环境变量 TOKEN
        token = os.getenv('TOKEN')
        if not token:
            return jsonify({"code": 400, "msg": "TOKEN 未配置"}), 400

        # 请求 UptimeRobot API
        url = "https://api.uptimerobot.com/v3/monitors"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        req = request.Request(url, headers=headers, method='GET')

        with request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('utf-8')
            json_data = json.loads(data)
            # 响应数据封装
            result = [{"url": item["url"], "status": item["status"]} for item in json_data["data"]]
            return jsonify(result)

    except error.HTTPError as e:
        return jsonify({"code": e.code, "msg": f"HTTP 错误：{e.reason}"}), e.code
    except error.URLError as e:
        return jsonify({"code": 500, "msg": f"网络错误：{str(e)}"}), 500
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务异常：{str(e)}"}), 500

# 这段代码仅本地运行生效，Vercel 环境不会执行，可保留/删除
if __name__ == '__main__':
    # 端口9000仅作用于本地，线上无效
    app.run(host='0.0.0.0', port=9000, debug=True)
