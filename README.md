# GenAI Artisan Marketplace

A Flask-based web application for artisans to generate AI-powered marketing content using Google Cloud Vertex AI.

## Features

- User registration and authentication
- AI-powered content generation (marketing copy, social media posts, craft stories)
- Dashboard for managing generated content
- SQLite database for data persistence

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Cloud Project with Vertex AI enabled
- Service account credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd genai-artisan-marketplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows (PowerShell):
     ```powershell
     & venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Google Cloud credentials**

   **Important Security Note:** Service account credentials should be stored outside the project directory for security.

   - Move your service account JSON file to a secure location (e.g., `C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json`)
   - Set the environment variable to point to this location:

   **Windows (PowerShell):**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json"
   $env:GOOGLE_CLOUD_PROJECT = "my-project-genai-471504"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS=C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json
   set GOOGLE_CLOUD_PROJECT=my-project-genai-471504
   ```

   **Linux/Mac:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/secure/location/service-account.json"
   export GOOGLE_CLOUD_PROJECT="my-project-genai-471504"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Register a new account or login

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models/
│   └── database.py        # Database models and functions
├── utils/
│   └── ai_helper.py       # Vertex AI integration
├── templates/             # HTML templates
├── static/                # CSS and JavaScript files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints

- `GET /` - Home page (redirects to login/dashboard)
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /dashboard` - User dashboard
- `GET/POST /generate_content` - Content generation form
- `POST /api/generate_marketing_copy` - Generate marketing copy
- `POST /api/generate_social_media_post` - Generate social media post
- `POST /api/generate_craft_story` - Generate craft story
- `POST /api/generate_product_visual` - Generate product visual description

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLOUD_PROJECT=my-project-genai-471504
GOOGLE_APPLICATION_CREDENTIALS=C:\secure\genAI\credentials\my-project-genai-471504-228dc08e66b2.json
VERTEX_AI_LOCATION=asia-south1
```

## Security Notes

- Never commit service account JSON files to version control
- Store credentials in secure locations outside the project directory
- Use environment variables for sensitive configuration
- Regularly rotate service account keys

## Troubleshooting

### Vertex AI Initialization Issues
- Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account JSON file
- Verify the service account has Vertex AI permissions
- Check that the Google Cloud project ID is correct

### Database Issues
- The app uses SQLite (`artisans.db`) which is created automatically
- If you encounter database errors, delete `artisans.db` and restart the app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
