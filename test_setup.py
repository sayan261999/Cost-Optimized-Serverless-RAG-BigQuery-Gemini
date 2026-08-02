from google.cloud import bigquery
from langchain_google_genai import ChatGoogleGenerativeAI

try :
    # test BQ connection
    bq_client = bigquery.Client()
    print(f"BigQuery client initialized successfully.Active project : {bq_client.project}")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",project=bq_client.project,location="us-central1")
    response = llm.invoke("Hello, how are you?")
    print(f"Response from LLM: {response.content}")
    print("enviroment is configured correctly for Google Vertex AI and BigQuery.")
except Exception as e:
    print(f"Error occurred: {e}")