from google.cloud import bigquery
import pdfplumber
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
)
import vertexai.preview.generative_models as generative_models
import json


project_id = "testgemini-410010"
table_id = "testgemini-410010.Tera.Candidates"

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

textsi_1 = """Bạn là nhân viên thuộc team Nhân sự và nhận rất nhiều Cv, hãy thực hiện lưu trữ các dữ liệu CV nhận được bằng cách thu thâp thông tin và điền thành bảng gồm 3 columns là Name, Position, Phone, Email, Experiences, Skill, không đánh giá dữ liệu
Vui lòng trả về câu trả lời ở dạng JSON format. Ví dụ là:
{
  "offset": 1,
  "Name": "HO THI MY DUNG",
  "Phone": "0934843577",
  "Email": "dungho83.k43@gmail.com",
  "Experiences": [
    "YeaH1 Group: 09/2022 - Present",
    "OCB-Orient Commercial Joint Stock Bank: 04/2021 -07/2022",
    "GCOMM Insight & Growth: 07/2020 -09/2020"
  ],
  "Skills": [
    "Analytical Skills",
    "Visualization",
    "Problem-Solving",
    "BigQuery",
    "Data Studio",
    "Dbt",
    "Google Analytics",
    "CleverTap",
    "Google Colab",
    "R",
    "SQL Server"
  ]
}"""


def read_content(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            print(text)
    return text


def insert_data(data):
    client = bigquery.Client(project=project_id)
    schema = [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("Name", "STRING"),
        bigquery.SchemaField("Phone", "STRING"),
        bigquery.SchemaField("Email", "STRING"),
        bigquery.SchemaField("Experiences", "STRING", mode="REPEATED"),
        bigquery.SchemaField("Skills", "STRING", mode="REPEATED"),
    ]
    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
    except:
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table)  # Make an API request.

    table = client.get_table(table_id)
    # Insert data
    print("data to insert")
    print(data)
    rows_to_insert = [
        {
            "id": data["Phone"],
            "Name": data["Name"],
            "Phone": data["Phone"],
            "Email": data["Email"],
            "Experiences": data["Experiences"],
            "Skills": data["Skills"],
        }
    ]
    errors = client.insert_rows_json(table, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def generate(content):
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-pro-preview-0409", system_instruction=[textsi_1]
    )
    responses = model.generate_content(
        [content],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    result = ""
    for response in responses:
        print(response.text)
        result = result + response.text

    return result


def parseMessageToJSON(message):
    message = message.replace("```json", "")
    message = message.replace("```", "")
    return message


def upload_file(file):
    content = read_content(file)
    record = parseMessageToJSON(generate(content))
    json_data = json.loads(record)
    insert_data(json_data)
    return json_data
