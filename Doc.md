Getting Started

    Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
    Authentication: This version of the application does not require authentication or API keys.

Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:

    400: Bad Request
    404: Resource Not Found
    422: Not Processable

Endpoints
GET /categories

    General:
        Returns a list of question categories  objects, and success value
        .
    Sample: curl http://127.0.0.1:5000/categories

  {"Categories":[
    {
        "id":1,
        "type":"Science"
    },
    {
        "id":2,
        "type":"Art"
    },
    {
        "id":3,
        "type":"Geography"
    },
    {
        "id":4,
        "type":"History"
    },
    {
        "id":5,
        "type":"Entertainment"
    },
    {
        "id":6,
        "type":"Sports"
    }
    ],
    "success":true
    }

GET /questions

    General:
        Returns a list of questions  objects, total number of Questions and success value. the results are paginated
        .
    Sample: curl http://127.0.0.1:5000/questions?page=1

{
    "Questions":
    [
        {
            "category":4,
            "id":5,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "category":4,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
        {
            "category":5,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "category":5,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "category":5,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "category":6,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "category":6,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "category":3,
            "id":14,
            "question":"In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "category":3,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        },
        {
            "category":2,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }
    ],
    "Total Number of Questions":17,
    "categories":["Science","Art","Geography","History","Entertainment","Sports"],
    "success":true
}


DELETE /questions/<int:question_id>

    General:
        Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question.
    curl -X DELETE http://127.0.0.1:5000/books/4
{
    "Questions":
    [
        {
            "answer":"Maya Angelou",
            "category":4,
            "difficulty":2,
            "id":5,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
        {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer":"The Palace of Versailles",
            "category":3,
            "difficulty":3,
            "id":14,
            "question":"In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer":"Agra",
            "category":3,
            "difficulty":2,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        },
        {
            "answer":"Escher",
            "category":2,
            "difficulty":1,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },{
            "answer":"Mona Lisa",
            "category":2,
            "difficulty":3,
            "id":17,
            "question":"La Giaconda is better known as what?"
        },
        {
            "answer":"One",
            "category":2,
            "difficulty":4,
            "id":18,
            "question":"How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer":"The Liver",
            "category":1,
            "difficulty":4,
            "id":20,
            "question":"What is the heaviest organ in the human body?"
        },
        {
            "answer":"Alexander Fleming",
            "category":1,
            "difficulty":3,
            "id":21,
            "question":"Who discovered penicillin?"
        },
        {
            "answer":"Blood",
            "category":1,
            "difficulty":4,
            "id":22,
            "question":"Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer":"Scarab",
            "category":4,
            "difficulty":4,
            "id":23,
            "question":"Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer":"Adeyi Qudus",
            "category":4,
            "difficulty":4,
            "id":24,"question":"what is your name"
        }
    ],
    "deleted":4,
    "success":true,
    "total_questions":16
}


POST /questions

    General:
        Creates a new questio using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend.
    curl http://127.0.0.1:5000/question -X POST -H "Content-Type: application/json" -d '{"question": "What is your name", "answer": "Adeyi Q", "category": "5", "difficulty": 10}'

{
  "books": 
  [
    {
        "question": "What is your name", 
        "answer": "Adeyi Q", 
        "category": "5", 
        "difficulty": 10
    }
  ],
  "created": 24,
  "success": true,
  "total_questions": 17
}





PATCH /books/{book_id}

    General:
        If provided, updates the rating of the specified book. Returns the success value and id of the modified book.
    curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'

{
  "id": 15,
  "success": true
}
