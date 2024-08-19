from flask import Flask, request, jsonify
from .database import get_images_from_db

app = Flask(__name__)

@app.route('/api/getImages', methods=['GET'])
def get_images():
    document_name = request.args.get('documentName')
    page_number = request.args.get('pageNumber')
    if not document_name or page_number is None:
        return jsonify({'error': 'Missing parameters'}), 400

    images = get_images_from_db(document_name, page_number)
    return jsonify(images)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
