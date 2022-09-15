from datetime import timedelta
from schedule import get_schedule
import networkx as nx

def main():
    date = input("What date do you want (YYYY-MM-DD)? ")
    max_overlap_duration = int(input("How many minutes of the beginning of a movie do you want to miss at most? "))
    max_time_between_movies = int(input("How many minutes do you want to have between movies at most? "))
    starting_time = input("What time do you want to start the earliest? (Optional) ")
    plausible_movies = []
    for movie in get_schedule():
        if movie.start_time.strftime("%Y-%m-%d") == date:
            if starting_time != "" and movie.start_time.strftime("%H:%M") < starting_time:
                continue
            plausible_movies.append(movie)
    print(f"Found {len(plausible_movies)} performances on {date}.")

    # Build a graph of movies to watch
    G = nx.DiGraph()
    for movie in plausible_movies:
        G.add_node(movie)
    for movie in plausible_movies:
        for other_movie in plausible_movies:
            if movie == other_movie:
                continue
            if movie.end_time + timedelta(minutes=max_time_between_movies) < other_movie.start_time:
                continue
            if movie.end_time - other_movie.start_time > timedelta(minutes=max_overlap_duration):
                continue
            if movie.end_time >= other_movie.end_time:
                continue
            G.add_edge(movie, other_movie)

    longest_path = nx.dag_longest_path(G)
    print(f"Found {len(longest_path)} movies to watch.")
    for movie in longest_path:
        print(movie)

if __name__ == "__main__":
    main()