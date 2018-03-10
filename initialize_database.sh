#!/bin/bash

sudo -u postgres createdb nyc-taxi-data

sudo -u postgres psql nyc-taxi-data -f create_nyc_taxi_schema.sql

sudo -u postgres shp2pgsql -s 2263:4326 taxi_zones/taxi_zones.shp | sudo -u postgres psql -d nyc-taxi-data
sudo -u postgres psql nyc-taxi-data -c "CREATE INDEX index_taxi_zones_on_geom ON taxi_zones USING gist (geom);"
sudo -u postgres psql nyc-taxi-data -c "CREATE INDEX index_taxi_zones_on_locationid ON taxi_zones (locationid);"
sudo -u postgres psql nyc-taxi-data -c "VACUUM ANALYZE taxi_zones;"

sudo -u postgres shp2pgsql -s 2263:4326 nyct2010_15b/nyct2010.shp | sudo -u postgres psql -d nyc-taxi-data
sudo -u postgres psql nyc-taxi-data -f add_newark_airport.sql
sudo -u postgres psql nyc-taxi-data -c "CREATE INDEX index_nyct_on_geom ON nyct2010 USING gist (geom);"
sudo -u postgres psql nyc-taxi-data -c "CREATE INDEX index_nyct_on_ntacode ON nyct2010 (ntacode);"
sudo -u postgres psql nyc-taxi-data -c "VACUUM ANALYZE nyct2010;"

sudo -u postgres psql nyc-taxi-data -f add_tract_to_zone_mapping.sql

cat ./data/fhv_bases.csv | sudo -u postgres psql nyc-taxi-data -c "COPY fhv_bases FROM stdin WITH CSV HEADER;"
cat ./data/central_park_weather.csv | sudo -u postgres psql nyc-taxi-data -c "COPY central_park_weather_observations FROM stdin WITH CSV HEADER;"
sudo -u postgres psql nyc-taxi-data -c "UPDATE central_park_weather_observations SET average_wind_speed = NULL WHERE average_wind_speed = -9999;"
