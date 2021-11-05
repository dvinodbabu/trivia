# Trivia - A quiz game


## Full Stack Trivia



The project is a quiz game where user can select a field from the list of category and test his knowledge.

The developers were tasked to create api's to work in conjecture frontend. The requirements are as below.
1. Display questions - both all questions and by category. Questions should show the question, 
   category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Pre-Requirements
### Dependencies
The techstack that this application use are python, node and postgresql.

The following dependencies should be installed prior running the application
1. python (3.7 or higher)
2. pip (preinstalled with python)
3. node (tested with v16.13.0)
4. npm (tested with 8.1.0)
5. postgresql (optional - if you use remote server)

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. 

```bash
cd ${PROJECT_PATH}\backend
createdb trivia
psql trivia < trivia.psql
```

### Backend


1. setup a virtual environment
```
cd ${PROJECT_PATH}\backend
python3 -m venv dev
dev\Scripts\activate.bat
```
2. Install the python dependencies
```
cd ${PROJECT_PATH}\backend
pip install -r requirements.txt
```
3. Start the server
The flask development server will start in port 5000 (http://localhost:5000)
```
cd ${PROJECT_PATH}\backend
SET FLASK_APP=flaskr
SET FLASK_ENV=development
python -m flask run
(windows users can alternatively you can run the run.bat script in /backend folder)
```

### Frontend

1. Install the node dependencies and packages using the below command
```bash
cd ${PROJECT_PATH}\frontend
npm install
```

2. Start the development server using the below command (start the backend server first)
The node server will start in the port 3000 (http://localhost:3000)
```bash
cd ${PROJECT_PATH}\frontend
npm start
```
## API Documentation

* Base URL: The backend is hosted at `http://localhost:5000/`
* Authentication: None

### Error Handling

Errors are returned in the below JSON format:
```
    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }
```
The API will return the following types of errors:

* 500 - Server Error
* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

## API end-points

#### GET /categories
* Definition: fetches list of categories
* Sample: `curl -X GET http://localhost:5000/categories`<br>
* Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```
#### GET /questions
* Definition: fetches list of questions. Supports pagination.
* Sample: `curl -X GET http://localhost:5000/questions?page=1`<br>
* Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 30
}
```
#### GET /categories/{category_id}/questions
* Definition: fetches list of questions by category
* Sample: `curl -X GET http://localhost:5000/categories/1/questions`<br>
* Response:
```
{
    "current_category": [
        [
            "Science"
        ]
    ],
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```
#### DELETE /questions/{question_id}
* Definition: Deletes a question by question_id
* Sample: `curl -X DELETE http://localhost:5000/questions/40`<br>
* Response:
```{
    "deleted": 40,
    "success": true,
    "total_questions": 41
}
```
#### POST /questions/query
* Definition: Searches question(s) based on a search term 
* Sample: `curl -X POST -d "{\"searchTerm\": \"Tom\"}" -H "Content-Type: application/json" http://localhost:5000/questions/query`<br>
* Response:
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "totalQuestions": 1
}
```
#### POST /quizzes
* Definition: Starts the quiz game. Displays questions based on the user selected 
category randomly. This is api also keeps track of the questions already asked.
* Response:
```
{
        'success': True,
        'question': new_question
}
```
#### POST /questions
* Definition: Adds a new question to the questions database.
* Response:
```
{
       'success' : True,
       'created' : new_question id
       'total_questions' : total number of questions
}
```