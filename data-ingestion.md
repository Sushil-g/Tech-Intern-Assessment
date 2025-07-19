### Data Ingestion: Workflow & Details

This section outlines how the `calls_data_ingest.py` script transforms generated call records into queryable MongoDB documents, setting the stage for CSV export and Tableau visualization.

### Configuration & Initialization

The script begins by loading essential environment variables like `MONGO_URI`, `DB_NAME`, `COLLECTION_NAME`, and `NUM_CALLS`. These allow for flexible configuration, whether you're working locally or connecting to a remote MongoDB instance.
Using these parameters, the script initializes a `MongoClient`, establishing a connection to the designated database and collection.

### Synthetic Data Generation

To simulate realistic call records, the script relies on the `Faker` library alongside standard Python modules such as `uuid`, `random`, and `datetime`.
Each record includes key fields:
- `call_id`: a unique identifier
- `caller` and `callee`: generated phone numbers
- `start_time` and `end_time`: timestamps for the call
- `duration_sec`: call length in seconds (null for missed calls)
- `status`: indicates success, failure, or missed
- `cost_usd`: generated cost of the call
  
### Document Preparation
Each call record is assembled as a Python dictionary, closely matching MongoDB’s native document structure. Conditional logic is used to manage optional fields—such as excluding `duration_sec` if the call was missed—keeping the schema flexible without sacrificing clarity.

### Batch Insertion
Once all records are generated, they’re collected into a list and inserted using `insert_many()` in a single operation. This bulk insert approach minimizes network traffic and significantly improves ingestion speed.

### Error Handling & Retry Logic
To ensure robustness, the script wraps the insertion logic in a `try/except` block. This catches potential issues such as connectivity errors or duplicate key conflicts.
When a failure occurs, a retry mechanism can pause the operation and attempt reinsertion up to a configurable limit—making the process resilient under varying conditions.

### Index Creation (Optional)
For optimized querying, indexes can be created on frequently accessed fields like `start_time`, `status`, and `call_id`. While not mandatory, the script can be extended to automatically call `collection.create_index()` after ingestion, enhancing performance for downstream analytics.

### Data Export for CSV
Once the documents are stored, the dataset can be exported using either the `mongoexport` command or a simple Python-based cursor iteration. The resulting file (`calls.csv`) preserves the key structure needed for visualization, including fields like `call_id`, `start_time`, and `duration_sec`.

### Downstream Usage in Tableau
Tableau connects to `calls.csv` as a static data source and powers five analytical worksheets plus a consolidated dashboard. Analysts can refresh the CSV and reload the workbook anytime to update the visualizations with the latest call data.

Together, these steps form a seamless pipeline: generated Python records become structured MongoDB documents, which then transform into a CSV tailored for rich, interactive Tableau insights.
