from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "course-registration-demo-key"

students = []
courses = [
    {"id": 1, "name": "Python Programming"},
    {"id": 2, "name": "Web Development"},
    {"id": 3, "name": "Machine Learning"}
]
enrollments = []
next_student_id = 1


@app.route("/")
def home():
    return render_template("index.html", courses=courses)


@app.route("/register", methods=["GET", "POST"])
def register():
    global next_student_id

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()

        if not name or not roll_no:
            flash("Please enter all student details.")
        elif any(s["roll_no"] == roll_no for s in students):
            flash("Roll number already registered.")
        else:
            students.append({
                "id": next_student_id,
                "name": name,
                "roll_no": roll_no
            })
            next_student_id += 1
            flash("Student registered successfully.")
            return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/enroll", methods=["GET", "POST"])
def enroll():
    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        course_id = request.form.get("course_id", "")

        student = next(
            (s for s in students if s["roll_no"] == roll_no), None
        )
        course = next(
            (c for c in courses if str(c["id"]) == course_id), None
        )

        if not student:
            flash("Please register the student first.")
        elif not course:
            flash("Please select a valid course.")
        elif any(
            e["roll_no"] == roll_no and e["course_id"] == course["id"]
            for e in enrollments
        ):
            flash("Student is already enrolled in this course.")
        else:
            enrollments.append({
                "roll_no": roll_no,
                "student_name": student["name"],
                "course_id": course["id"],
                "course_name": course["name"]
            })
            flash("Course enrollment successful.")
            return redirect(url_for("home"))

    return render_template("courses.html", courses=courses)


@app.route("/enrollments")
def view_enrollments():
    return render_template(
        "courses.html",
        courses=courses,
        enrollments=enrollments,
        view_only=True
    )


if __name__ == "__main__":
    app.run(debug=True)