import os
import sys
from preprocessing import analyze_pdf_for_text_size, filter_pdf_content_by_text_size, save_filtered_text_to_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]

    if not os.path.exists(pdf_file):
        print(f"Error: File {pdf_file} not found.")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = f"{base_name}_filtered.txt"

    most_common_text_size = analyze_pdf_for_text_size(pdf_file)

    filtered_content = filter_pdf_content_by_text_size(pdf_file, most_common_text_size)

    save_filtered_text_to_file(filtered_content, output_file)

    print(f"Filtered content saved to {output_file}")

if __name__ == "__main__":
    main()
