# Superheroes API

A Flask-based REST API for managing superheroes, their powers, and the relationships between them. This API allows users to retrieve information about heroes and powers, update power descriptions, and create associations between heroes and their powers.

## Features

The Superheroes API provides the following endpoints:

- **Heroes Management**: Retrieve all heroes or get details of a specific hero including their associated powers.
- **Powers Management**: Retrieve all powers or get details of a specific power including associated heroes, and update power descriptions.
- **Hero-Powers Relationships**: Create new associations between heroes and powers with specified strength levels.

## Setup Instructions

Follow these steps to set up and run the Superheroes API locally:

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**

   ```bash
   flask db init
   ```

3. **Create and Apply Migrations**

   ```bash
   flask db migrate
   flask db upgrade
   ```

4. **Seed the Database**

   ```bash
   python seed.py
   ```

5. **Start the Server**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`.

## API Endpoints

### Get All Heroes

- **Method**: GET
- **Endpoint**: `/heroes`
- **Description**: Retrieves a list of all heroes with basic information.
- **Response Example**:
  ```json
  [
    {
      "id": 1,
      "name": "Kamala Khan",
      "super_name": "Ms. Marvel"
    },
    {
      "id": 2,
      "name": "Doreen Green",
      "super_name": "Squirrel Girl"
    }
  ]
  ```

### Get Hero by ID

- **Method**: GET
- **Endpoint**: `/heroes/<id>`
- **Description**: Retrieves detailed information about a specific hero, including their powers.
- **Response Example** (Success):
  ```json
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel",
    "powers": [
      {
        "id": 1,
        "name": "Super Strength",
        "description": "Gives the wielder super human strength"
      },
      {
        "id": 2,
        "name": "Flight",
        "description": "Gives the ability to fly through the skies at supersonic speed"
      }
    ]
  }
  ```
- **Error Response** (404):
  ```json
  {
    "error": "Hero not found"
  }
  ```

### Get All Powers

- **Method**: GET
- **Endpoint**: `/powers`
- **Description**: Retrieves a list of all powers with basic information.
- **Response Example**:
  ```json
  [
    {
      "id": 1,
      "name": "Super Strength",
      "description": "Gives the wielder super human strength"
    },
    {
      "id": 2,
      "name": "Flight",
      "description": "Gives the ability to fly through the skies at supersonic speed"
    }
  ]
  ```

### Get Power by ID

- **Method**: GET
- **Endpoint**: `/powers/<id>`
- **Description**: Retrieves detailed information about a specific power, including associated heroes.
- **Response Example** (Success):
  ```json
  {
    "id": 1,
    "name": "Super Strength",
    "description": "Gives the wielder super human strength",
    "heroes": [
      {
        "id": 1,
        "name": "Kamala Khan",
        "super_name": "Ms. Marvel"
      }
    ]
  }
  ```
- **Error Response** (404):
  ```json
  {
    "error": "Power not found"
  }
  ```

### Update Power Description

- **Method**: PATCH
- **Endpoint**: `/powers/<id>`
- **Description**: Updates the description of a specific power. The description must be at least 20 characters long.
- **Request Body**:
  ```json
  {
    "description": "Updated description that is at least 20 characters long"
  }
  ```
- **Response Example** (Success):
  ```json
  {
    "id": 1,
    "name": "Super Strength",
    "description": "Updated description that is at least 20 characters long"
  }
  ```
- **Error Response** (400):
  ```json
  {
    "errors": ["Description must be at least 20 characters"]
  }
  ```

### Create Hero-Power Relationship

- **Method**: POST
- **Endpoint**: `/hero_powers`
- **Description**: Creates a new association between a hero and a power with a specified strength level.
- **Request Body**:
  ```json
  {
    "strength": "Strong",
    "hero_id": 1,
    "power_id": 2
  }
  ```
- **Response Example** (Success - 201):
  ```json
  {
    "id": 1,
    "strength": 10,
    "hero_id": 1,
    "power_id": 2,
    "hero": {
      "id": 1,
      "name": "Kamala Khan",
      "super_name": "Ms. Marvel"
    },
    "power": {
      "id": 2,
      "name": "Flight",
      "description": "Gives the ability to fly through the skies at supersonic speed"
    }
  }
  ```
- **Error Response** (400):
  ```json
  {
    "errors": ["Strength must be Strong, Weak, or Average", "Hero not found"]
  }
  ```

## Technologies Used

- **Flask**: Web framework for building the API
- **SQLAlchemy**: ORM for database interactions
- **Flask-Migrate**: Database migration management
- **Python**: Programming language
- **SQLite**: Database for data storage

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please contact:

- Email: your.email@example.com
- GitHub: [Your GitHub Profile](https://github.com/yourusername)
