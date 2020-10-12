-- Queries for creating database on local

CREATE TABLE calculations(
cal_id SERIAL PRIMARY KEY,
user_id INTEGER,
user_name VARCHAR(20),
num1 FLOAT
num2 FLOAT
operations VARCHAR(20),
signs CHAR,
answer FLOAT
)

SELECT * FROM calculations;

-- DELETE FROM calculations;