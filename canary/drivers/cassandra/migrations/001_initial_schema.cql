CREATE TABLE monitor_jobs (
    date TIMESTAMP,
    path TEXT,
    job_count INT,
    jobs TEXT,
    PRIMARY KEY (path, date)
);
