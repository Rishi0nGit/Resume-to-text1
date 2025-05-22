import logging
import azure.functions as func
import io
from pdfminer.high_level import extract_text
import mammoth

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        content = req.get_body()
        filename = req.headers.get('x-filename','').lower()
        ext = filename.rsplit('.',1)[-1]

        if ext == 'pdf':
            text = extract_text(io.BytesIO(content))
        elif ext in ('docx','doc'):
            result = mammoth.extract_raw_text(io.BytesIO(content))
            text = result.value
        else:
            return func.HttpResponse("Unsupported file type", status_code=400)

        return func.HttpResponse(text, mimetype="text/plain")
    except Exception as e:
        logging.exception("Error processing file")
        return func.HttpResponse(f"Error: {e}", status_code=500)
