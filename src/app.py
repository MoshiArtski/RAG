from flask import Flask, render_template, request, jsonify
from src.langchain.summarizer import summarize_profile

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        name = request.json.get('name')
        if not name:
            app.logger.error("No name provided in the request.")
            return jsonify({'error': 'Name is required'}), 400

        app.logger.info(f"Name received: {name}")

        # Call to the actual summarization function
        summary, facts = summarize_profile(name)  # Make sure this function is working correctly

        return jsonify({
            'summary': summary,
            'interesting_fact_1': facts[0],
            'interesting_fact_2': facts[1]
        })
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'An internal error occurred.'}), 500


if __name__ == "__main__":
    app.run(debug=True)