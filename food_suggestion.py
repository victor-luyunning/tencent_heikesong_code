import requests

def main(params: dict) -> dict:
    mood = params.get("mood", "").strip()
    season = params.get("season", "").strip()

    if not mood:
        return {"result": {"error": "Missing 'mood' in input parameters"}}

    # 构造请求体
    request_data = {
        "action": "call",
        "tool": "recommend_by_mood_and_season",
        "params": {
            "mood": mood,
            "season": season if season else None
        }
    }

    try:
        response = requests.post(
            "http://124.223.109.228:9000/mcp",   # FastAPI MCP 入口
            headers={"Content-Type": "application/json"},
            json=request_data,
            timeout=30
        )

        if response.status_code != 200:
            return {
                "result": {
                    "error": f"Request failed with status {response.status_code}",
                    "details": response.text
                }
            }

        result = response.json()

    except requests.exceptions.Timeout:
        return {"result": {"error": "Request timed out"}}
    except requests.exceptions.ConnectionError:
        return {"result": {"error": "Failed to connect to the server. Is it running?"}}
    except requests.exceptions.RequestException as e:
        return {"result": {"error": f"Request failed: {str(e)}"}}
    except ValueError:
        return {"result": {"error": "Invalid JSON response", "raw_response": response.text}}

    return {"result": result}