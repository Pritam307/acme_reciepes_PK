# 🍲 Acme Recipes Backend

Backend application built with **Django**, **Graphene (GraphQL)**, **Django REST Framework (DRF)**, and **PostgreSQL (cloud)**.  
Implements recipe & ingredient management with GraphQL queries/mutations, JWT authentication, and Swagger docs.  

---

## 🚀 Features
- **GraphQL API** with Queries & Mutations
- **JWT Auth** (via DRF SimpleJWT)
- **REST Token Endpoints** for login/refresh
- **Swagger UI** for API documentation
- **PostgreSQL** (via `DATABASE_URL`, defaults to SQLite if not set)
- **CORS** enabled for frontend integration
- **Custom middleware** to make JWT auth work in GraphQL

---

## 🛠️ Setup & Installation

### 1. Clone repo
```bash
git clone <repo-url>
cd acme_recipes
```

> **ℹ️ This app is deployed at:**  
> [http://155.248.255.247:9091/](http://155.248.255.247:9091/)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
- Copy `.env.example` to `.env` and update values as needed.

---

## ⚡ Common Commands

### Run development server
```bash
python manage.py runserver
```

### Stop server
- Press `Ctrl+C` in the terminal running the server.

### Make migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

---

## 🐳 Docker Setup

### 1. Build Docker image
```bash
docker build -t acme_recipes .
```

### 2. Run with Docker Compose
```bash
docker-compose up
```

- The app will be available at [http://localhost:9091](http://localhost:9091)
- To stop, press `Ctrl+C` or run:
    ```bash
    docker-compose down
    ```

### 3. Run migrations in Docker
```bash
docker-compose exec web python manage.py migrate
```

### 4. Create superuser in Docker
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 🔗 GraphQL API Endpoints

- **GraphQL Playground/UI:**  
  [http://localhost:9091/graphql/](http://localhost:9091/graphql/)

### Example Queries & Mutations

#### Recipes

- **Query all recipes**
    ```graphql
    query {
      allRecipes {
        id
        title
        description
        ingredients {
          name
        }
      }
    }
    ```

- **Get single recipe**
    ```graphql
    query {
      recipe(id: 1) {
        id
        title
        description
      }
    }
    ```

- **Create recipe**
    ```graphql
    mutation {
      createRecipe(title: "Pasta", description: "Tasty", ingredients: ["Tomato", "Basil"]) {
        recipe {
          id
          title
        }
      }
    }
    ```

#### Ingredients

- **Query all ingredients**
    ```graphql
    query {
      allIngredients {
        id
        name
      }
    }
    ```

- **Create ingredient**
    ```graphql
    mutation {
      createIngredient(name: "Salt") {
        ingredient {
          id
          name
        }
      }
    }
    ```

#### Auth

- **Obtain JWT token**
    ```graphql
    mutation {
      tokenAuth(username: "youruser", password: "yourpass") {
        token
      }
    }
    ```

- **Refresh JWT token**
    ```graphql
    mutation {
      refreshToken(token: "yourtoken") {
        token
      }
    }
    ```

---

## 📚 API Docs

- **Swagger UI:**  
  [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---
