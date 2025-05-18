# SnapURL - Image Hosting Platform

A modern full-stack web application for uploading and sharing images with unique URLs. Built with FastAPI, React, and MongoDB.


DEMO: 

##  Features

- Image upload with drag-and-drop support
- Instant URL generation for sharing
- Modern, responsive UI with Chakra UI
- MongoDB integration for image metadata
- Dockerized for easy deployment
- RESTful API with FastAPI

##  Tech Stack

### Backend
- Python 3.11
- FastAPI
- MongoDB
- Motor (async MongoDB driver)
- Python-multipart for file uploads

### Frontend
- React
- Vite
- Chakra UI
- Axios
- React Icons

### Infrastructure
- Docker
- Docker Compose
- MongoDB Atlas (optional)

##  Project Structure

```
snapurl/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

##  Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd snapurl
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

##  API Endpoints

- `POST /upload` - Upload an image
- `GET /images` - List all uploaded images
- `GET /health` - Health check endpoint

## 🔧 Environment Variables

### Backend
- `MONGODB_URL` - MongoDB connection URL

### Frontend
- `VITE_API_URL` - Backend API URL

##  License

MIT

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 