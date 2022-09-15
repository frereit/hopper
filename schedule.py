from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urljoin
import requests

@dataclass(frozen=True, eq=True)
class Movie:
    title: str
    start_time: datetime
    end_time: datetime
    url: str

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')})"

def get_schedule():
    """Return a list of Movie objects."""
    base_url = "https://www.cineplex.de/programm/mannheim/"
    main_soup = BeautifulSoup(requests.get(base_url).text, "html.parser")
    for link in main_soup.find_all("a", class_="filmInfoLink"):
        film_soup = BeautifulSoup(requests.get(urljoin(base_url, link["href"])).text, "html.parser")
        title = link.text
        schedule = film_soup.find("div", class_="schedule")
        try:
            length = int(film_soup.find("li", class_="movie-attributes__duration").text[:-1])
        except AttributeError:
            print(f"Could not find length for {title}, assuming 120 minutes.")
            length = 120
        for performance in schedule.find_all("div", class_="performance-holder"):
            time = performance.find("time", class_="schedule__time").text
            date = performance.find("time", class_="schedule__time").get("datetime")
            start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(minutes=length)
            movie = Movie(title, start_time, end_time, urljoin(base_url, link["href"]))
            yield movie
