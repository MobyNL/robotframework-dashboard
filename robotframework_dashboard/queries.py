CREATE_RUNS = """ CREATE TABLE IF NOT EXISTS runs ("run_start" TEXT, "full_name" TEXT, "name" TEXT, "total" INTEGER, "passed" INTEGER, "failed" INTEGER, "skipped" INTEGER, "elapsed_s" TEXT, "start_time" TEXT, tags TEXT, unique(run_start, full_name)); """
CREATE_SUITES = """ CREATE TABLE IF NOT EXISTS suites ("run_start" TEXT, "full_name" TEXT, "name" TEXT, "total" INTEGER, "passed" INTEGER, "failed" INTEGER, "skipped" INTEGER, "elapsed_s" TEXT, "start_time" TEXT, unique(run_start, full_name)); """
CREATE_TESTS = """ CREATE TABLE IF NOT EXISTS tests ("run_start" TEXT, "full_name" TEXT, "name" TEXT, "passed" INTEGER, "failed" INTEGER, "skipped" INTEGER, "elapsed_s" TEXT, "start_time" TEXT, "tags" TEXT); """
CREATE_KEYWORDS = """ CREATE TABLE IF NOT EXISTS keywords ("run_start" TEXT, "name" TEXT, "passed" INTEGER, "failed" INTEGER, "skipped" INTEGER, "times_run" TEXT, "total_time_s" TEXT, "average_time_s" TEXT, "min_time_s" TEXT, "max_time_s" TEXT); """

INSERT_INTO_RUNS = """ INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?) """
INSERT_INTO_SUITES = """ INSERT INTO suites VALUES (?,?,?,?,?,?,?,?,?) """
INSERT_INTO_TESTS = """ INSERT INTO tests VALUES (?,?,?,?,?,?,?,?,?) """
INSERT_INTO_KEYWORDS = """ INSERT INTO keywords VALUES (?,?,?,?,?,?,?,?,?,?) """

SELECT_FROM_RUNS = """ SELECT * FROM runs """
SELECT_NAME_START_FROM_RUNS = """ SELECT name, run_start FROM runs """
SELECT_FROM_SUITES = """ SELECT * FROM suites """
SELECT_FROM_TESTS = """ SELECT * FROM tests """
SELECT_FROM_KEYWORDS = """ SELECT * FROM keywords """

DELETE_FROM_RUNS = """ DELETE FROM runs WHERE run_start="{run_start}" """
DELETE_FROM_SUITES = """ DELETE FROM suites WHERE run_start="{run_start}" """
DELETE_FROM_TESTS = """ DELETE FROM tests WHERE run_start="{run_start}" """
DELETE_FROM_KEYWORDS = """ DELETE FROM keywords WHERE run_start="{run_start}" """
