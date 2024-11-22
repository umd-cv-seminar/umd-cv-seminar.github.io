import argparse
from bs4 import BeautifulSoup

def process_html(file_path):
    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tags with the 'src' attribute
    for tag in soup.find_all(src=True):
        original_src = tag['src']
        # Prepend "../" to the 'src' attribute
        tag['src'] = "../" + original_src

    # Write the modified HTML back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

def main():
    parser = argparse.ArgumentParser(description="Modify HTML to prepend '../' to all 'src' attributes.")
    parser.add_argument("file_path", help="Path to the HTML file to be processed")

    args = parser.parse_args()

    # Process the HTML file
    process_html(args.file_path)

if __name__ == "__main__":
    main()
