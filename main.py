from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from database import get_db_connection, init_db, read_annual_data_from_db
from services import fetch_alpha_vantage_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/symbols/{symbol}/annual/{year}")

def get_annual_data(symbol: str, year: str):
    conn = get_db_connection()
    # Check availability of data within the local database
    rows = read_annual_data_from_db(symbol, year, conn)

    # Fetch from external API if data is not available locally
    if not rows:
        try:
            external_data = fetch_alpha_vantage_data(symbol)
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        # Filter for the requested year and insert into local database
        for date, metrics in external_data.items():
            if date.startswith(year):
                conn.execute(
                    "INSERT OR IGNORE INTO monthly_data VALUES (?, ?, ?, ?, ?)",
                    (symbol, date, metrics['2. high'], metrics['3. low'], metrics['5. volume'])
            )
        conn.commit()

        # Query back from local database after insertion
        rows = read_annual_data_from_db(symbol, year, conn)

    if not rows:
        raise HTTPException(status_code=404, detail="Data not found")

    # Aggregate to get max high, min low, and sum of volume
    res = conn.execute('''
        SELECT MAX(high) as high, MIN(low) as low, SUM(volume) as volume 
        FROM monthly_data 
        WHERE symbol = ? AND date LIKE ?
    ''', (symbol, f"{year}%")).fetchone()

    conn.close()

    return {
        "high": f"{res['high']:.4f}",
        "low": f"{res['low']:.4f}",
        "volume": str(res['volume'])
    }