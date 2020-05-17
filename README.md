# Sentinel2Overlap
Python script to search for Sentinel2 satellite tiles that cover user defined area

### Requirements

| modules | 
| ------ | 
| requests==2.23.0 | 
| geopandas==0.6.1 | 

### Run
```
python sentinel2overlap.py -i "Kharkiv_region.geojson" -o "overlap.geojson" -v
```