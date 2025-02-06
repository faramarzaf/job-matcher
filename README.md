# Job Matcher

Job Matcher is a web application designed to help users find job opportunities that align with their skills and preferences.

## Features

- **User-Friendly Interface**: Navigate through job listings with ease.
- **Skill-Based Matching**: Receive job recommendations based on your unique skill set.
- **Real-Time Updates**: Stay informed with the latest job openings.

## Technologies Used

- **Backend**: Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **Containerization**: Docker

## Getting Started

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/faramarzaf/job-matcher.git
   cd job-matcher

2. **Set Up the Environment**:
Ensure you have Python installed. 
Install the required Python packages: 
   ```bash
       pip install -r requirements.txt 
3. **Database Initialization**: 
Ensure MongoDB is installed and running. Use the provided **init-mongo.js** script to initialize the database.  


4. **Env Setup**:
    ```bash
      SECRET_KEY=
      ALGORITHM=HS256
      GOOGLE_CLIENT_ID=
      GOOGLE_CLIENT_SECRET=
      GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      JWT_SECRET_KEY=your_jwt_secret_key
      JWT_ALGORITHM=HS256
      MONGO_USER=
      MONGO_PASSWORD=
      DATABASE_NAME=
      MONGO_URI=mongodb://localhost:27017
  
5. **Docker Setup**:  
Alternatively, you can run the application using Docker. Build and Start the Containers:   
    ```bash
       docker-compose up --build

This will set up both the application and the MongoDB database.
Access the Application: Navigate to http://localhost:8000 in your browser.
