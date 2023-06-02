#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
                        CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
                        Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'
        ),
        UniqueConstraint(
            'email',
            name='unique_email'
        ),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'
        )
    )
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"{self.email}," \
            + f"Grade {self.grade}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    # use our engine to configure a session class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="alberte.einstain@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    duncan_kipkemoi = Student(
        name="duncan kipkemoi",
        email="duncan.kipkemoi@zurich.edu",
        grade=8,
        birthday=datetime(
            year=2000,
            month=1,
            day=3
        ),
    )
    pkurui_sang = Student(
        name="pkurui sang",
        email="pkurui.sang@zurich.edu",
        grade=11,
        birthday=datetime(
            year=1998,
            month=10,
            day=23
        ),
    )
    # pkurui_sangwe = Student(
    #     name="pkurui sang",
    #     email="pkurui.sang@zurich.edu",
    #     grade=11,
    #     birthday=datetime(
    #         year=1998,
    #         month=10,
    #         day=23
    #     ),
    # )

    session.bulk_save_objects(
        [albert_einstein, duncan_kipkemoi, pkurui_sang])
    session.commit()
    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {duncan_kipkemoi.id}.")
    # print([student for student in students])
    students = session.query(Student).all()
    print(students)

    names = [name for name in session.query(Student.name)]
    print(names)
    emails = [email for email in session.query(Student.email)]
    print(emails)

    students_by_name = [student for student in session.query(
        Student.name
    ).order_by(
        Student.name
    )]
    print(students_by_name)

    student_by_grade = [student for student in session.query(
        Student.grade
    ).order_by(
        desc(Student.grade)
    )]

    print(student_by_grade)

    student_by_grade_desc = [student for student in session.query(
        Student.name, Student.grade
    ).order_by(
        desc(Student.grade)
    )]

    print(student_by_grade_desc)

    oldest_student = [student for student in session.query(
        Student.name, Student.birthday
    ).order_by(
        desc(Student.grade)).first()]

    print(oldest_student)

    # student_count = session.query(func.count(Student.id)).first()
    # print(student_count)

    query = session.query(Student).filter(Student.name.like('%duncan%'),
                                          Student.grade == 8)
    for record in query:
        print(record.name)

    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(student.name,
            student.grade) for student in session.query(Student)])

    query = session.query(
        Student
    ).filter(
        Student.name == "Albert Einstein"
    )
    # retrieve first the matching record as object
    # albert_einstein = query.first()

    # # delete record

    # session.delete(albert_einstein)
    # session.commit()

    # try to retrieve deleted record
    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)
