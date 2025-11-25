import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { BOGOTA_COORDS, COLORS } from '../utils/constants';
import './MapView.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function MapView({ departments, selectedDepartment }) {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [selectedDeptInfo, setSelectedDeptInfo] = useState(null);

  useEffect(() => {
    fetch('https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_COL_1.json')
      .then(response => response.json())
      .then(data => setGeoJsonData(data))
      .catch(error => console.error('Error loading GeoJSON:', error));
  }, []);

  useEffect(() => {
    if (selectedDepartment && departments) {
      const deptInfo = departments.find(d => d.department === selectedDepartment);
      setSelectedDeptInfo(deptInfo);
    } else {
      setSelectedDeptInfo(null);
    }
  }, [selectedDepartment, departments]);

  const getDepartmentStyle = (feature) => {
    const deptName = feature.properties.NAME_1 || feature.properties.name;
    
    if (deptName === 'Bogotá D.C.' || deptName === 'Bogota, D.C.') {
      return {
        fillColor: COLORS.BOGOTA,
        weight: 1,
        color: '#2C3E50',
        fillOpacity: 0.7
      };
    }
    
    if (selectedDepartment && deptName === selectedDepartment) {
      return {
        fillColor: COLORS.SELECTED,
        weight: 2,
        color: '#2C3E50',
        fillOpacity: 0.7
      };
    }
    
    return {
      fillColor: COLORS.OTHERS,
      weight: 1,
      color: '#2C3E50',
      fillOpacity: 0.5
    };
  };

  const axisLine = {
    color: COLORS.AXIS,
    weight: 2,
    dashArray: '10, 5',
    opacity: 0.7
  };

  return (
    <div className="map-view">
      <MapContainer
        center={BOGOTA_COORDS}
        zoom={6}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {geoJsonData && (
          <GeoJSON 
            data={geoJsonData} 
            style={getDepartmentStyle}
          />
        )}

        <Polyline
          positions={[
            [12, BOGOTA_COORDS[1]],
            [-5, BOGOTA_COORDS[1]]
          ]}
          pathOptions={axisLine}
        />

        <Polyline
          positions={[
            [BOGOTA_COORDS[0], -82],
            [BOGOTA_COORDS[0], -66]
          ]}
          pathOptions={axisLine}
        />

        <Marker position={BOGOTA_COORDS} icon={redIcon}>
          <Popup>
            <strong>Bogotá D.C.</strong><br />
            Latitud: {BOGOTA_COORDS[0]}<br />
            Longitud: {BOGOTA_COORDS[1]}<br />
            (Punto de referencia)
          </Popup>
        </Marker>

        {selectedDeptInfo && (
          <>
            <Polyline
              positions={[
                BOGOTA_COORDS,
                [selectedDeptInfo.lat, selectedDeptInfo.lon]
              ]}
              pathOptions={{
                color: COLORS.LINE,
                weight: 2.5,
                dashArray: '5, 10',
                opacity: 0.7
              }}
            />

            <Marker 
              position={[selectedDeptInfo.lat, selectedDeptInfo.lon]} 
              icon={greenIcon}
            >
              <Popup>
                <div style={{ minWidth: '200px' }}>
                  <strong>{selectedDeptInfo.department}</strong><br />
                  {selectedDeptInfo.capital}<br />
                  <hr style={{ margin: '5px 0' }} />
                  <strong>Coordenadas:</strong><br />
                  Latitud: {selectedDeptInfo.lat.toFixed(4)}°<br />
                  Longitud: {selectedDeptInfo.lon.toFixed(4)}°<br />
                  <hr style={{ margin: '5px 0' }} />
                  <strong>Distancia desde Bogotá D.C.:</strong><br />
                  Norte-Sur: {selectedDeptInfo.km_norte_sur > 0 ? '+' : ''}{selectedDeptInfo.km_norte_sur.toFixed(1)} km
                  {selectedDeptInfo.km_norte_sur > 0 ? ' (Norte)' : ' (Sur)'}<br />
                  Este-Oeste: {selectedDeptInfo.km_este_oeste > 0 ? '+' : ''}{selectedDeptInfo.km_este_oeste.toFixed(1)} km
                  {selectedDeptInfo.km_este_oeste > 0 ? ' (Este)' : ' (Oeste)'}<br />
                  <strong>Distancia Total: {selectedDeptInfo.distancia_total.toFixed(1)} km</strong>
                </div>
              </Popup>
            </Marker>
          </>
        )}
      </MapContainer>
    </div>
  );
}

export default MapView;
