# Code Challenge: Python API Development

**Objective:**

Develop a RESTful API using Django or FastAPI framework that manages a simple "Bookstore". Your API will provide endpoints to create, read, update, and delete books in the store. Include functionality to handle user authentication to allow only registered users to modify the bookstore content.

## Requirements:
<details>


### API Functionality:

- Create a model for Books with fields: title, author, publish_date, ISBN, and price.
- Implement CRUD operations for the Books model.
- Implement user authentication: Users should register with at least an email and password.
- Only authenticated users can perform create, update, or delete operations.
- All users (authenticated or not) can list and read information about the books.

### Database:

- Use any SQL or NoSQL database of your choice to store data.

### Documentation:

- Provide a README file that includes:
  - Instructions on how to set up and run the application.
  - A brief description of the API's functionality.

### Testing:

- Write unit tests for your models and endpoints.
- Include API tests to demonstrate how each endpoint works.

### System Diagram:

- Provide a system architecture diagram showing the API, database, and any other components of your system.

### Deployment:

- Deploy your application to a free hosting provider (e.g., Heroku, PythonAnywhere, or any other).
- Provide a URL to the live API.

### Bonus (optional):

- The API needs to support a volume of 1000 requests per second in a stress test in both write and read operations.
- Can upload an image with the book cover.
- Implement rate limiting for your API.
- Add filters to list endpoints, such as filtering books by author or publish_date.
- Setup CI/CD

### Submission:

- Submit your code in a version-controlled repository (e.g., GitHub).
- Provide the system diagram as part of your repository.
- Include a Postman collection or an OpenAPI specification file to interact with the API.
- The documentation should be comprehensive and clear, suitable for new developers who are not familiar with your project.

### Evaluation Criteria:

- API should inmplement "REST API Design Best Practices". Check it out there are several good articles in the internet.
- Functionality: The API works as described in the requirements.
- Code Quality: The code is clean, modular, and follows Pythonic principles.
- Testing: The application has thorough tests, and all tests pass.
- Documentation: The documentation is clear and helpful.
- History of commits (structure and quality)
- Technical choices: Is the choice of libraries, database, architecture, etc. the best choice for the application?
- Extra Features: Implementation of the bonus features will be considered a plus.

## Doubts

Any questions you may have, please contact us by e-mail.

Godspeed! ;)

  <summary>Click to view requirements</summary>

</details>


## System Diagram

![d1.png](documents%2Fimages%2Fd1.png)

### Technical choices
- Webserver: Uvicorn ASGI
- Django 4.2: 
  - django-ninja: framework to building the APIs, Fast, Async-ready, heavily inspired by FastAPI 
- PG Bouncer: connection pooler for PostgreSQL, managing efficient database connections, reducing overhead, and providing features like load balancing and connection limits for improved performance.
- PostgresSQL: Open-source relational database management system.

I chose to implement async APIs for better scalability and responsiveness. Async allows efficient handling of concurrent requests, ensuring improved performance in handling a large number of operations simultaneously.  


#### Benchmark API with 20 concurrent clients, and send total 5000 GET requests 

![ab.png](documents%2Fimages%2Fab.png)
The server load is quite good, achieving a throughput of 1,343 requests per second.

## Testing

### Open API: http://51.79.248.178:8000/api/openapi.json
### Swagger UI: http://51.79.248.178:8000/api/docs

- Demo account:
    - Username: admin
    - Password: admin

  You can use this account to login via API `/auth/login` or register a new account to yourself
