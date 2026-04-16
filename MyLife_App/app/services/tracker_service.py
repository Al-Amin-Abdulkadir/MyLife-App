# Tracker services are instantiated per-request in routes/tracker.py
# using db: Session = Depends(get_db) — no module-level instances needed.
