from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTChar

# Function to check if a font is bold based on the font name
def is_bold(font_name):
    return 'Bold' in font_name

# Function to check if a font is italic based on the font name
def is_italic(font_name):
    return 'Italic' in font_name or 'Oblique' in font_name

# Function to get the most and second most common items from a dictionary
def get_most_and_second_most_common(data):
    if data:
        sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
        most_common = sorted_data[0] if sorted_data else None
        second_most_common = sorted_data[1] if len(sorted_data) > 1 else None
        return most_common, second_most_common
    return None, None

# Function to process the PDF and get the most and second most common font/size for each category
def analyze_pdf(pdf_file):
    font_data = {'default': {}, 'bold': {}, 'italic': {}}
    text_size_data = {'default': {}, 'bold': {}, 'italic': {}}

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
                                font = character.fontname
                                text_size = character.size

                                if is_bold(font):
                                    font_type = 'bold'
                                elif is_italic(font):
                                    font_type = 'italic'
                                else:
                                    font_type = 'default'

                                if font in font_data[font_type]:
                                    font_data[font_type][font] += 1
                                else:
                                    font_data[font_type][font] = 1

                                if text_size in text_size_data[font_type]:
                                    text_size_data[font_type][text_size] += 1
                                else:
                                    text_size_data[font_type][text_size] = 1

    most_common_default_font, second_most_common_default_font = get_most_and_second_most_common(font_data['default'])
    most_common_bold_font, second_most_common_bold_font = get_most_and_second_most_common(font_data['bold'])
    most_common_italic_font, second_most_common_italic_font = get_most_and_second_most_common(font_data['italic'])

    most_common_default_size, second_most_common_default_size = get_most_and_second_most_common(text_size_data['default'])
    most_common_bold_size, second_most_common_bold_size = get_most_and_second_most_common(text_size_data['bold'])
    most_common_italic_size, second_most_common_italic_size = get_most_and_second_most_common(text_size_data['italic'])

    return {
        'default': {
            'font': most_common_default_font,
            'size': most_common_default_size
        },
        'bold': {
            'font': most_common_bold_font,
            'size': most_common_bold_size
        },
        'italic': {
            'most_common': {
                'font': most_common_italic_font,
                'size': most_common_italic_size
            },
            'second_most_common': {
                'font': second_most_common_italic_font,
                'size': second_most_common_italic_size
            }
        }
    }

# Function to filter text based on the most common fonts and sizes and retain second most common italic text
def filter_pdf_content(pdf_file, common_fonts_sizes):
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
                                font = character.fontname
                                text_size = character.size

                                font_type = None
                                if is_bold(font):
                                    font_type = 'bold'
                                elif is_italic(font):
                                    font_type = 'italic'
                                else:
                                    font_type = 'default'

                                if font_type == 'default' and font == common_fonts_sizes['default']['font'][0] and text_size == common_fonts_sizes['default']['size'][0]:
                                    filtered_text += character.get_text()
                                elif font_type == 'bold' and font == common_fonts_sizes['bold']['font'][0] and text_size == common_fonts_sizes['bold']['size'][0]:
                                    filtered_text += character.get_text()
                                elif (font_type == 'italic' 
                                      and common_fonts_sizes['italic']['second_most_common']['font'] is not None
                                      and font == common_fonts_sizes['italic']['second_most_common']['font'][0]
                                      and text_size == common_fonts_sizes['italic']['second_most_common']['size'][0]):
                                    filtered_text += character.get_text()

    return filtered_text

pdf_file = "temp.pdf"

common_fonts_sizes = analyze_pdf(pdf_file)

filtered_content = filter_pdf_content(pdf_file, common_fonts_sizes)

print(filtered_content)
