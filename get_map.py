import sys
import osmnx as ox

def get_map(location, save_path, map_type='drive'):
    # get drive map of location
    drive_map = ox.graph_from_place(location, network_type=map_type, simplify=True)

    # save map
    ox.io.save_graphml(drive_map, save_path)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 get_map.py <location> <save_path> <map_type>")
        sys.exit(1)
    
    map_type = sys.argv[3]
    if map_type not in ['drive', 'walk', 'bike']:
        print("map_type must be one of: drive, walk, bike")
        sys.exit(1)

    location = sys.argv[1]
    save_path = sys.argv[2]

    get_map(location, save_path, map_type)


if __name__ == '__main__':
    main()