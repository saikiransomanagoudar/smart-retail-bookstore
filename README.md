# Smart Retail Bookstore

An AI-powered bookstore application that leverages advanced language models and multi-agent systems to provide personalized book recommendations and intelligent shopping experiences.

![Smart Retail Bookstore Architecture](./architecture-diagram.png)

## System Overview

The Smart Retail Bookstore is a comprehensive e-commerce platform that combines modern web technologies with cutting-edge AI capabilities. Built on a microservices architecture, it features an intelligent multi-agent system powered by LangChain and OpenAI, providing users with personalized book recommendations, AI-powered chatbot assistance, and seamless order management.

## Architecture

The system follows a modern, scalable architecture with clear separation of concerns:

- **Frontend**: React-based single-page application with modern UI/UX
- **Backend**: FastAPI server with AI-powered services and multi-agent orchestration
- **Database**: PostgreSQL with user preference storage and order management
- **AI Services**: LangChain integration with OpenAI GPT models for intelligent operations
- **External APIs**: Hardcover GraphQL API for comprehensive book metadata

## Key Features

### AI-Powered Recommendations
- **Intelligent Book Matching**: Advanced recommendation engine using LangChain and OpenAI
- **User Preference Learning**: Dynamic preference analysis and adaptation
- **Contextual Understanding**: Multi-turn conversations for better recommendation accuracy

### Multi-Agent System
- **Operator Agent**: Central orchestrator managing all specialized agents
- **Recommendation Agent**: Specialized in book discovery and matching
- **Order Management Agents**: Handle order placement, tracking, and fraud detection
- **User Proxy Agent**: Manages user interactions and context

### AI Chatbot Assistant
- **Natural Language Processing**: Understands complex book-related queries
- **Conversation Memory**: Maintains context across multiple interactions
- **Multi-Modal Support**: Handles recommendations, orders, and general inquiries

### E-commerce Functionality
- **User Authentication**: Secure login with Clerk integration
- **Shopping Cart**: Persistent cart management with user preferences
- **Order Management**: Complete order lifecycle from placement to tracking
- **User Profiles**: Personalized dashboards and preference management

## Technology Stack

### Frontend
- **React 18** - Modern UI framework with hooks and functional components
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **Redux Toolkit** - State management with modern Redux patterns
- **React Router** - Client-side routing and navigation
- **Clerk** - Authentication and user management
- **Lucide React** - Beautiful, customizable icons
- **React Slick** - Carousel and slider components
- **Axios** - HTTP client for API communication

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Robust, open-source database
- **LangChain** - Framework for developing LLM-powered applications
- **OpenAI GPT-4o-mini** - Advanced language model integration
- **GraphQL** - Efficient data querying with external APIs
- **Pydantic** - Data validation and settings management

### AI & ML
- **LangChain Agents** - Multi-agent orchestration and task delegation
- **Conversation Memory** - Context-aware conversation management
- **Prompt Engineering** - Optimized prompts for better AI responses
- **LangGraph** - State management for multi-agent workflows

## Project Structure

```
smart-retail-bookstore/
├── backend/                          # FastAPI backend services
│   ├── app/
│   │   ├── api/                     # API endpoints and routers
│   │   │   ├── chatbot.py          # Chatbot API endpoints
│   │   │   └── recommendations.py  # Recommendation API endpoints
│   │   ├── core/                    # Core configuration and settings
│   │   │   ├── config.py           # Environment and app configuration
│   │   │   └── memory.py           # Memory management utilities
│   │   ├── database/                # Database configuration and models
│   │   │   ├── database.py         # Database connection and session management
│   │   │   └── initialize.py       # Database initialization scripts
│   │   ├── models/                  # Data models and schemas
│   │   │   ├── orders.py           # Order data models with CRUD operations
│   │   │   └── user.py             # User preference models
│   │   └── services/                # Business logic and AI services
│   │       ├── chatbot_service.py  # Multi-agent chatbot orchestration
│   │       ├── recommendation_agent.py # AI recommendation engine
│   │       ├── recommendation_service.py # Recommendation business logic
│   │       ├── operator_agent.py   # Central agent orchestrator
│   │       ├── order_placement_agent.py # Order processing agent
│   │       ├── order_query_agent.py # Order query and tracking agent
│   │       ├── fraudulent_transaction_agent.py # Fraud detection
│   │       ├── user_proxy_agent.py # User interaction management
│   │       ├── graphql_service.py  # External API integration
│   │       └── utils.py            # Utility functions
│   └── requirements.txt             # Python dependencies
├── frontend/                         # React frontend application
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── Authors/            # Author-related components
│   │   │   ├── Books/              # Book display components
│   │   │   ├── Chatbot/            # AI chatbot interface
│   │   │   ├── Home/               # Homepage and landing components
│   │   │   ├── Modals/             # Modal and dialog components
│   │   │   └── Profile/            # User profile components
│   │   ├── pages/                  # Main application pages
│   │   │   ├── Dashboard.jsx       # User dashboard with recommendations
│   │   │   ├── Cart.jsx            # Shopping cart management
│   │   │   ├── Login.jsx           # User authentication
│   │   │   ├── Signup.jsx          # User registration
│   │   │   ├── Profile.jsx         # User profile management
│   │   │   ├── OrderHistory.jsx    # Order tracking and history
│   │   │   ├── Settings.jsx        # User settings
│   │   │   ├── Favourite.jsx       # User favorites
│   │   │   ├── AllBooks.jsx        # Browse all books
│   │   │   ├── Authors.jsx         # Author listings
│   │   │   ├── ViewBookDetails.jsx # Book detail views
│   │   │   └── Loader.jsx          # Loading states
│   │   ├── Redux/                  # State management
│   │   │   ├── booksSlice.jsx      # Book state management
│   │   │   └── store.js            # Redux store configuration
│   │   └── main.jsx                # Application entry point
│   ├── package.json                 # Node.js dependencies
│   └── tailwind.config.js          # Tailwind CSS configuration
├── create_tables.py                 # Database initialization script
└── README.md                        # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- OpenAI API key
- Hardcover API access

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-retail-bookstore/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/bookstore_db
   OPENAI_API_KEY=your_openai_api_key
   HARDCOVER_API_TOKEN=your_hardcover_token
   ```

5. **Database setup**
   ```bash
   python create_tables.py
   ```

6. **Run the backend**
   ```bash
   python -m uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API authentication key | Yes |
| `HARDCOVER_API_TOKEN` | Hardcover GraphQL API token | Yes |
| `PROJECT_NAME` | Application name | No |
| `PROJECT_VERSION` | Application version | No |

### Database Schema

The application uses PostgreSQL with the following main tables:

- **user_preferences**: Stores user reading preferences and favorites
  - `user_id` (String, Primary Key)
  - `favorite_books` (Text)
  - `favorite_authors` (Text)
  - `preferred_genres` (Text)
  - `themes_of_interest` (Text)
  - `reading_level` (String)

- **orders**: Manages order information and status
  - `order_id` (String, Primary Key)
  - `user_id` (String, Foreign Key)
  - `title` (String)
  - `price` (Float)
  - `total_quantity` (Integer)
  - `street`, `city`, `state`, `zip_code` (String)
  - `card_number`, `expiry_date` (String)
  - `purchase_date`, `expected_shipping_date` (DateTime)

## API Endpoints

### Recommendations API
- `POST /api/recommendations/initial-recommendations` - Get initial book recommendations
- `GET /api/recommendations/trending-books` - Get trending books
- `POST /api/recommendations/preferences` - Save user preferences
- `GET /api/recommendations/preferences/{user_id}` - Get user preferences

### Chatbot API
- `POST /api/chatbot/chat` - Process chatbot messages
- `POST /api/chatbot/place-order` - Handle order placement
- `GET /api/chatbot/health` - Health check endpoint

## AI Agent System

The application features a sophisticated multi-agent system:

### Operator Agent
- **Role**: Central orchestrator and decision maker
- **Responsibilities**: 
  - Routes user requests to appropriate specialized agents
  - Manages conversation flow and context
  - Coordinates between different AI services
  - Uses LangGraph for state management

### Specialized Agents
- **Recommendation Agent**: Analyzes user preferences and generates book suggestions
- **Order Placement Agent**: Handles order creation and processing
- **Order Query Agent**: Manages order tracking and status inquiries
- **Fraudulent Transaction Agent**: Detects and prevents fraudulent activities
- **User Proxy Agent**: Manages user interactions and context

### Agent Communication
Agents communicate through a state graph managed by LangGraph, ensuring:
- Proper task delegation
- Context preservation
- Efficient resource utilization
- Scalable agent interactions

## User Scenarios

### 1. New User Onboarding
1. User completes preference questionnaire
2. System analyzes preferences using AI
3. Generates initial book recommendations
4. Stores preferences for future use

### 2. Personalized Recommendations
1. User logs into dashboard
2. System retrieves stored preferences
3. AI generates contextual recommendations
4. Results displayed with rich metadata

### 3. AI Chatbot Interaction
1. User initiates conversation
2. System routes to appropriate agent
3. Agent processes request using LLM
4. Response generated and streamed back

### 4. Order Management
1. User selects books and adds to cart
2. Order placement agent processes request
3. Fraud detection agent validates transaction
4. Order confirmed and tracking provided

## Security Features

- **Authentication**: Secure user authentication with Clerk
- **Authorization**: Role-based access control
- **Fraud Detection**: AI-powered transaction monitoring
- **Data Encryption**: Secure data transmission and storage
- **API Security**: Input validation and error handling

## Performance & Scalability

- **Asynchronous Processing**: FastAPI async/await for concurrent requests
- **Database Optimization**: Efficient queries with SQLAlchemy
- **AI Model Optimization**: Efficient prompt engineering and response handling
- **State Management**: Optimized Redux state updates
- **Component Optimization**: React performance best practices


## Deployment

### Local Development
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173` (Vite default)
- Database runs on local PostgreSQL instance

### Production Considerations
- Use production-grade database (PostgreSQL with connection pooling)
- Implement proper logging and monitoring
- Set up CI/CD pipelines
- Configure load balancers and CDN
- Implement backup and disaster recovery

## Acknowledgments

- **OpenAI** for providing the GPT models
- **LangChain** for the multi-agent framework
- **FastAPI** for the high-performance backend framework
- **React** for the frontend framework
- **Tailwind CSS** for the utility-first CSS framework

---
