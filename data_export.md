### Visualization Script & Data Usage
This section details how the `export_calls_csv.py` script extracts call data from MongoDB and prepares it for Tableau-based visualizations.

### Key Steps in Data Export & Visualization

**1. Connect & Retrieve**  
The script begins by connecting to the MongoDB `calls` collection using `pymongo.MongoClient`. It retrieves all call records using `coll.find()`, storing them in a Python list. This raw data serves as the foundation for downstream transformation and analysis.

**2. DataFrame Conversion**  
The retrieved documents are converted into a `pandas.DataFrame`, which helps translate MongoDB’s BSON types into native Python equivalents—essentially turning structured dictionaries into well-defined rows. This format streamlines further data processing.

**3. Type Normalization**  
To make the data readable and compatible with export tools, the script normalizes key fields:
- Converts MongoDB `ObjectId` instances into strings.
- Transforms `start_time` and `end_time` fields from datetime objects into human-friendly formats.
This step ensures that the final CSV is clean, consistent, and easy for external tools (like Tableau) to interpret.

**4. CSV Export**  
The cleaned DataFrame is exported using `df.to_csv(OUTPUT_FILE, index=False)`, creating `calls.csv` as a static file. This becomes the single source of truth for Tableau, eliminating the need for complex database connections and allowing quick refreshes when new data is generated.

### Tableau Integration
Once the CSV is ready, Tableau Desktop loads it as a flat-file data source. From here, the visualization workflow follows two key stages:

**Sheet Creation:**  
  Five analytical sheets are built, each addressing a specific facet of the data:
  - *Calls by Type* – categorizes different types of calls.
  - *Calls by Status* – tracks outcomes like completed, failed, or missed.
  - *Daily Calls* – visualizes call volume trends across dates.
  - *Calls by Weekday* – compares call traffic across weekdays.
  - *Duration Histogram* – shows how long calls typically last.

**Dashboard Assembly:**  
  These sheets are brought together into an interactive dashboard. Users can apply filters and trigger cross-sheet highlighting to explore trends and patterns with ease.
