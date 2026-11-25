from pypdf import PdfReader
from io import BytesIO


def extract_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    try:

        # Read PDF files
        if file_name.endswith(".pdf"):

            pdf = PdfReader(
                BytesIO(uploaded_file.getvalue())
            )

            text = ""

            for page in pdf.pages:
                text += page.extract_text() or ""

            return text

        # Read TXT files
        elif file_name.endswith(".txt"):

            return uploaded_file.getvalue().decode(
                "utf-8",
                errors="replace"
            )

        else:
            return "Unsupported file format."

    except Exception as error:

        return f"Document reading error: {error}"