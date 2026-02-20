import React from 'react';
import styles from '../styles/LocationCard.module.css';

interface LocationCardProps {
  deviceId?: string;
  lat?: number;
  lon?: number;
}

export default function LocationCard({ deviceId, lat, lon }: LocationCardProps) {
  const getLocationName = (): string => {
    if (lat && lon) {
      if (lat >= 19.5 && lat <= 20.5 && lon >= 75 && lon <= 76) {
        return 'Chhatrapati Sambhajinagar, Maharashtra';
      }
      if (lat >= 12.5 && lat <= 13.5 && lon >= 77 && lon <= 78) {
        return 'Bangalore, Karnataka';
      }
      if (lat >= 19.0 && lat <= 19.5 && lon >= 72.5 && lon <= 73.5) {
        return 'Mumbai, Maharashtra';
      }
      if (lat >= 28.5 && lat <= 29 && lon >= 77 && lon <= 78) {
        return 'Delhi';
      }
    }
    return 'Unknown Location';
  };

  const getCountry = (): string => {
    return 'India';
  };

  return (
    <div className={styles.locationCard}>
      <div className={styles.icon}>📍</div>
      <div className={styles.info}>
        <div className={styles.name}>{getLocationName()}</div>
        <div className={styles.country}>{getCountry()}</div>
        {lat && lon && (
          <div className={styles.coords}>
            {lat.toFixed(4)}°N, {lon.toFixed(4)}°E
          </div>
        )}
      </div>
      {deviceId && (
        <div className={styles.deviceBadge}>
          <span className={styles.deviceIcon}>📡</span>
          {deviceId}
        </div>
      )}
    </div>
  );
}
