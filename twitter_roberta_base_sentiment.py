# 请保存函数名为 main，输入输出均为 dict；最终结果会以 json 字符串方式返回，请勿直接返回不支持 json.dumps 的对象
import requests

def main(params: dict) -> dict:
    # 从输入参数中提取用户查询内容
    user_input = params.get("input", "").strip()
    
    if not user_input:
        return {"result": {"error": "Missing 'input' in input parameters"}}

    try:
        # 发送请求到 FastAPI 服务
        response = requests.post(
            "http://124.223.109.228:8000/predict",
            headers={"Content-Type": "application/json"},
            json={"text": user_input},
            timeout=30
        )
        
        # 检查 HTTP 状态码
        if response.status_code != 200:
            return {
                "result": {
                    "error": f"Request failed with status {response.status_code}",
                    "details": response.text
                }
            }

        # 解析返回结果
        result = response.json()

    except requests.exceptions.Timeout:
        return {"result": {"error": "Request timed out"}}
    except requests.exceptions.ConnectionError:
        return {"result": {"error": "Failed to connect to the model server. Is it running?"}}
    except requests.exceptions.RequestException as e:
        return {"result": {"error": f"Request failed: {str(e)}"}}
    except ValueError:
        return {"result": {"error": "Invalid JSON response", "raw_response": response.text}}

    # 正常返回结果
    return {"result": result}