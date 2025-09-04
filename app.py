from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import os
from config import config
from models.database import get_db, close_connection, init_db, query_db, insert_db
from utils.ai_helper import initialize_vertex_ai, generate_marketing_copy, generate_social_media_post, generate_craft_story, generate_product_visual_description, generate_image

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize database
with app.app_context():
    init_db()

# Initialize Vertex AI (requires credentials)
try:
    initialize_vertex_ai()
except Exception as e:
    print(f"Vertex AI initialization failed: {e}")

@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form.get('full_name')
        craft_type = request.form.get('craft_type')
        location = request.form.get('location')
        bio = request.form.get('bio')

        # Check if user exists
        existing_user = query_db('SELECT id FROM artisans WHERE username = ? OR email = ?', [username, email], one=True)
        if existing_user:
            flash('Username or email already exists')
            return redirect(url_for('register'))

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user
        user_id = insert_db('INSERT INTO artisans (username, email, password_hash, full_name, craft_type, location, bio) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           [username, email, password_hash, full_name, craft_type, location, bio])

        session['user_id'] = user_id
        flash('Registration successful!')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query_db('SELECT * FROM artisans WHERE username = ?', [username], one=True)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = query_db('SELECT * FROM artisans WHERE id = ?', [session['user_id']], one=True)
    products = query_db('SELECT * FROM products WHERE artisan_id = ?', [session['user_id']])
    generated_content = query_db('SELECT * FROM generated_content WHERE artisan_id = ?', [session['user_id']])

    return render_template('dashboard.html', user=user, products=products, generated_content=generated_content)

from flask import jsonify

@app.route('/api/generate_marketing_copy', methods=['POST'])
def api_generate_marketing_copy():
    data = request.form
    craft_type = data.get('craft_type')
    description = data.get('description')
    if not craft_type or not description:
        return jsonify({'error': 'Missing craft_type or description'}), 400
    prompt = f"Generate marketing copy for {craft_type} with description: {description}"
    generated = generate_marketing_copy(prompt)
    return jsonify({'marketing_copy': generated})

@app.route('/api/generate_social_media_post', methods=['POST'])
def api_generate_social_media_post():
    data = request.form
    craft_type = data.get('craft_type')
    description = data.get('description')
    platform = data.get('platform', 'Instagram')
    if not craft_type or not description:
        return jsonify({'error': 'Missing craft_type or description'}), 400
    prompt = f"Generate a social media post for {craft_type} on {platform} with description: {description}"
    generated = generate_social_media_post(prompt, platform)
    return jsonify({'social_media_post': generated})

@app.route('/api/generate_craft_story', methods=['POST'])
def api_generate_craft_story():
    data = request.form
    craft_type = data.get('craft_type')
    description = data.get('description')
    if not craft_type or not description:
        return jsonify({'error': 'Missing craft_type or description'}), 400
    craft_description = f"{craft_type} with description: {description}"
    generated = generate_craft_story(craft_description)
    return jsonify({'craft_story': generated})

@app.route('/api/generate_product_visual', methods=['POST'])
def api_generate_product_visual():
    data = request.form
    craft_type = data.get('craft_type')
    description = data.get('description')
    if not craft_type or not description:
        return jsonify({'error': 'Missing craft_type or description'}), 400
    product_name = f"{craft_type} product"
    generated = generate_product_visual_description(product_name, craft_type)
    return jsonify({'product_visual_description': generated})

# Keep the existing generate_content route for UI usage
@app.route('/generate_content', methods=['GET', 'POST'])
def generate_content():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content_type = request.form['content_type']
        prompt = request.form['prompt']

        if content_type == 'marketing_copy':
            generated = generate_marketing_copy(prompt)
        elif content_type == 'social_post':
            platform = request.form.get('platform', 'Instagram')
            generated = generate_social_media_post(prompt, platform)
        elif content_type == 'craft_story':
            user = query_db('SELECT * FROM artisans WHERE id = ?', [session['user_id']], one=True)
            generated = generate_craft_story(user['bio'], user['craft_type'])
        elif content_type == 'image':
            generated = generate_image(prompt)
        else:
            generated = "Invalid content type"

        # Save to database
        insert_db('INSERT INTO generated_content (artisan_id, content_type, prompt, generated_text, generated_image_url) VALUES (?, ?, ?, ?, ?)',
                 [session['user_id'], content_type, prompt, generated if isinstance(generated, str) else None, generated if not isinstance(generated, str) else None])

        flash('Content generated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('content_generator.html')

if __name__ == '__main__':
    app.run(debug=True)
