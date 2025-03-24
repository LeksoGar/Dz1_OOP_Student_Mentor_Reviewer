class Student:
    all_students = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.all_students.append(self)

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        if not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть в диапазоне от 1 до 10.'
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка: Лектор не закреплен за курсом или студент не учится на этом курсе.'

    def calculate_avg_grade(self):
        """Вычисление средней оценки студента"""
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg_grade = self.calculate_avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress or 'Нет'}\n"
                f"Завершенные курсы: {finished_courses or 'Нет'}")

# Сравнение студентов по средней оценке
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_avg_grade() == other.calculate_avg_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_avg_grade() < other.calculate_avg_grade()

    @classmethod
    def calculate_avg_student_grade(cls, course):
        """Подсчет средней оценки за ДЗ по всем студентам в рамках конкретного курса"""
        all_grades = []
        for student in cls.all_students:
            if course in student.grades:
                all_grades.extend(student.grades[course])
        return sum(all_grades) / len(all_grades) if all_grades else 0


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    all_lecturers = []

    def __init__(self,name, surname):
        super().__init__(name, surname)
        self.grades = {}
        Lecturer.all_lecturers.append(self)

    def calculate_avg_grade(self):
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg_grade = self.calculate_avg_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.1f}"

# Сравнение лекторов по средней оценке
    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_avg_grade() == other.calculate_avg_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_avg_grade() < other.calculate_avg_grade()

    @classmethod
    def calculate_avg_lecturer_grade(cls, course):
        all_grades = []
        for lecturer in cls.all_lecturers:
            if course in lecturer.grades:
                all_grades.extend(lecturer.grades[course])
        return sum(all_grades) / len(all_grades) if all_grades else 0


class Reviewer(Mentor):
    def __init__(self,name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if not (1 <= grade <= 10):
            return 'Ошибка. Оценка должна быть в диапазоне от 1 до 10.'
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка: Эксперт не закреплен за курсом или студент не учится на курсе.'

    def __str__(self):
       return f"Имя: {self.name}\nФамилия: {self.surname}"


student1 = Student('Алексей', 'Гармаш','муж')
student2 = Student('Анна','Русова','жен')

lecturer1 = Lecturer('Препод','Строгий')
lecturer2 = Lecturer('Учитель','Добрый')

reviewer1 = Reviewer('Клавдия','Петрова')
reviewer2 = Reviewer('Константин','Ватрушка')

student1.courses_in_progress.append('Python')
student1.courses_in_progress.append('Git')
student1.finished_courses.append('Введение в программирование')
student2.courses_in_progress.append('Python')
student2.finished_courses.append('Английский для всех сфер деятельности')

lecturer1.courses_attached.append('Python')
lecturer2.courses_attached.append('Python')

reviewer1.courses_attached.append('Python')
reviewer2.courses_attached.append('Python')

student1.rate_lecturer(lecturer1,'Python', 10)
student1.rate_lecturer(lecturer1,'Python', 9)
student2.rate_lecturer(lecturer2,'Python', 8)
student2.rate_lecturer(lecturer2,'Python', 7)

reviewer1.rate_hw(student1,'Python', 8)
reviewer1.rate_hw(student1,'Python', 7)
reviewer2.rate_hw(student2,'Python', 6)
reviewer2.rate_hw(student2,'Python', 5)

print("Студенты:")
print(student1)
print()
print(student2)
print()

print("Лекторы:")
print(lecturer1)
print()
print(lecturer2)
print()

print("Проверяющие:")
print(reviewer1)
print()
print(reviewer2)
print()

print("Сравнение студентов:")
print(f"Меньше ли средняя оценка за домашние задания у {student2.name[:-1]}ы в сравнении c {student1.name[:-1]}ем? -", student2 < student1)
print(f"Равны ли средние оценки за домашние задания у {student1.name[:-1]}я и {student2.name[:-1]}ы? -", student1 == student2)
print()
print("Сравнение лекторов:")
print(f"Меньше ли средняя оценка за лекции у {lecturer2.name[:-1]}я в сравнении c {lecturer1.name}ом? -", lecturer2 < lecturer1)
print(f"Равны ли средние оценки за лекции у {lecturer1.name}а и {lecturer2.name[:-1]}я? -", lecturer1 == lecturer2)
print()

print("Средняя оценка студентов по курсу Python:", Student.calculate_avg_student_grade('Python'))
print("Средняя оценка лекторов по курсу Python:", Lecturer.calculate_avg_lecturer_grade('Python'))



