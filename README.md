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
- Content approval workflow: Generated content is saved as 'pending', previewed, edited if needed, and approved before publishing

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

   The SQLite database (`artisans.db`) will be created automatically on first run. The database migration is now automated and will run automatically on app startup, adding any missing columns (e.g., `approval_status`, `include_quote`, `materials`) without manual intervention.

   **Note:** The migration script `fix_db_add_materials.py` is still available for manual execution if needed, but it's no longer required as the process is now automated.

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
├── tests/
│   └── api_test.py
└── utils/
    └── ai_helper.py
```

## API Endpoints

- `GET /` - Redirects to login or dashboard based on session
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - User dashboard showing profile and generated content
- `GET/POST /generate_content` - Form to generate AI-powered content (marketing copy, social media posts, craft stories, product visuals)
- `GET/POST /preview/<content_id>` - Preview, edit, and approve generated content
- `POST /delete_content/<content_id>` - Delete generated content
- `GET /migrate_db` - Run database migration script (alternative to running `fix_db_add_materials.py` directly)
- `POST /api/generate_marketing_copy` - API endpoint for generating marketing copy
- `POST /api/generate_social_media_post` - API endpoint for generating social media posts
- `POST /api/generate_craft_story` - API endpoint for generating craft stories
- `POST /api/generate_product_visual` - API endpoint for generating product visual descriptions

## Environment Variables

Create a `.env` file or set environment variables in your system:

```env
API_KEY=your-secret-key-here
GOOGLE_SERVICE_ACCOUNT_JSON=your-json-service-account-credentials
SECRET_KEY=your-secret-key-here
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
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
