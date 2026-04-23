import os
import sqlite3
import logging
import csv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DB_FILE = os.path.join(OUTPUT_DIR, "transformed_posts.db")
CSV_FILE = os.path.join(OUTPUT_DIR, "analytics_posts.csv")
REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def connect_db():
    logging.info("Connecting to SQLite database")
    return sqlite3.connect(DB_FILE)


def create_raw_table(conn):
    logging.info("Creating raw posts table if not exists")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT
    );
    """

    conn.execute(create_table_query)
    conn.commit()


def load_sample_data(conn):
    logging.info("Checking if sample data needs to be loaded")

    count_query = "SELECT COUNT(*) FROM posts;"
    count = conn.execute(count_query).fetchone()[0]

    if count > 0:
        logging.info("Raw posts table already has data. Skipping sample insert.")
        return

    sample_data = [
        (1, 1, "sunt aut facere", "quia et suscipit suscipit recusandae consequuntur"),
        (2, 1, "qui est esse", "est rerum tempore vitae sequi sint nihil reprehenderit"),
        (3, 2, "ea molestias quasi exercitationem repellat qui ipsa sit aut", "et iusto sed quo iure voluptatem occaecati omnis"),
        (4, 2, "eum et est occaecati", "ullam et saepe reiciendis voluptatem adipisci"),
        (5, 3, "nesciunt quas odio", "repudiandae veniam quaerat sunt sed alias aut fugiat"),
        (6, 3, "dolorem eum magni eos aperiam quia", "ut aspernatur corporis harum nihil quis provident"),
        (7, 4, "magnam facilis autem", "dolore placeat quibusdam ea quo vitae"),
        (8, 4, "dolorem dolore est ipsam", "dignissimos aperiam dolorem qui eum"),
        (9, 5, "nesciunt iure omnis dolorem tempora et accusantium", "consectetur animi nesciunt iure dolore"),
        (10, 5, "optio molestias id quia eum", "quo et expedita modi cum officia vel magni")
    ]

    insert_query = """
    INSERT INTO posts (id, user_id, title, body)
    VALUES (?, ?, ?, ?);
    """

    conn.executemany(insert_query, sample_data)
    conn.commit()
    logging.info("Sample raw data inserted into posts table")


def run_data_quality_checks(conn):
    logging.info("Running data quality checks on raw posts table")

    total_records = conn.execute("SELECT COUNT(*) FROM posts;").fetchone()[0]
    null_titles = conn.execute("SELECT COUNT(*) FROM posts WHERE title IS NULL OR TRIM(title) = '';").fetchone()[0]
    null_bodies = conn.execute("SELECT COUNT(*) FROM posts WHERE body IS NULL OR TRIM(body) = '';").fetchone()[0]

    duplicate_ids_query = """
    SELECT COUNT(*) FROM (
        SELECT id
        FROM posts
        GROUP BY id
        HAVING COUNT(*) > 1
    ) AS duplicate_check;
    """
    duplicate_ids = conn.execute(duplicate_ids_query).fetchone()[0]

    report_lines = [
        "DAY 8 DATA QUALITY REPORT",
        "==========================",
        f"Total raw records: {total_records}",
        f"Null or empty titles: {null_titles}",
        f"Null or empty bodies: {null_bodies}",
        f"Duplicate ids: {duplicate_ids}"
    ]

    with open(REPORT_FILE, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines))

    logging.info("Data quality report created")


def create_transformed_table(conn):
    logging.info("Dropping existing analytics_posts table if exists")
    conn.execute("DROP TABLE IF EXISTS analytics_posts;")

    logging.info("Creating transformed analytics_posts table using SQL")

    transform_query = """
    CREATE TABLE analytics_posts AS
    SELECT
        id,
        user_id,
        title,
        body,
        LENGTH(title) AS title_length,
        LENGTH(body) AS body_length,
        CASE
            WHEN LENGTH(title) < 20 THEN 'short'
            WHEN LENGTH(title) BETWEEN 20 AND 50 THEN 'medium'
            ELSE 'long'
        END AS title_category
    FROM posts
    WHERE title IS NOT NULL
      AND TRIM(title) != ''
      AND body IS NOT NULL
      AND TRIM(body) != '';
    """

    conn.execute(transform_query)
    conn.commit()
    logging.info("Transformed analytics_posts table created successfully")


def export_to_csv(conn):
    logging.info("Exporting analytics_posts table to CSV")

    select_query = """
    SELECT id, user_id, title, body, title_length, body_length, title_category
    FROM analytics_posts
    ORDER BY id;
    """

    rows = conn.execute(select_query).fetchall()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "id",
            "user_id",
            "title",
            "body",
            "title_length",
            "body_length",
            "title_category"
        ])
        writer.writerows(rows)

    logging.info("CSV export completed")


def show_summary(conn):
    logging.info("Generating SQL summary metrics")

    summary_query = """
    SELECT title_category, COUNT(*) AS record_count
    FROM analytics_posts
    GROUP BY title_category
    ORDER BY record_count DESC;
    """

    results = conn.execute(summary_query).fetchall()

    print("\nTransformed Data Summary")
    print("========================")
    for row in results:
        print(f"Category: {row[0]} | Records: {row[1]}")


def main():
    setup_logging()
    logging.info("Day 8 pipeline started")

    conn = connect_db()

    try:
        create_raw_table(conn)
        load_sample_data(conn)
        run_data_quality_checks(conn)
        create_transformed_table(conn)
        export_to_csv(conn)
        show_summary(conn)

        logging.info("Day 8 pipeline completed successfully")
        print("\nPipeline completed successfully.")
        print(f"Database created at: {DB_FILE}")
        print(f"CSV exported at: {CSV_FILE}")
        print(f"Report created at: {REPORT_FILE}")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")
        print(f"Pipeline failed: {error}")

    finally:
        conn.close()
        logging.info("Database connection closed")


if __name__ == "__main__":
    main()