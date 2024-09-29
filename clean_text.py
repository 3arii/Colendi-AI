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
    clean_non_ascii_chars, 
    replace_unicode_quotes, 
    clean, 
    group_broken_paragraphs
)

def clean_and_extract_text_file(input_file, output_file):
    """
    Cleans the text content from the input file by removing sensitive information (emails, phone numbers, IPs, etc.)
    and applies additional cleaning such as removing non-ASCII characters, punctuation, bullets, and broken paragraphs.
    The cleaned content is written to the output file.
    """
    # Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    # Read the content from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Step 1: Extract and remove email addresses
    email_addresses = extract_email_address(raw_text)
    if email_addresses:
        print(f"Extracted emails: {email_addresses}")
        for email in email_addresses:
            raw_text = raw_text.replace(email, "")  # Remove email addresses

    # Step 2: Extract and remove IP addresses
    ip_addresses = extract_ip_address(raw_text)
    if ip_addresses:
        print(f"Extracted IP addresses: {ip_addresses}")
        for ip in ip_addresses:
            raw_text = raw_text.replace(ip, "")  # Remove IP addresses

    # Step 3: Extract and remove phone numbers
    phone_number = extract_us_phone_number(raw_text)
    if phone_number:
        print(f"Extracted phone number: {phone_number}")
        raw_text = raw_text.replace(phone_number, "")  # Remove phone numbers

    # Step 4: Extract and remove mapi id (common in email headers)
    mapi_ids = extract_mapi_id(raw_text)
    if mapi_ids:
        print(f"Extracted mapi id: {mapi_ids}")
        for mapi in mapi_ids:
            raw_text = raw_text.replace(mapi, "")  # Remove MAPI IDs

    # Step 5: Extract ordered bullets (optional)
    bullets = extract_ordered_bullets(raw_text)
    if bullets:
        print(f"Extracted ordered bullets: {bullets}")

    # Step 6: Clean non-ASCII characters
    cleaned_text = clean_non_ascii_chars(raw_text)

    # Step 7: Replace Unicode quotes
    cleaned_text = replace_unicode_quotes(cleaned_text)

    # Step 8: Clean bullets, extra whitespace, dashes, and trailing punctuation
    cleaned_text = clean(
        cleaned_text, 
        bullets=True, 
        extra_whitespace=True, 
        dashes=True, 
        trailing_punctuation=True
    )

    # Step 9: Remove punctuation
    cleaned_text = remove_punctuation(cleaned_text)

    # Step 10: Group broken paragraphs
    cleaned_text = group_broken_paragraphs(cleaned_text)

    # Write the cleaned text to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Cleaned text has been saved to {output_file}")


if __name__ == "__main__":
    input_file = "temp_filtered.txt"  # Replace this with the path to your input text file
    output_file = "output_cleaned.txt"  # Replace this with the path to your output text file

    # Clean the text file and remove sensitive information
    clean_and_extract_text_file(input_file, output_file)
