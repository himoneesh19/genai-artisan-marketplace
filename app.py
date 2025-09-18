from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import os
import markdown
from config import config
from models.database import get_db, close_connection, init_db, query_db, insert_db
from utils.ai_helper import initialize_vertex_ai, generate_text, generate_marketing_copy, generate_social_media_post, generate_craft_story, generate_product_visual_description, generate_image

app = Flask(__name__)
app.config.from_object(config['development'])

# Add markdown filter
@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

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
        materials = request.form.get('materials')

        # Check if user exists
        existing_user = query_db('SELECT id FROM artisans WHERE username = ? OR email = ?', [username, email], one=True)
        if existing_user:
            flash('Username or email already exists')
            return redirect(url_for('register'))

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user
        user_id = insert_db('INSERT INTO artisans (username, email, password_hash, full_name, craft_type, location, bio, materials) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           [username, email, password_hash, full_name, craft_type, location, bio, materials])

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
    generated_content = query_db('SELECT * FROM generated_content WHERE artisan_id = ? AND approval_status = ?', [session['user_id'], 'approved'])

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
@app.route('/delete_content/<int:content_id>', methods=['POST'])
def delete_content(content_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Check if the content belongs to the user
    content = query_db('SELECT * FROM generated_content WHERE id = ? AND artisan_id = ?', [content_id, session['user_id']], one=True)
    if not content:
        flash('Content not found or access denied')
        return redirect(url_for('dashboard'))

    # Delete the content
    db = get_db()
    db.execute('DELETE FROM generated_content WHERE id = ?', [content_id])
    db.commit()

    flash('Content deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/preview/<int:content_id>', methods=['GET', 'POST'])
def preview_content(content_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    content = query_db('SELECT * FROM generated_content WHERE id = ? AND artisan_id = ?', [content_id, session['user_id']], one=True)
    if not content:
        flash('Content not found')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'approve':
            # Update status to approved
            db = get_db()
            db.execute('UPDATE generated_content SET approval_status = ? WHERE id = ?', ['approved', content_id])
            db.commit()
            flash('Content approved and published!')
            return redirect(url_for('dashboard'))
        elif action == 'edit':
            # Update the content
            new_text = request.form.get('generated_text')
            db = get_db()
            db.execute('UPDATE generated_content SET generated_text = ? WHERE id = ?', [new_text, content_id])
            db.commit()
            flash('Content updated!')
            # Reload content
            content = query_db('SELECT * FROM generated_content WHERE id = ?', [content_id], one=True)

    return render_template('preview.html', content=content)

@app.route('/generate_content', methods=['GET', 'POST'])
def generate_content():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        generate_as = request.form['generate_as']
        tone = request.form.get('tone', 'friendly')
        language = request.form.get('language', 'english')
        include_quote = 'include_quote' in request.form
        prompt = request.form['prompt']

        user = query_db('SELECT * FROM artisans WHERE id = ?', [session['user_id']], one=True)

        # Build base prompt with user data
        base_info = f"Artisan: {user['full_name']}, Craft: {user['craft_type']}, Location: {user['location']}, Bio: {user['bio']}, Materials: {user['materials'] or ''}"

        # Determine person
        if 'first_person' in generate_as:
            person = "first-person"
        else:
            person = "third-person"

        # Build full prompt
        full_prompt = f"Generate content as {person} in {language} language with a {tone} tone. {base_info}. Additional details: {prompt}"
        if include_quote:
            full_prompt += " Include a personal quote from the artisan."

        # Map generate_as to content_type
        content_type_map = {
            'artisan_first_person': 'artisan_first_person',
            'product_listing_third_person': 'product_listing',
            'social_caption': 'social_caption',
            'ad_copy': 'ad_copy',
            'about_press': 'about_press',
            'image': 'image'
        }
        content_type = content_type_map.get(generate_as, 'unknown')

        if generate_as == 'image':
            try:
                generated = generate_image(full_prompt)
                generated_text = None
                generated_image_url = url_for('static', filename=f'images/{generated}')
            except Exception as e:
                flash(str(e))
                return redirect(url_for('generate_content'))
        else:
            # Use appropriate generation function
            if generate_as == 'ad_copy':
                generated = generate_marketing_copy(full_prompt)
            elif generate_as == 'social_caption':
                generated = generate_social_media_post(full_prompt, 'Instagram')  # Default platform
            elif generate_as == 'about_press':
                generated = generate_craft_story(full_prompt)
            else:
                generated = generate_text(full_prompt)  # For others
            generated_text = generated
            generated_image_url = None

        # Save to database as pending
        content_id = insert_db('INSERT INTO generated_content (artisan_id, content_type, prompt, generated_text, generated_image_url, approval_status, include_quote) VALUES (?, ?, ?, ?, ?, ?, ?)',
                               [session['user_id'], content_type, prompt, generated_text, generated_image_url, 'pending', int(include_quote)])

        return redirect(url_for('preview_content', content_id=content_id))

    return render_template('content_generator.html')

@app.route('/migrate_db')
def migrate_db():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        import subprocess
        result = subprocess.run(['python', 'fix_db_add_materials.py'], capture_output=True, text=True)
        if result.returncode == 0:
            flash('Database migration completed successfully!')
            return 'Migration successful: ' + result.stdout
        else:
            flash('Migration failed!')
            return 'Migration failed: ' + result.stderr
    except Exception as e:
        flash('Migration error!')
        return f'Migration error: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
