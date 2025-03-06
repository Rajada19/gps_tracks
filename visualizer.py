import os
import gpxpy
import gpxpy.gpx
import folium
import fitparse
import gzip
from concurrent.futures import ProcessPoolExecutor




def read_gpx(file_path):
    """Read GPX file and extracts latitude & longitude points."""
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coordinates = [
        (point.latitude, point.longitude)
        for track in gpx.tracks
        for segment in track.segments
        for point in segment.points
    ]

    return coordinates



def read_fit(file_path):
    """Reads FIT or FIT.GZ file and extracts latitude & longitude points."""
    coordinates = []

    # Read the file content before passing it to fitparse
    if file_path.endswith('.gz'):
        with gzip.open(file_path, 'rb') as f:
            file_content = f.read()
        fit_data = fitparse.FitFile(file_content)
    else:
        fit_data = fitparse.FitFile(file_path)

    latitudes = []
    longitudes = []

    # Parse records for GPS data
    for record in fit_data.get_messages('record'):
        lat = record.get_value('position_lat')
        lon = record.get_value('position_long')

        if lat is not None and lon is not None:
            # Convert FIT degrees-semicircles to decimal degrees
            lat = lat * (180 / 2 ** 31)
            lon = lon * (180 / 2 ** 31)
            latitudes.append(lat)
            longitudes.append(lon)

    # Combine into coordinate pairs
    coordinates = list(zip(latitudes, longitudes))
    return coordinates

def process_file(file):
    """Processes single file (GPX or FIT) and returns the coordinates."""
    if file.lower().endswith('.gpx'):
        return read_gpx(file)
    elif file.lower().endswith(('.fit', '.fit.gz')):
        return read_fit(file)
    else:
        return []


def scan_folder_for_tracks(folder_path):
    """Scans folder for GPX, FIT, and FIT.GZ files and returns a list of file paths."""
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.lower().endswith(('.gpx', '.fit', '.fit.gz'))
    ]



def plot_multiple_tracks(folder_path, map_name="tracks_map.html", track_color="blue", multi_threaded=False):
    """Scans folder, reads all tracks, and plots them on a folium map. Can be set to multi threaded"""
    files = scan_folder_for_tracks(folder_path)

    if not files:
        print("No valid GPX or FIT in the folder.")
        return

    all_coordinates = []

    if multi_threaded:
        print("Multi-threaded mode")
        with ProcessPoolExecutor() as executor:
            results = executor.map(process_file, files)
            all_coordinates.extend(results)
    else:
        print("Single-threaded mode")
        results = map(process_file, files)
        all_coordinates.extend(results)
    # Remove empty lists
    all_coordinates = [coords for coords in all_coordinates if coords]

    if not all_coordinates:
        print("No valid tracks were extracted.")
        return

    # Center map on the first track's start location
    start_location = all_coordinates[0][0]
    my_map = folium.Map(location=start_location, zoom_start=14)

    # Add each track to the map in the same color
    for i, coordinates in enumerate(all_coordinates):
        folium.PolyLine(coordinates, color=track_color, weight=2.5, opacity=1, tooltip=f"Track {i + 1}").add_to(my_map)

    # Save the map
    my_map.save(map_name)
    print(f"Map saved as {map_name}")


if __name__ == "__main__":

### EXAMPLE MULTI-threaded: Uses all cores of the CPU!
#    folder_path = "data"
#    map_name = "tracks_map.html"  #saves the data to this file (.html) needed
#    plot_multiple_tracks(folder_path, track_color="blue", multi_threaded=True, map_name="multi.html")  # Color can be changed

### EXAMPLE SINGLE-threaded:
#    folder_path = "FOLDER_PATH"
#    map_name = "tracks_map.html"  #saves the data to this file (.html) needed
#    plot_multiple_tracks(folder_path, track_color="blue", map_name="multi.html")  # Color can be changed



