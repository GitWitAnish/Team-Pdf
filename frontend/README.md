# Nepal Legal AI - React Frontend

A modern React.js frontend for the Nepal Legal AI chatbot, designed to help users query Nepali legal documents.

## Features

- 🎨 **Modern Dark UI** - ChatGPT-inspired dark theme
- 💬 **Chat Interface** - Intuitive conversational UI
- 📚 **Source Citations** - Expandable source references for each answer
- 📱 **Responsive Design** - Works on desktop and mobile
- ⚡ **Fast & Lightweight** - Built with Vite + React 18

## Project Structure

```
frontend/
├── index.html                # Entry HTML (Vite)
├── vite.config.js            # Vite configuration
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx       # Navigation sidebar
│   │   ├── Sidebar.css
│   │   ├── Welcome.jsx       # Welcome screen with suggestions
│   │   ├── Welcome.css
│   │   ├── ChatMessage.jsx   # Individual chat message
│   │   ├── ChatMessage.css
│   │   ├── ChatInput.jsx     # Chat input component
│   │   └── ChatInput.css
│   ├── services/
│   │   └── api.js            # API communication
│   ├── App.jsx               # Main application
│   ├── App.css
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── .env.example
├── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend setup)

### Installation

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create environment file:

   ```bash
   cp .env.example .env
   ```

4. Configure the API URL in `.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```

### Running the App

Start the development server:

```bash
npm run dev
```

The app will open at [http://localhost:3000](http://localhost:3000)

### Building for Production

```bash
npm run build
```

The build output will be in the `build/` folder.

Preview the production build:

```bash
npm run preview
```

## Backend Setup

The frontend requires the FastAPI backend to be running:

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:

   ```bash
   python main.py
   ```

   Or with uvicorn:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

The API will be available at [http://localhost:8000](http://localhost:8000)

## API Endpoints

| Method | Endpoint      | Description              |
| ------ | ------------- | ------------------------ |
| GET    | `/health`     | Health check             |
| POST   | `/api/search` | Search and get AI answer |

### Search Request

```json
{
  "question": "What are fundamental rights in Nepal?",
  "top_k": 8,
  "use_llm": true,
  "llm_model": "gpt-3.5-turbo"
}
```

### Search Response

```json
{
  "answer": "The fundamental rights in Nepal include...",
  "sources": "**1. Constitution of Nepal (2072)**\n> ..."
}
```

## Customization

### Theming

Edit the CSS files to customize colors:

- **Primary color**: `#10a37f` (green)
- **Background**: `#171717` (dark)
- **Surface**: `#212121` (slightly lighter)
- **Border**: `#303030`
- **Text**: `#ececec`

### Adding Suggestions

Edit the `suggestions` array in `src/components/Welcome.js` to add or modify suggestion cards.

## License

This project is built for the Nepal Legal AI hackathon.
