import React from 'react';
import styles from '../styles/CurrentWeather.module.css';

interface CurrentWeatherProps {
  temperature?: number;
  humidity?: number;
  condition?: string;
}

export default function CurrentWeather({ temperature, humidity, condition }: CurrentWeatherProps) {
  const feelsLike = temperature ? (temperature - (humidity ? humidity * 0.05 : 0)).toFixed(1) : '--';
  
  const getCondition = (): string => {
    if (!condition) {
      if (temperature && temperature > 30) return 'Clear';
      if (temperature && temperature > 20) return 'Partly Cloudy';
      return 'Cloudy';
    }
    return condition;
  };

  const getConditionIcon = (): string => {
    const cond = getCondition().toLowerCase();
    if (cond.includes('clear') || cond.includes('sunny')) return '☀️';
    if (cond.includes('cloud') || cond.includes('partly')) return '⛅';
    if (cond.includes('rain') || cond.includes('drizzle')) return '🌧️';
    if (cond.includes('thunder') || cond.includes('storm')) return '⛈️';
    if (cond.includes('snow')) return '❄️';
    if (cond.includes('fog') || cond.includes('mist')) return '🌫️';
    return '🌤️';
  };

  return (
    <div className={styles.currentWeather}>
      <div className={styles.mainInfo}>
        <div className={styles.icon}>{getConditionIcon()}</div>
        <div className={styles.temp}>{temperature !== undefined ? `${temperature.toFixed(0)}°` : '--'}</div>
      </div>
      <div className={styles.condition}>{getCondition()}</div>
      <div className={styles.feelsLike}>
        Feels like <span>{feelsLike}°</span>
      </div>
    </div>
  );
}
