# theatre-management-system

Theatre API Service is an API designed to manage data about a theater and its performances. The API allows you to:

## Functionality

### Get information about performances:
- Show time
- Performance date and time

### Get information about actors:
- Actor name
- Actor photo

### Get information about genres:
- Genre name

### Ticket
- Available seats

### Get information about plays:
- Play name
- Play description
- Play actors
- Play genres
- Play image

### Book tickets:
- Select a performance
- Select seats

### Get information about the theater hall:
- Number of seats
- Seat layout

### Filter plays:
- By actors
- By genres
- By date

### Filter performances:
- By play
- By date

## Technologies

- **API**: RESTful
- **Data format**: JSON
- **Programming language**: Python 3
- **Framework**: Django
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Version control system**: Git
- **Documentation**: Swagger

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/stamaksim/theatre-management-system
    cd theatre-management-system
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Run using Docker:**
    ```bash
    docker-compose up --build
    ```

## Usage

Once the server is running, you can access the API documentation at `http://localhost:8000/swagger/`.

### Example Requests

**Get all performances:**
```bash
GET /api/theatre/plays

Response:
[
  {
    "id": 1,
    "name": "Hamlet",
    "description": "A tragedy written by William Shakespeare",
    "genres": ["Tragedy"],
    "actors": ["John Doe", "Jane Smith"],
    "image": "url_to_image"
  },
  {
    "id": 2,
    "name": "Macbeth",
    "description": "A tragedy written by William Shakespeare",
    "genres": ["Tragedy"],
    "actors": ["Jim Brown", "Sara White"],
    "image": "url_to_image"
  }
]
