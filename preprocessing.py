from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTChar

# Function to get the most common item from a dictionary
def get_most_common(data):
    if data:
        return max(data.items(), key=lambda item: item[1]) if data else None
    return None

# Function to process the PDF and get the most common text size across the entire document
def analyze_pdf_for_text_size(pdf_file):
    text_size_data = {}

    with open(pdf_file, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        parser.set_document(doc)

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()

            for element in layout:
                if isinstance(element, LTTextBox):
                    for text_line in element:
                        for character in text_line:
                            if isinstance(character, LTChar):
                                text_size = character.size

                                # Collect text size information
                                if text_size in text_size_data:
                                    text_size_data[text_size] += 1
                                else:
                                    text_size_data[text_size] = 1

    # Get the most common text size across the entire document
    most_common_text_size = get_most_common(text_size_data)
    return most_common_text_size

# Function to filter text based on the most common text size
def filter_pdf_content_by_text_size(pdf_file, most_common_text_size):
    filtered_text = ""

    with open(pdf_file, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        parser.set_document(doc)

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()

            for element in layout:
                if isinstance(element, LTTextBox):
                    for text_line in element:
                        for character in text_line:
                            if isinstance(character, LTChar):
                                text_size = character.size

                                # Only include text that matches the most common text size
                                if text_size == most_common_text_size[0]:
                                    filtered_text += character.get_text()

    return filtered_text

# Function to save the filtered text to a .txt file
def save_filtered_text_to_file(filtered_text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(filtered_text)
