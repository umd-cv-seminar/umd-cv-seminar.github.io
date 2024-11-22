import os
import json
import argparse

# Default directories and filenames
DEFAULT_TEMPLATE = "base.html"
DEFAULT_TEMPLATES_DIR = "templates"
DEFAULT_OUTPUT_DIR = "./"
DEFAULT_CONTENT_DIR = "content"
DEFAULT_SCHEDULE_FILE = "fa2024_schedule.json"
DEFAULT_OUTPUT_FILE = "index.html"

# Utility function to load a template
def load_template(template_path):
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()

# Utility function to save a generated file
def save_output(output_path, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

# Generate the index page
def generate_index(template_path, schedule_path, output_path):
    template = load_template(template_path)
    schedule_data = load_schedule(schedule_path)
    content = template.replace("{{ schedule }}", generate_schedule_html(schedule_data))
    save_output(output_path, content)

# Load schedule data from a JSON file
def load_schedule(schedule_path):
    with open(schedule_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Generate HTML for the schedule
def generate_schedule_html(schedule_data):
    schedule_html = ""

    for date, talks in schedule_data.items():
        # Add the date as a header
        schedule_html += f"""
        <table>
        <tbody> 
        <tr>
            <td colspan="2" class="date"><h3>{date}</h3></td>
        </tr>
        """

        # Process each talk for the date
        for index, talk in enumerate(talks):
            # Assign `left` for single talks or the first of two talks, `split` for the second of two talks
            css_class = "" if len(talks) == 1 or index == 0 else "split"

            # Add optional paper link if it exists
            paper_link_html = f'<br><a href="{talk["paper_link"]}" target="_blank">[Paper]</a>' if "paper_link" in talk else ""

            schedule_html += f"""
            <tr>
                <td class="left {css_class}">
                    <img src="{talk['image']}" class="profile">
                    <a href="{talk['link']}">{talk['name']}</a>
                    <p>{talk['affiliation']}</p>
                </td>
                <td class="{css_class}">
                    <h3 class="title">{talk['title']}</h3>
                    <button type="button" class="collapsible">Click to expand abstract</button>
                    <div class="content">
                        <p><strong>Abstract: </strong>{talk['abstract']}{paper_link_html}</p>
                    </div>
                </td>
            </tr>
            """
        schedule_html += f"""
        </tbody>
        </table> 
        """
    return schedule_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a static site for a seminar schedule.")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="Path to the base template file.")
    parser.add_argument("--templates_dir", default=DEFAULT_TEMPLATES_DIR, help="Path to the templates directory.")
    parser.add_argument("--output_dir", default=DEFAULT_OUTPUT_DIR, help="Directory to save the generated output.")
    parser.add_argument("--content_dir", default=DEFAULT_CONTENT_DIR, help="Directory containing the schedule JSON file.")
    parser.add_argument("--schedule", default=DEFAULT_SCHEDULE_FILE, help="Schedule JSON filename.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="Output HTML filename.")

    args = parser.parse_args()

    # Resolve paths
    template_path = os.path.join(args.templates_dir, args.template)
    schedule_path = os.path.join(args.content_dir, args.schedule)
    output_path = os.path.join(args.output_dir, args.output)

    # Generate the index page
    generate_index(template_path, schedule_path, output_path)
    print(f"Site generated successfully at {output_path}!")
