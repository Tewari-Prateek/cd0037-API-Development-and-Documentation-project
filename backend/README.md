# API Development and Documentation Final Project

## Trivia API Endpoints Documentation

### Getting Started
- Base URL: The backend app is hosted at localhost,:earth_asia:`http://127.0.0.1:5000/`
- Authentication: No API :key: or Authentication is required for Trivia App.

### Error Handling

The API will return five different type of errors on failed request:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity 
- 500: Internal Server Error

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 500,
    "message": "Internal Server Error"
}
```


### Endpoints
#### GET /categories
- General:
    - Retrieves all the categories from Database.
    - Returns:
        - A success value.
        - A dictionary of categories.
        - Count of all categories.
- Sample: `curl http://127.0.0.1:5000/categories`

```{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

#### GET /questions
- General:
    - Retrieves all questions from Database.
    - Returns:
       - A success value.
       - A list of questions.
       - Number of total questions.
       - A dictionary of categories.
       - Current selected category.
    - Results are paginated as 10 per page.
- Sample: `curl http://127.0.0.1:5000/questions`

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
  "currentCategory": "all", 
  "questions": [
    {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "all", 
  "questions": [
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
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "totalQuestions": 20
}
  
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the selected question.
    - Returns
        - A success value.
        - Id of the deleted question.
- Sample: `curl http://127.0.0.1:5000/questions/25 -X DELETE`
```
{
  "deleted": 25, 
  "success": true
}
```

#### POST /questions
- General:
    - Creates a new question or searches for the search term depending on the existence of the 'searchTerm' argument.
    - If 'searchTerm' exists, it returns:
        - A list of questions containing the search term.
        - A success value.
        - Number of total questions.
        - Current category.
    - Otherwise, returns:
        - A success value.
        - Id of the newly created question.
- Samples: 
    - Create question: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "The head quarters of International Olympic Committee is at?", "answer": "Lausanne in Switzerland", "difficulty": "4", "category": "6"}'`
    - Search question: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Butter"}'`

```
{
  "created": 25, 
  "success": true
}
```

```
{
  "current_category": "all", 
  "questions": [
    {
    "answer": "Lausanne in Switzerland.", 
    "category": "6", 
    "difficulty": "4", 
    "question": "The head quarters of International Olympic Committee is at?", 
    "success": true
}
  ], 
  "success": true, 
  "total_questions": 1
}
```

#### GET /categories/{category_id}/questions
- General:
    - Retrieves questions by category.
    - Returns:
        - A success value.
        - A list of questions by category.
        - Total number of questions within that category and the current category.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "currentCategory": "History", 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}
```

#### POST /quizzes
- General:
    - Starts the quiz by sending a request to the backend with a list of previously shown questions and the selected quiz category
    - Returns a success value and a question
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": ["17", "24"], "quiz_category": {"id": "2", "type": "Art"}}'`
```
{
  "question": {
    "answer": "Mihir Sen.", 
    "category": 6, 
    "difficulty": 5, 
    "id": 27, 
    "question": "The first man to swim across the Palk straits is?"
  }, 
  "success": true
}

```