import json
from bs4 import BeautifulSoup

# File paths
HTML_FILE = "index_old.html"  # Replace with the path to your HTML file
JSON_FILE = "content/schedule.json"  # Replace with the path to your JSON file

def extract_abstracts_from_html(html_file):
    """Extract abstracts from the HTML file."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    schedule_data = {}

    # Loop through all rows in the table
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 2:  # Ensure there are two cells in the row
            profile_cell = cells[0]
            details_cell = cells[1]

            # Extract the date from the second cell's first <h3> tag
            date = details_cell.find("h3").text.strip() if details_cell.find("h3") else None
            if not date:
                continue  # Skip if no date is found

            # Extract other details
            image = profile_cell.find("img")["src"] if profile_cell.find("img") else ""
            link = profile_cell.find("a")["href"] if profile_cell.find("a") else ""
            name = profile_cell.find("a").text.strip() if profile_cell.find("a") else ""
            affiliation = profile_cell.find("p").text.strip() if profile_cell.find("p") else ""
            title = details_cell.find("h3", class_="title").text.strip() if details_cell.find("h3", class_="title") else ""
            abstract_div = details_cell.find("div", class_="content")
            abstract = abstract_div.find("p").text.strip() if abstract_div and abstract_div.find("p") else ""

            # Ensure the date is a key in the schedule_data dictionary
            if date not in schedule_data:
                schedule_data[date] = []

            # Append the talk details to the date
            schedule_data[date].append({
                "image": image,
                "link": link,
                "name": name,
                "affiliation": affiliation,
                "title": title,
                "abstract": abstract
            })
    
    return schedule_data

def merge_with_existing_json(new_data, json_file):
    """Merge the extracted data with the existing JSON data."""
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    # Merge the data
    for date, talks in new_data.items():
        if date not in existing_data:
            existing_data[date] = talks
        else:
            # Update or add new talks for the same date
            existing_talks = existing_data[date]
            for new_talk in talks:
                # Check if the talk already exists based on title
                if not any(talk["title"] == new_talk["title"] for talk in existing_talks):
                    existing_talks.append(new_talk)
            existing_data[date] = existing_talks

    # Save the merged data back to the JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

    print(f"Data successfully merged into {json_file}")

if __name__ == "__main__":
    # Extract abstracts from HTML
    extracted_data = extract_abstracts_from_html(HTML_FILE)

    # Merge with existing JSON
    merge_with_existing_json(extracted_data, JSON_FILE)
