import sqlite3

conn = sqlite3.connect("candidates.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    college_name TEXT,
    round1 REAL,
    round2 REAL,
    round3 REAL,
    technical REAL,
    total REAL,
    result TEXT,
    rank INTEGER)
""")

conn.commit()

def validate_length(value, max_length, field_name):
    if len(value) > max_length:
        print(f"{field_name} exceeds max length of {max_length}")
        exit()

def get_marks(prompt, min_val, max_val):
    try:
        val = float(input(prompt))
        if not (min_val <= val <= max_val):
            print(f"Marks must be between {min_val} and {max_val}")
            exit()
        return val
    except:
        print("Inavlid numeric input")
        exit()

student_name = input("Enter Student name: ")
validate_length(student_name, 30, "Student Name")

college_name = input("Enter College name: ")
validate_length(college_name, 50, "College Name")

round1 = get_marks("Enter Round 1 Marks (0-10): ", 0, 10)
round2 = get_marks("Enter Round 2 Marks (0-10): ", 0, 10)
round3 = get_marks("Enter Round 3 Marks (0-10): ", 0, 10)
technical = get_marks("Enter Technical Round Marks (0-20): ", 0, 20)

total = round1 + round2 + round3 + technical

result = "Selected" if total >= 35 else "Rejected"

cursor.execute("""
INSERT INTO candidates
(student_name, college_name, round1, round2, round3, technical, total, result)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (student_name, college_name, round1, round2, round3, technical, total, result))

conn.commit()

cursor.execute("SELECT id, total FROM candidates ORDER BY total DESC")
rows = cursor.fetchall()

rank = 1
previous_total = None

for row in rows:
    candidate_id = row[0]
    current_total = row[1]

    if previous_total is not None and current_total < previous_total:
        rank += 1
    
    cursor.execute("UPDATE candidates SET rank=? WHERE id=?", (rank, candidate_id))

    previous_total = current_total

conn.commit()

print("\n-----Candidate Ranking-----")

cursor.execute("""
SELECT student_name, college_name, total, result, rank
FROM candidates
ORDER BY rank
""")

for candidate in cursor.fetchall():
    print(candidate)


conn.close()