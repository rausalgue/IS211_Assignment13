DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS grades;

CREATE TABLE student (
  Identifier INTEGER PRIMARY KEY,
  FirstName TEXT,
  LastName TEXT
);

CREATE TABLE quizzes (
  Identifier INTEGER PRIMARY KEY,
  Subject TEXT,
  TotalQuestions INTEGER,
  Date TEXT
);

CREATE TABLE grades (
  Identifier INTEGER PRIMARY KEY,
  Student INTEGER,
  Quiz INTEGER,
  Grade INTEGER,
  FOREIGN KEY (Student) REFERENCES student(Identifier),
  FOREIGN KEY (Quiz) REFERENCES quizzes(Identifier)
);