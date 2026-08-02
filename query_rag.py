from google.cloud import bigquery
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_vertexai import ChatVertexAI
import traceback

def ask_question(question):
    try:
        print(f"\n user question: {question} \n")
        # Initialize BigQuery client
        bq_client = bigquery.Client()
        project_id = bq_client.project

        # initialize the exaxt same embeddings model used to embed users question
        print("embedding the user question...")
        embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",project=project_id,location="us-central1",vertexai=True)
        query_vector = embeddings_model.embed_query(question)

        # search bigquery using native vector search to find the most relevant chunks
        print("searching for relevant chunks in BigQuery...")
        table_id = f"{project_id}.rag_dataset.tcs_report_embeddings"

        # bigquery sql for semantic vector search
        query = f"""
        SELECT
            base.content,
            base.source_page,
            distance
        FROM VECTOR_SEARCH(
            TABLE `{table_id}`,
            'text_embedding',
            (SELECT @query_vector AS text_embedding),
            top_k => 3,
            distance_type => 'COSINE'
        )
        """

        # pass the vector securely as a parameter
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("query_vector", "FLOAT64", query_vector)
            ]
        )

        query_results = list(
            bq_client.query(
                query,
                job_config=job_config
            ).result()
        )

        print(f"\nRetrieved {len(query_results)} relevant chunks.\n")

        if not query_results:
            print("No relevant chunks found.")
            return

        # compile the retrieved chunks into a single text block
        retrieved_context = ""
        print("\n --- Top Retrieved chunks from BigQuery --- ")

        for i , row in enumerate(query_results):
            print("=" * 80)
            print(f"Chunk {i+1}")
            print(f"Distance : {row.distance:.4f}")
            print(row["content"][:300])
            retrieved_context += f"{row['content']}\n\n"

        #prompt Engineering: force gemini to answer the question based on the retrieved context
        print("\n --- Sending context and question to Gemini --- ")
        prompt = f"""
        you are a professional financial analyst for an enterprise company . 
        use only the following context to answer the question. 
        if the answer is not in the context, say "I don't have enough the information to answer that question."
        context from Financial Documents :
        {retrieved_context}
        user question : {question}
        """

        # call the gemini model to answer the question based on the retrieved context
        llm = ChatVertexAI(model="gemini-2.5-flash",project=project_id,location="us-central1")
        response = llm.invoke(prompt)

        print("\n===================================================================")
        print("Final Gemini Answer:")
        print("=====================================================================")
        print(response.content)
        print("=====================================================================")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    # you can change the question below to test with different queries
    user_question = "What is the company's strategy regarding enterprise infrastructure and AI?"
    ask_question(user_question)