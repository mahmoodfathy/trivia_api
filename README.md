# trivia_api Full Stack App
## Getting Started

### Introduction
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1-Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2-Delete questions.

3-Add questions and require that they include question and answer text.

4-Search for questions based on a text query string.

5-Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.


### Audience 
This documentation is designed for people familiar with JavaScript,python programming and object-oriented programming concepts.
This conceptual documentation is designed to let you quickly start exploring the trivia api and have fun playing and share it with other people.

### API



```
Endpoints
GET '/api/categories'
GET '/api/questions'
GET '/api/categories/<int:id>/questions'
POST '/api/questions'
POST '/api/questions/search'
POST '/api/quizzes'
DELETE '/api/questions/<int:id>'
```
### GET EndPoints
```
GET '/api/categories'
```

```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
```
GET '/api/questions?page=<page_number>' 
```
```
Fetches a paginated dictionary of questions of all available categories
- Request Arguments (optional): page_number:int
- Retruns: an object with categories , that contains a object of id: category_string key:value pairs,current_category,questions , succes status, and number of total questions
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
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
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
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
 "total_questions": 19
}

```
```
GET '/api/categories/<int:id>/questions'
```
```
Fetches a dictionary of questions for the specified category
request parameters: id(category id) :int
returns
{
  "current_category": 1, 
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
  ], 
  "success": true, 
  "total_questions": 2,
  "code":200
}

```
### Post EndPoints
```
POST '/api/questions'
```
```
This endpoint creates a new question
request body :
        {
            'question':"how to make tests?",
            'answer': 'unitest',
            'difficulty': 1,
            'category':1
        }
returns 
      {
        'success': true,
        'code': 200
      }
```
```
POST '/api/questions/search'
```
```
This endpoint searches for term in a question and returns all the question including this term case insensitive
request body :{
searchTerm:string
}
returns 
{
'success':true,
'code':200,
 "questions": [
    {
      "answer": "Juve", 
      "category": 6, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is cristiano's team?"
    }
  ], 
'total_questions':1
}
```
```
POST '/api/quizzes'
```
```
this endpoint returns random non repeating questions in a specific category, if the there are no more questions returns a 404 not found error

request body:
{
'previous_questions':array,
'quiz_category':{'type':string,'id':int}
}
returns
{
        'question':{
      "answer": "Juve", 
      "category": 6, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is cristiano's team?"
                    } ,
        'success':true,
        'code':200
      }
if there are no more questions in this category then it returns
{
      'success':false,
      'code':404,
      'message':'resource not found!'
    }

```
### DELETE EndPoints
```
DELETE '/api/questions/<int:id>'
```
```
This endpoint deletes a specific question 
request parameters: question id:int
returns

{
      'success':true,
      'code':200
    }
in case any errors it returns a 404 error with this response:

{
      'success':false,
      'code':404,
      'message':'resource not found!'
    }
```
