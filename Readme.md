pipeline clearly explained:

✅ Your Current Data Flow (Correct)
Step 1 — Collection Students scan the QR code → opens your Google Form → they submit ratings for Taste, Temperature, Quantity, Hygiene, Experience.

Step 2 — Export You go to Google Sheets (linked to the Form responses) → File → Download → CSV format.

Step 3 — Replace the file Rename the downloaded file to exactly Updated PVGCOET Mess Feedback.csv and paste/replace it inside your project folder (same location as Home.py).

Step 4 — Restart Streamlit Since your data is cached with @st.cache_data, you need to either:

Press C or click Clear cache in the Streamlit top-right menu, OR
Stop the terminal (Ctrl+C) and re-run streamlit run Home.py
Step 5 — Dashboard auto-updates All pages (Home, Statistical Data, Charts, AI Insights) read from the same CSV — so everything refreshes automatically with new data.

🔄 Pipeline Summary for Updating Data
New responses submitted via QR
        ↓
Google Form → Google Sheets (auto-synced)
        ↓
Download as CSV from Google Sheets
        ↓
Rename file → "Updated PVGCOET Mess Feedback.csv"
        ↓
Replace old file in project folder
        ↓
Clear Streamlit cache → Dashboard updates instantly