import os
from unstructured.cleaners.extract import (
    extract_email_address,
    extract_ip_address,
    extract_us_phone_number,
    extract_datetimetz,
    extract_mapi_id,
    extract_ordered_bullets
)
from unstructured.cleaners.core import (
    remove_punctuation, 
    replace_unicode_quotes, 
    clean, 
    group_broken_paragraphs
)

def clean_and_extract_text_file(input_file, output_file):
    """
    Cleans the text content from the input file by removing sensitive information (emails, phone numbers, IPs, etc.)
    and applies additional cleaning such as removing punctuation, bullets, and broken paragraphs.
    The cleaned content is written to the output file.
    """
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    email_addresses = extract_email_address(raw_text)
    if email_addresses:
        print(f"Extracted emails: {email_addresses}")
        for email in email_addresses:
            raw_text = raw_text.replace(email, "") 

    ip_addresses = extract_ip_address(raw_text)
    if ip_addresses:
        print(f"Extracted IP addresses: {ip_addresses}")
        for ip in ip_addresses:
            raw_text = raw_text.replace(ip, "")  

    phone_number = extract_us_phone_number(raw_text)
    if phone_number:
        print(f"Extracted phone number: {phone_number}")
        raw_text = raw_text.replace(phone_number, "")

    mapi_ids = extract_mapi_id(raw_text)
    if mapi_ids:
        print(f"Extracted mapi id: {mapi_ids}")
        for mapi in mapi_ids:
            raw_text = raw_text.replace(mapi, "")  

    bullets = extract_ordered_bullets(raw_text)
    if bullets:
        print(f"Extracted ordered bullets: {bullets}")

    cleaned_text = replace_unicode_quotes(raw_text)

    cleaned_text = clean(
        cleaned_text, 
        bullets=True, 
        extra_whitespace=True, 
        dashes=True, 
        trailing_punctuation=True
    )

    cleaned_text = remove_punctuation(cleaned_text)

    cleaned_text = group_broken_paragraphs(cleaned_text)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Cleaned text has been saved to {output_file}")


if __name__ == "__main__":
    input_file = "temp_filtered.txt"  
    output_file = "output_cleaned.txt"  

    clean_and_extract_text_file(input_file, output_file)
