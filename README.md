# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

### Documentation API Refrence

Getting started 
    >BASE URL: The url can be run locally as it is not hosted. It can be run from the backend at http://127.0.0.1:5000/, then it will be set to http://localhost:3000/ on the frontend.
    >AUTHENTICATION: None

Error Handling
    Errors are be returned as JSON objects using this format:

    ```json
        {
            "error": 404, 
            "message": "resource not found", 
            "success": false
        }
    ```
    This API will return only these type of erros:
        > 404 : Not Found
        > 422 : Unprocessable

Endpoints
    GET '/categories'
    >Gets a dictionary of categories where the keys are the ids and the values are the string equivalent of the id
    >Returns an object with the key 'categories' which has an object id : type

        ```json
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

    GET '/questions?page={int}'
    >Gets a dictionary of paginated questions where the keys are the ids and the values are the string equivalent of the id
    >Request Argument: 'page' int
    >Returns an object with the key 'questions' which has an object id : An object with 10 paginated questions, total questions, object including all categories, and current category string

        ```json
            {
            "questions": [
                {
                "id": 2,
                "question": "question",
                "answer": "answer",
                "difficulty": 3,
                "category": 1
                }
            ],
            "totalQuestions": 21,
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "currentCategory": ""
            }
        ```

    DELETE '/questions/<int:id>'
    >Takes the id of the question to be deleted then deletes that specific question
    >Request Argument: int id
    >Does not require any return value, it will only return the status code to indicated success or not

    POST '/questions'
    >sends a post to create a new question
    >Request Body:

        ```json
        {
        "question": "new question",
        "answer": "new answer",
        "difficulty": 3,
        "category": 1
        }
        ```
    >Does not need to return any data

    POST '/question'
    >Sends a post to search for the provided search term
    >Request Body:

        ```json
        {
        "searchTerm": "search term from the user"
        }
        ```
    >Returns a list of questions, a number of totalQuestions that met the search term and the current category string

    GET '/categories/<int:id>/questions'
    >gets the questions based on the spcific category id provided 
    >Request Argument int id
    >Returns an object with questions for the specified category, total questions, and current category string

        ```json
        {
        "questions": [
            {
            "id": 3,
            "question": "question",
            "answer": "answer",
            "difficulty": 3,
            "category": 1
            }
        ],
        "totalQuestions": 100,
        "currentCategory": "Science"
        }
        ```

    POST '/quizzes'
    >Send a post to get the next question
    >Request Body:

        ```json
        {
            'previous_questions' : {[4, 2, 1, 10]}
            'quiz_category' : 'currentCategory'
        }
        ```

    >Returns and object with a single question

        ```json
        {
        "question": {
            "id": 1,
            "question": "question",
            "answer": "answer",
            "difficulty": 3,
            "category": 2
        }
        }
        ```
    
