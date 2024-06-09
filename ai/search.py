import http.client
import json
import os


def search_cv(query: str):
    token = os.getenv("GCLOUD_TOKEN")
    conn = http.client.HTTPSConnection("discoveryengine.googleapis.com")
    payload = json.dumps(
        {
            "query": query,
            "pageSize": 1,
            "queryExpansionSpec": {"condition": "AUTO"},
            "spellCorrectionSpec": {"mode": "AUTO"},
            "contentSearchSpec": {
                "summarySpec": {
                    "summaryResultCount": 3,
                    "modelPromptSpec": {
                        "preamble": "Bạn là thành viên của team HR, vui tính và hài hước, luôn mang lại tiếng cười cho mọi người hỏi. Thân thiện với mọi câu phản hồi, lịch sự và vui tươi. Hãy trả lời các câu hỏi và yêu cầu bằng Tiếng Việt. Trả lời chính xác dựa trên dữ liệu, không chế tác và ngắn gọn trọng tâm. Trả lời gói gọn trong 200 từ."
                    },
                    "modelSpec": {"version": "gemini-1.0-pro-002/answer_gen/v1"},
                    "ignoreAdversarialQuery": True,
                    "includeCitations": True,
                },
                "snippetSpec": {"returnSnippet": True},
                "extractiveContentSpec": {"maxExtractiveAnswerCount": 1},
            },
        }
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    conn.request(
        "POST",
        "/v1alpha/projects/1030547508006/locations/global/collections/default_collection/dataStores/hrpolicy_1716864229444/servingConfigs/default_search:search",
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    plain_text = json.loads(data)
    return plain_text
