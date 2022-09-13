from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Students(db.Model):
    student_number = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String, nullable=False)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        student_number = request.form['student_number']
        name = request.form['name']
        credits = request.form['credits']
        degree = request.form['degree']

        new_student = Students(
            student_number=student_number, 
            name=name,
            credits=credits,
            degree=degree
        )

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your student'

    else:
        degrees = []
        degree = 'all'
        params = request.args
        students = Students.query.order_by(Students.student_number).all()
        
        for student in students:
            degrees.append(student.degree)

        print(degrees)

        res_degrees = [*set(degrees)]
        print(res_degrees)

        if params:
            if params['degree'] and params['degree'] != 'all':
                degree = params['degree']
                students = list(filter(lambda s: s.degree == degree, students))
                res_degrees = []
                res_degrees.append(degree)
                return render_template('home.html', students=students, degrees=res_degrees)

            elif params['degree'] == 'all':
                return render_template('home.html', students=students, degrees=res_degrees)

        return render_template('home.html', students=students, degrees=res_degrees)


@app.route('/delete/<int:student_number>')
def delete(student_number):
    student_to_delete = Students.query.get_or_404(student_number)

    print(student_to_delete)

    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that student'


@app.route('/update/<int:student_number>', methods=['GET', 'POST'])
def update(student_number):
    student = Students.query.get_or_404(student_number)

    if request.method == 'POST':
        student.name = request.form['name']
        student.credits = request.form['credits']
        student.degree = request.form['degree']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem with updating student'

    else:
        return render_template('update.html', student=student)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
