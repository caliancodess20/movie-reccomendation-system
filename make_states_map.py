import geopandas as gpd

districts = gpd.read_file("india_states.geojson")

states = districts.dissolve(by="st_nm").reset_index()
states = states[["st_nm", "geometry"]]
states["geometry"] = states["geometry"].simplify(0.02)

states.to_file("india_states_merged.geojson", driver="GeoJSON")
print(len(states), "states saved")