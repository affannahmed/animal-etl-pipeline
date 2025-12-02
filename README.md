# Animal ETL Pipeline

ETL pipeline for a coding challenge. Fetches animal data from an API, transforms it, and sends it back.

## The Challenge

Build a pipeline that:
1. Fetches all animals from `/animals/v1/animals` (it's paginated)
2. Gets detailed info for each animal
3. Transforms two fields:
   - `friends`: from `"dog,cat,bird"` → `["dog", "cat", "bird"]`
   - `born_at`: to ISO8601 UTC timestamp
4. POSTs batches of 100 to `/animals/v1/home`

The API randomly throws errors (500, 502, 503, 504) and pauses for 5-15 seconds to simulate real-world issues.

## Setup
```bash
# Clone and setup
git clone <your-repo>
cd animal-etl-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the API (separate terminal)
docker run --rm -p 3123:3123 -ti lp-programming-challenge-1

# Run the pipeline
python main.py
```

## How It Works

**client.py** - Handles API calls with retry logic using `tenacity`. Retries up to 5 times with exponential backoff when the server acts up.

**transformation_logic.py** - Pure transformation functions. Splits the friends string and converts dates to ISO8601.

**loading_logic.py** - Batches animals into groups of 100 and POSTs them. Shows progress as it goes.

**main.py** -  Fetch → Transform → Load.

## Running It

Takes about 10-20 minutes to process all ~5,850 animals. You'll see it hit server errors occasionally - that's expected and the retry logic handles it.

# Expected output :
Starting Animal ETL Pipeline

==================================================
Fetching all animals
Fetched page 1/585 (10 animals)
Fetched page 2/585 (10 animals)

## Dependencies

- `requests` - HTTP
- `tenacity` - Retry logic

- `python-dateutil` - Date parsing
