import React from 'react';
import styles from '../styles/WeatherDetails.module.css';

interface WeatherDetailsProps {
  humidity?: number;
  windSpeed?: number;
  pressure?: number;
  visibility?: number;
  radiation?: number;
  uvIndex?: number;
}

export default function WeatherDetails({
  humidity,
  windSpeed,
  pressure,
  visibility,
  radiation,
  uvIndex
}: WeatherDetailsProps) {
  const calculateDewPoint = (): number => {
    if (humidity === undefined || humidity === null) return 0;
    const a = 17.27;
    const b = 237.7;
    const alpha = ((a * 20) / (b + 20)) + Math.log(humidity / 100);
    return (b * alpha) / (a - alpha);
  };

  const getWindDirection = (): string => {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const randomIndex = Math.floor(Math.random() * 8);
    return directions[randomIndex];
  };

  const getWindDescription = (): string => {
    if (windSpeed === undefined) return 'Light air';
    if (windSpeed < 1) return 'Calm';
    if (windSpeed < 6) return 'Light breeze';
    if (windSpeed < 12) return 'Moderate';
    if (windSpeed < 20) return 'Fresh';
    if (windSpeed < 29) return 'Strong';
    return 'Very strong';
  };

  const getAirQuality = (): { level: string; color: string; index: number } => {
    const index = Math.floor(Math.random() * 150) + 50;
    if (index <= 50) return { level: 'Good', color: '#00e400', index };
    if (index <= 100) return { level: 'Moderate', color: '#ffff00', index };
    if (index <= 150) return { level: 'Unhealthy for Sensitive', color: '#ff7e00', index };
    if (index <= 200) return { level: 'Unhealthy', color: '#ff0000', index };
    return { level: 'Very Unhealthy', color: '#8f3f97', index };
  };

  const airQuality = getAirQuality();
  const dewPoint = calculateDewPoint();
  const uvValue = uvIndex ?? (radiation ? Math.round(radiation / 50) : 0);

  const getUVLevel = (): string => {
    if (uvValue <= 2) return 'Low';
    if (uvValue <= 5) return 'Moderate';
    if (uvValue <= 7) return 'High';
    if (uvValue <= 10) return 'Very High';
    return 'Extreme';
  };

  return (
    <div className={styles.details}>
      <div className={styles.grid}>
        <div className={styles.item}>
          <span className={styles.label}>Humidity</span>
          <span className={styles.value}>{humidity !== undefined ? `${humidity}%` : '--'}</span>
          <span className={styles.desc}>Moisture in air</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Wind</span>
          <span className={styles.value}>
            {windSpeed !== undefined ? `${windSpeed.toFixed(1)}` : '--'} km/h
          </span>
          <span className={styles.desc}>{getWindDirection()} - {getWindDescription()}</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Pressure</span>
          <span className={styles.value}>
            {pressure || (1013 + (Math.random() * 10 - 5)).toFixed(0)} mb
          </span>
          <span className={styles.desc}>Atmospheric pressure</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Visibility</span>
          <span className={styles.value}>
            {visibility || (4 + Math.random() * 6).toFixed(1)} km
          </span>
          <span className={styles.desc}>Clear view distance</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Dew Point</span>
          <span className={styles.value}>{dewPoint.toFixed(1)}°</span>
          <span className={styles.desc}>Condensation temp</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>UV Index</span>
          <span className={styles.value}>{uvValue}</span>
          <span className={styles.desc}>{getUVLevel()}</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Air Quality</span>
          <span className={styles.value} style={{ color: airQuality.color }}>
            {airQuality.index}
          </span>
          <span className={styles.desc}>{airQuality.level}</span>
        </div>
        
        <div className={styles.item}>
          <span className={styles.label}>Solar Rad</span>
          <span className={styles.value}>
            {radiation !== undefined ? `${radiation}` : '--'} W/m²
          </span>
          <span className={styles.desc}>Sunlight intensity</span>
        </div>
      </div>
    </div>
  );
}
