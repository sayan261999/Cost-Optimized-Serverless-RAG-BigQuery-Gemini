import os
import pandas as pd
from  google.cloud import bigquery
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ingest_data import process_pdf

def create_and_store_embeddings():
    # get the chunks 
    pdf_path = os.path.join("C:\\Projects\\RAG_Project\\data", "TCS_annual-report-2025-2026.pdf")  # Replace with your PDF file path
    all_chunks = process_pdf(pdf_path)

    # we will slice the first 50 chunks for our prototype to run fast
    chunks_to_process = all_chunks[:50]  # Adjust the number of chunks as needed
    print(f"\n Transforming {len(chunks_to_process)} chunks into vector embeddings...")

    #2 initialize the Embeddings model using the 2026 text-embedding-004 model
    bq_client = bigquery.Client()
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",project=bq_client.project,location="us-central1",vertexai=True)

    #3 create the vectors 
    data_for_bq = []
    for i , chunk in enumerate(chunks_to_process):
        vector = embeddings_model.embed_query(chunk.page_content)

        # prepare the row for BQ
        data_for_bq.append({
            "chunk_id": f"chunk_{i}",
            "content": chunk.page_content, 
            "source_page": int(chunk.metadata.get("page", 0)),
            "text_embedding": vector
        })

        # print the progress for every 10 chunks processed
        if (i + 1) % 10 == 0:
            print(f"Embedded chunks {i + 1}/{len(chunks_to_process)}...")


    #4 save to BigQuery
    print("\n saving vectors to BigQuery...")
    df=pd.DataFrame(data_for_bq)

    # Define the BigQuery dataset and table 
    dataset_id = f"{bq_client.project}.rag_dataset"
    table_id = f"{dataset_id}.tcs_report_embeddings"

    # Create the dataset if it doesn't exist
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = bq_client.create_dataset(dataset, exists_ok=True)

    # load the DataFrame into BigQuery(write_truncate to overwrite the table if it already exists)
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Successfully uploaded {job.output_rows} rows(vectors) to BigQuery table: {table_id}")

if __name__ == "__main__":
    create_and_store_embeddings()

