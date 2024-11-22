from bs4 import BeautifulSoup
import json

# File paths
HTML_FILE = "pages/fa2023.html"  # Replace with your HTML file name
OUTPUT_JSON = "content/fa2023_schedule.json"  # Replace with your desired JSON file name

def extract_schedule(html_file):
    """Extracts seminar schedule information from the HTML file."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    schedule_data = {}

    # Find all table rows in the schedule table
    rows = soup.find("table").find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 2:  # Ensure there are two cells in the row
            profile_cell = cells[0]
            details_cell = cells[1]

            # Extract the date from the second cell's first <h3> tag
            date = details_cell.find("h3").text.strip()

            # Extract other details
            image = profile_cell.find("img")["src"] if profile_cell.find("img") else ""
            link = profile_cell.find("a")["href"] if profile_cell.find("a") else ""
            name = profile_cell.find("a").text.strip() if profile_cell.find("a") else ""
            affiliation = profile_cell.find("p").text.strip() if profile_cell.find("p") else ""
            title = details_cell.find_all("h3")[1].text.strip() if len(details_cell.find_all("h3")) > 1 else ""
            abstract_tag = details_cell.find("p")
            abstract = abstract_tag.text.strip().replace("Abstract: ", "") if abstract_tag else ""

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

def save_to_json(data, output_file):
    """Saves the extracted data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Extract schedule data
    schedule = extract_schedule(HTML_FILE)
    
    # Save to JSON
    save_to_json(schedule, OUTPUT_JSON)
    print(f"Schedule data has been successfully saved to {OUTPUT_JSON}")
