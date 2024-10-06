## Cats Exhibition

A comprehensive app for managing cats and their details for exhibitions. Keep track of each cat's breed, age, color, and more, and efficiently organize information for cat exhibition events.

Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

1. **Clone the Repository**
    Clone the repository to your local machine:
    ```
    git clone git@github.com:Komanok-dev/exhibition.git
    cd exhibition
    ```

2. **Create .env file in the project folder and fill it with these data:**
    ```
    DATABASE_DRIVER=
    DATABASE_USERNAME=
    DATABASE_PASSWORD=
    DATABASE_HOSTNAME=
    DATABASE_PORT=
    DATABASE_NAME=
    ```

3. **Build and Run the Docker Containers:**
    ```
    docker-compose up --build
    ```

4. **Seed the Database by default data if you need:**
    ```
    docker-compose exec app python initial_data.py
    ```

5. **Access the Application:**

The application will be running on http://localhost:8000.
Swagger UI: You can view the API documentation and test the endpoints using Swagger UI:
    ```
    http://localhost:8000/docs
    ```

4. **Testing:**

Run app and then execute the following command:
    ```
    docker-compose exec app pytest
    ```
