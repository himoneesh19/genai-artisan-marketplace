# GenAI Artisan Marketplace

A Flask-based web application that empowers artisans to create AI-powered marketing content using Google Cloud Vertex AI. Includes user authentication, content generation for marketing copy and social media, and a dashboard for managing outputs.

## Features

- User registration and authentication
- AI-powered content generation:
  - Marketing copy
  - Social media posts
  - Craft stories
  - Product visual descriptions and images
- Dashboard to view and manage generated content
- SQLite database for data persistence
- Integration with Google Cloud Vertex AI for generative AI capabilities
- Responsive UI built with Bootstrap

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Vertex AI enabled
- Service account credentials with Vertex AI permissions

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/himoneesh19/genai-artisan-marketplace.git
   cd genai-artisan-marketplace
   ```

2. **Create and activate a virtual environment**

   - Windows (PowerShell):

     ```powershell
     python -m venv venv
     & venv\Scripts\Activate.ps1
     ```

   - Windows (Command Prompt):

     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

   - Linux/Mac:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**

   - Store your service account JSON file securely outside the project directory.
   - Set environment variables to point to your credentials and project ID.

   Example for Windows PowerShell:

   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\secure\genAI\credentials\your-service-account.json"
   $env:GOOGLE_CLOUD_PROJECT = "your-google-cloud-project-id"
   ```

   Example for Linux/Mac:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account.json"
   export GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"
   ```

5. **Initialize the database**

   The SQLite database (`artisans.db`) will be created automatically on first run. To apply schema fixes, run:

   ```bash
   python fix_db_add_materials.py
   ```

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Access the application**

   Open your browser and navigate to:

   ```
   http://127.0.0.1:5000
   ```

## Project Structure

The following files and folders are included in the repository:

```
.
├── app.py
├── app.yaml
├── config.py
├── fix_db_add_materials.py
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── start.bat
├── start.ps1
├── TODO.md
├── .gcloudignore
├── .gitignore
├── models/
│   ├── .gitkeep
│   └── database.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   ├── 3cc980d2-073d-405d-9e35-b12e6c432ae4.png
│   │   ├── b62801ed-873e-41cc-a1ac-7e1ca43e47c4.png
│   │   └── fddac8bc-243a-43d1-a4d0-3e93e3b4568d.png
│   └── js/
│       └── scripts.js
├── templates/
│   ├── .gitkeep
│   ├── base.html
│   ├── content_generator.html
│   ├── dashboard.html
│   ├── login.html
│   ├── preview.html
│   └── register.html
└── utils/
    └── ai_helper.py
```

## API Endpoints

- `GET /` - Redirects to login or dashboard based on session
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - User dashboard showing profile and generated content
- `GET/POST /generate_content` - Main form to generate AI-powered content (used by UI dropdown options)
- `POST /api/generate_marketing_copy` - Generate marketing copy (programmatic API access)
- `POST /api/generate_social_media_post` - Generate social media post (programmatic API access)
- `POST /api/generate_craft_story` - Generate craft story (programmatic API access)
- `POST /api/generate_product_visual` - Generate product visual description (programmatic API access)
- `GET/POST /preview/<content_id>` - Preview, edit, approve generated content
- `POST /delete_content/<content_id>` - Delete generated content

## Environment Variables

Create a `.env` file or set environment variables in your system:

```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json
VERTEX_AI_LOCATION=asia-south1
```

## Security Notes

- Never commit service account JSON files or sensitive credentials to version control.
- Store credentials securely outside the project directory.
- Use environment variables for sensitive configuration.
- Regularly rotate service account keys.

## Troubleshooting

### Vertex AI Initialization Issues

- Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account JSON file.
- Verify the service account has Vertex AI permissions.
- Check that the Google Cloud project ID is correct.

### Database Issues

- The app uses SQLite (`artisans.db`) which is created automatically.
- If you encounter database errors, delete `artisans.db` and restart the app.
- Run `fix_db_add_materials.py` to apply schema fixes if needed.

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly.
5. Submit a pull request.

## License

This project is licensed under the MIT License.
