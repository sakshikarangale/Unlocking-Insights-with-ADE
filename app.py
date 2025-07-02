from flask import Flask, request, render_template, jsonify
import pytesseract
from PIL import Image
import os
from googletrans import Translator
from simplet5 import SimpleT5

app = Flask(__name__)

# Path to the Tesseract executable (change this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

translator = Translator()
model = SimpleT5()
# Load the SimpleT5 model
model.load_model("t5", r"D:\Unlocking Insights With ADE\Scouce code\simplet5-epoch-0-train-loss-1.5692-val-loss-1.3757", use_gpu=False) #Model path can be change as PC path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    try:
        language = request.form.get('language')
        if language == 'English':
            # Below path can be change as PC path
            save_path = r'D:\Unlocking Insights With ADE\Scouce code\English\E.txt'
            extracted_text = pytesseract.image_to_string(Image.open(file))
            with open(save_path, 'w', encoding='utf-8') as extracted_file:
                extracted_file.write(extracted_text)

            summary_save_path = r'D:\Unlocking Insights With ADE\Scouce code\English\su.txt'
            summary = model.predict(extracted_text)

            if isinstance(summary, list):
                summary = ' '.join(summary)

            with open(summary_save_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary)

            return jsonify({'status': 'success',
                            'message': f'File uploaded, text extracted, and summarized for {language}'})

        elif language == 'Marathi':
            #Below path can be change as PC path
            save_path = r'D:\Unlocking Insights With ADE\Scouce code\M.txt'  # Extracted Marathi Text
            translated_save_path = r'D:\Unlocking Insights With ADE\Scouce code\Marathi\e.txt'  # Translated English Text
            summary_save_path = r'D:\Unlocking Insights With ADE\Scouce code\Marathi\s.txt'  # English Summary
            summarized_marathi_text_path = r'D:\Unlocking Insights With ADE\Scouce code\Marathi\m_summarized.txt'  # Summarized Marathi Text (Path Corrected)

            extracted_text = pytesseract.image_to_string(Image.open(file), lang='mar')
            with open(save_path, 'w', encoding='utf-8') as extracted_file:
                extracted_file.write(extracted_text)

            translated_text = translator.translate(extracted_text, src='mr', dest='en').text
            with open(translated_save_path, 'w', encoding='utf-8') as translated_file:
                translated_file.write(translated_text)

            summary = model.predict(translated_text)
            if isinstance(summary, list):
                summary = ' '.join(summary)

            with open(summary_save_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary)

            summarized_marathi_text = translator.translate(summary, src='en', dest='mr').text
            with open(summarized_marathi_text_path, 'w', encoding='utf-8') as summarized_marathi_file:
                summarized_marathi_file.write(summarized_marathi_text)

            return jsonify({'status': 'success',
                            'message': f'File uploaded, text extracted, translated, summarized, and saved for {language}'})
        elif language == 'Hindi':
            # Below path can be change as PC path
            save_path = r'D:\Unlocking Insights With ADE\Scouce code\Hindi\H.txt'  # Extracted Hindi Text
            translated_save_path = r'D:\Unlocking Insights With ADE\Scouce code\Hindi\e.txt'  # Translated English Text
            summary_save_path = r'D:\Unlocking Insights With ADE\Scouce code\Hindi\s.txt'  # English Summary
            summarized_hindi_text_path = r'D:\Unlocking Insights With ADE\Scouce code\Hindi\h_summarized.txt'  # Summarized Hindi Text (Path Corrected)

            extracted_text = pytesseract.image_to_string(Image.open(file), lang='hin')
            with open(save_path, 'w', encoding='utf-8') as extracted_file:
                extracted_file.write(extracted_text)

            translated_text = translator.translate(extracted_text, src='hi', dest='en').text
            with open(translated_save_path, 'w', encoding='utf-8') as translated_file:
                translated_file.write(translated_text)

            summary = model.predict(translated_text)
            if isinstance(summary, list):
                summary = ' '.join(summary)

            with open(summary_save_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary)

            summarized_hindi_text = translator.translate(summary, src='en', dest='hi').text
            with open(summarized_hindi_text_path, 'w', encoding='utf-8') as summarized_hindi_file:
                summarized_hindi_file.write(summarized_hindi_text)

            return jsonify({'status': 'success',
                            'message': f'File uploaded, text extracted, translated, summarized, and saved for {language}'})

        else:
            return jsonify({'status': 'error', 'message': 'Unsupported language'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error processing image: {str(e)}'})
if __name__ == '__main__':
    app.run()  # No debug mode
