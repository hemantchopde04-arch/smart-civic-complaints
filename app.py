from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

CORS(app)

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(UPLOAD_FOLDER)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "complaints.db"
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS complaints (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    title TEXT,

    description TEXT,

    area TEXT,

    category TEXT,

    ai_category TEXT,

    image TEXT,

    status TEXT,

    feedback TEXT

)

""")

conn.commit()

conn.close()

# =========================
# SEND OTP
# =========================

@app.route("/send-otp", methods=["POST"])
def send_otp():

    data = request.json

    phone = data.get("phone")

    return jsonify({

        "success": True,

        "message":
        f"OTP Sent Successfully to {phone}"

    })

# =========================
# SUBMIT COMPLAINT
# =========================

@app.route(
    "/submit-complaint",
    methods=["POST"]
)

def submit_complaint():

    name = request.form.get("name")

    title = request.form.get("title")

    description = request.form.get(
        "description"
    )

    area = request.form.get("area")

    category = request.form.get(
        "category"
    )

    ai_category = request.form.get(
        "ai_category"
    )

    image = request.files.get("image")

    filename = ""

    if image:

        filename = image.filename

        image.save(

            os.path.join(
                UPLOAD_FOLDER,
                filename
            )

        )

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO complaints
    (
        name,
        title,
        description,
        area,
        category,
        ai_category,
        image,
        status,
        feedback
    )

    VALUES (?,?,?,?,?,?,?,?,?)

    """,

    (
        name,
        title,
        description,
        area,
        category,
        ai_category,
        filename,
        "Pending",
        ""
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message":
        "Complaint Submitted Successfully ✅"

    })

# =========================
# GET COMPLAINTS
# =========================

@app.route("/get-complaints")
def get_complaints():

    conn = sqlite3.connect(
        "complaints.db"
    )

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM complaints

    """)

    rows = cursor.fetchall()

    complaints = []

    for row in rows:

        complaints.append({

            "id": row["id"],

            "name": row["name"],

            "title": row["title"],

            "description":
            row["description"],

            "area": row["area"],

            "category":
            row["category"],

            "ai_category":
            row["ai_category"],

            "image": row["image"],

            "status": row["status"],

            "feedback":
            row["feedback"]

        })

    conn.close()

    return jsonify(complaints)

# =========================
# UPDATE STATUS
# =========================

@app.route(
    "/update-status/<int:id>",
    methods=["POST"]
)

def update_status(id):

    data = request.json

    status = data.get("status")

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE complaints

    SET status=?

    WHERE id=?

    """,

    (
        status,
        id
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message":
        "Status Updated"

    })

# =========================
# SAVE FEEDBACK
# =========================

@app.route(
    "/submit-feedback",
    methods=["POST"]
)

def submit_feedback():

    data = request.json

    complaint_id = data.get("id")

    feedback = data.get("feedback")

    conn = sqlite3.connect(
        "complaints.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE complaints

    SET feedback=?

    WHERE id=?

    """,

    (
        feedback,
        complaint_id
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message":
        "Feedback Submitted Successfully"

    })

# =========================
# IMAGE ACCESS
# =========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    app.run(debug=True)