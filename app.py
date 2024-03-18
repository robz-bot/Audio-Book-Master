from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Audiobook model
class Audiobook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    audio_content = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "audio_content": self.audio_content
        }

@app.route('/api/audiobooks')
def get_audiobooks():
    audiobooks = Audiobook.query.all()
    return jsonify([audiobook.to_dict() for audiobook in audiobooks])

@app.route('/api/add_audiobook', methods=['POST'])
def add_audiobook():
    try:
        data = request.get_json()

        # Validate required fields
        if 'title' not in data or 'author' not in data or 'audioUrl' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new audiobook instance
        new_audiobook = Audiobook(title=data['title'], author=data['author'], audio_content=data['audioUrl'])

        # Add the new audiobook to the database
        db.session.add(new_audiobook)
        db.session.commit()

        return jsonify({"message": "Audiobook added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete_audiobook/<int:audiobook_id>', methods=['DELETE'])
def delete_audiobook(audiobook_id):
    try:
        audiobook = Audiobook.query.get(audiobook_id)
        if audiobook:
            db.session.delete(audiobook)
            db.session.commit()
            return jsonify({"message": "Audiobook deleted successfully"}), 200
        else:
            return jsonify({"error": "Audiobook not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
