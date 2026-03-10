 # Schedulix.io - AI-Powered Task Management System

## Overview

Schedulix.io is a modern, responsive task management application that leverages AI to help users plan and organize their daily tasks efficiently. Built with a Python FastAPI backend and a clean, modern frontend, this application provides intelligent task planning and routine generation.

**Live Demo**: [https://schedulix-io.vercel.app/](https://schedulix-io.vercel.app/)

**Source Code**: [https://github.com/Prince-darji-2306/Schedulix.io](https://github.com/Prince-darji-2306/Schedulix.io)

## Features

### 🤖 AI-Powered Task Planning
- **Smart Task Generation**: AI analyzes task descriptions and generates optimized plans
- **Adaptive Subtasks**: Automatically creates detailed subtasks based on task complexity
- **Time-Based Scheduling**: Plans tasks according to current time and deadlines
- **Multiple Plan Options**: Generates 3 diverse planning approaches for user choice

### 📋 Task Management
- **Task Creation**: Add tasks with titles, descriptions, and deadlines
- **Status Tracking**: Monitor task progress with pending, in-progress, and completed states
- **Plan Approval**: Review and approve AI-generated plans before execution
- **Subtask Management**: Break down complex tasks into manageable steps

### 🕐 Daily Routine Planning
- **AI-Generated Routines**: Automatically creates daily schedules based on approved plans
- **Time-Optimized**: Schedules tasks efficiently throughout the day
- **Interactive Interface**: Click to complete subtasks with visual feedback
- **Progress Tracking**: Visual indicators for completed and pending tasks

### 🔔 Notifications System
- **Real-time Alerts**: Stay informed about task approvals and completions
- **Status Updates**: Track system events and task progress
- **User-Friendly Interface**: Clean notification display with read/unread states

### 🎨 Modern Design
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Glassmorphism UI**: Modern visual effects with frosted glass cards
- **Dark/Light Theme**: Clean, professional color scheme
- **Smooth Animations**: Polished user experience with subtle transitions

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Relational database
- **LangGraph** - AI workflow orchestration
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - ORM for database operations
- **Passlib** - Password hashing and security
- **PyJWT** - JSON Web Token authentication

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **JavaScript ES6+** - Vanilla JavaScript for interactivity
- **Google Fonts** - Outfit font family
- **Glassmorphism Design** - Modern visual effects

### AI & ML
- **GROQ - OpenAI/GpT-Oss-20b** - Advanced language model for task planning
- **LangGraph** - Workflow orchestration for AI planning
- **JSON Schema** - Structured plan generation

## Architecture

### Backend Architecture
```
Schedulix.io Backend
├── API Layer (FastAPI)
│   ├── /api/tasks - Task management endpoints
│   ├── /api/routine - Daily routine generation
│   ├── /api/auth - Authentication
│   └── /api/notifications - Notification system
├── Services Layer
│   ├── auth_service.py - JWT authentication
│   └── task_service.py - Business logic
├── Repositories Layer
│   ├── task_repo.py - Task database operations
│   ├── user_repo.py - User management
│   └── database.py - Database connection
├── Core Layer
│   ├── llm_engine.py - AI integration
│   └── scheduler.py - Task scheduling
└── Graph Layer
    └── workflow.py - AI planning workflows
```

### Frontend Architecture
```
Schedulix.io Frontend
├── HTML Templates
│   ├── dashboard.html - Main dashboard
│   ├── tasks.html - Task management
│   ├── routine.html - Daily routine view
│   ├── notifications.html - Notifications center
│   ├── login.html - Authentication
│   └── register.html - User registration
├── CSS Styling
│   └── main.css - Complete responsive design
└── JavaScript
    ├── nav.js - Mobile navigation
    ├── tasks.js - Task management logic
    ├── routine.js - Routine interaction
    └── auth.js - Authentication handling
```

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database
- Groq API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/schedulix.io.git
cd schedulix.io
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Database Setup
```bash
# Create database
createdb task_planner

# Run migrations
python backend/scripts/init_postgres.py
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```bash
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/schedulix"

# Authentication
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
GROQ_API_KEY="your-api-key"
```

### 5. Run the Application
```bash
# Start the backend server
cd backend
python main.py

# Frontend is served statically by FastAPI
# Visit http://localhost:8000 in your browser
```

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `POST /api/logout` - User logout

### Task Management
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `POST /api/approve-plan` - Approve AI-generated plan
- `POST /api/subtasks/{id}/toggle` - Toggle subtask completion

### Routine & Notifications
- `GET /api/routine` - Get daily routine
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/{id}/read` - Mark notification as read

## Usage Guide

### Creating Tasks
1. Navigate to the Tasks page
2. Click "Add New Task"
3. Fill in task details:
   - Title (required)
   - Description (optional)
   - Deadline date and time
   - Initial status
4. Submit to generate AI plan

### Approving Plans
1. AI generates 3 different planning approaches
2. Review each plan's markdown summary
3. Click "Approve Plan" to finalize
4. Subtasks are automatically created and scheduled

### Daily Routine
1. Visit the Routine page
2. View today's scheduled tasks
3. Click subtasks to mark as complete
4. Visual feedback shows progress

### Notifications
1. Check the Notifications page
2. View system alerts and task updates
3. Mark notifications as read
4. Stay informed about task status

## Responsive Design Features

### Mobile-First Approach
- **Touch-Friendly**: Large buttons and inputs optimized for mobile
- **Flexible Layouts**: Cards stack vertically on small screens
- **Hidden Navigation**: Hamburger menu for mobile navigation
- **Optimized Typography**: Readable text sizes across devices

### Breakpoint System
- **Mobile**: 320px - 768px
- **Tablet**: 769px - 1024px  
- **Desktop**: 1025px+

### Key Responsive Features
- **Adaptive Grid**: 1-2-3 column layouts based on screen size
- **Flexible Navigation**: Collapsible menu with smooth animations
- **Touch Targets**: Minimum 44px touch targets for accessibility
- **Fluid Typography**: Scales text appropriately for each device

## AI Integration

### Planning Workflow
1. **Input Analysis**: AI analyzes task title, description, current time, and deadline
2. **Plan Generation**: Creates 3 diverse planning approaches
3. **Optimization**: Final plan combines best elements from all approaches
4. **Subtask Creation**: Generates detailed, time-scheduled subtasks
5. **Output**: Structured JSON with markdown summary and subtask list

### Time-Aware Scheduling
- **Current Time Integration**: Plans start from actual current time
- **Deadline Respect**: All subtasks finish before deadline
- **Incremental Timing**: Subtasks scheduled in logical time sequence
- **Time Rounding**: Smart time rounding for practical scheduling

## Security Features

### Authentication
- **JWT Tokens**: Secure stateless authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Token Expiration**: Automatic token expiration and refresh
- **CORS Protection**: Cross-origin resource sharing controls

### Data Protection
- **Input Validation**: Pydantic models ensure data integrity
- **SQL Injection Prevention**: ORM prevents SQL injection attacks
- **Environment Variables**: Sensitive data stored securely
- **HTTPS Ready**: Prepared for secure deployment

## Development

### Code Structure
- **Modular Design**: Clean separation of concerns
- **Type Hints**: Full Python type annotation support
- **Error Handling**: Comprehensive error handling and logging
- **Testing Ready**: Structure supports unit and integration testing

### Frontend Development
- **Vanilla JavaScript**: No framework dependencies
- **CSS-in-JS**: Clean separation of styles and logic
- **Responsive First**: Mobile-first design approach
- **Performance Optimized**: Minimal JavaScript bundle size

## Deployment

### Production Requirements
- **Web Server**: Nginx or similar reverse proxy
- **Database**: PostgreSQL with proper backups
- **SSL Certificate**: HTTPS for security
- **Environment**: Production-grade environment variables

### Docker Support (Optional)
```bash
# Build and run with Docker
docker-compose up -d
```

### Cloud Deployment
- **AWS**: Compatible with AWS ECS, Lambda, or EC2
- **Heroku**: Ready for Heroku deployment
- **Vercel**: Frontend can be deployed to Vercel
- **Railway**: Database and backend deployment options

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards
- **PEP 8**: Follow Python coding standards
- **Type Hints**: Include type annotations
- **Documentation**: Document public APIs and complex logic
- **Testing**: Write tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Contact

For support, questions, or feature requests:
- Create an issue on GitHub
- Email: support@schedulix.io
- Documentation: [Link to docs]

## Changelog

### v1.0.0
- Initial release with core task management features
- AI-powered planning system
- Responsive design implementation
- Complete authentication system
- Notification system
- Daily routine generation

## Acknowledgments

- **FastAPI Team** - For the excellent web framework
- **PostgreSQL** - For reliable database management
- **Contributors** - For their valuable contributions

---

**Schedulix.io** - Plan smarter, achieve more. 🚀