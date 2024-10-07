# FoodDist
Matching the distributor of food ingredients with restaurants/cafes.

This project is an AI-powered sales assistant that helps users find product suggestions based on restaurant menus. It consists of a React frontend and a FastAPI backend.

## Features

- Search for restaurants
- Retrieve restaurant menus
- Compute similarities between menu items and distributor products
- Analyze matches to provide product suggestions to distributors.

## Prerequisites

- Node.js (v14 or later)
- Python (v3.11 or later)
- npm or yarn

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Start the backend server:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn install
   ```

3. Start the development server:
   ```
   npm run dev
   ```
   or
   ```
   yarn dev
   ```

The frontend will be available at `http://localhost:5173`.

## Environment Setup

### Backend Configuration

The backend requires a `.env` file in the root of the backend directory. This file should contain the necessary environment variables for the application to function correctly.

1. Create a file named `.env` in the backend directory.
2. Add the following content to the file:

```
OPENAI_API_KEY=<your_openai_api_key>
```

Replace `<your_openai_api_key>` with your actual OpenAI API key.


## Usage

1. Open your browser and go to `http://localhost:5173`.
2. Enter a restaurant name in the search bar.
3. The AI assistant will search for the restaurant, retrieve its menu, and provide product suggestions based on the menu items.

## Project Structure

- `frontend/`: Contains the React frontend application
- `backend/`: Contains the FastAPI backend application

## Technologies Used

- Frontend:
  - React
  - TypeScript
  - Vite
  - Tailwind CSS
- Backend:
  - Python
  - FastAPI
  - OpenAI API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.