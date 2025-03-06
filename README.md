# GPX & FIT Track Visualizer

This Python script processes GPX and FIT (including FIT.GZ) files to extract and visualize GPS coordinates on an interactive map using Folium. It supports multi-threaded processing for faster execution.

Supported file formats:
- .gpx
- .fit
- .fit.gz

## How to use

1. Change the path to the folder in which your GPS tracks are located.
2. Run the script
3. Open the html file.

### Options

1. The color of the tracks is set by default to blue but can be changed to the color of choice: `track_color="red"` 
2. Single-threaded or multi-threaded: by default, the code is set to single-threaded but can be set to multi-threaded in the method call: `multi_threaded=True`
3. The file in which the visualization is stored by default is `tracks_map.html`; this can be changed with: `map_name="your_map_name.html"`


Example
```python
folder_path = "YOUR_FOLDER_PATH"
plot_multiple_tracks(folder_path, track_color="blue", multi_threaded=True, map_name="multi.html")  # Color can be changed
```
