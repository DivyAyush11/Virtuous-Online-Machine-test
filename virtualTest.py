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
    if len(value) <= max_length:
        return True
    else:
        print(f"{field_name} must not exceed max length of {max_length}")
        return False

def get_marks(prompt, min_val, max_val):
    while True:
        try:
            val = float(input(prompt))
            if  min_val <= val <= max_val:
                return val
            else:
                print(f"Marks must be between {min_val} and {max_val}")
        except ValueError:
            print("Invalid numeric input. Please try again.")

student_name = input("Enter Student name: ")
validate_length(student_name, 30, "Student Name")

college_name = input("Enter College name: ")
validate_length(college_name, 50, "College Name")

round1 = get_marks("Enter Round 1 Marks (0-10): ", 0, 10)
round2 = get_marks("Enter Round 2 Marks (0-10): ", 0, 10)
round3 = get_marks("Enter Round 3 Marks (0-10): ", 0, 10)
technical = get_marks("Enter Technical Round Marks (0-20): ", 0, 20)

total = round1 + round2 + round3 + technical

# result = "Selected" if total >= 35 else "Rejected"
if ((round1 < 6.5 or round2 < 6.5 or round3 < 6.5 or technical < 13) and total < 35):
    result = "Rejected"
else:
    result = "Selected"

cursor.execute("""
INSERT INTO candidates
(student_name, college_name, round1, round2, round3, technical, total, result)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (student_name, college_name, round1, round2, round3, technical, total, result))

conn.commit()

cursor.execute("SELECT id, total FROM candidates ORDER BY total DESC")
rows = cursor.fetchall()

# rank = 1
previous_total = None

for index, row in enumerate(rows, start=1):
    candidate_id = row[0]
    current_total = row[1]

    if previous_total is None:
        rank = 1
    elif current_total < previous_total:
        rank = index
    
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