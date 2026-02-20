import React from 'react';
import styles from '../styles/HourlyForecast.module.css';

interface HourlyForecastProps {
  forecasts?: {
    time: string;
    temperature: number;
    humidity: number;
    wind_speed: number;
    precipitation: number;
    radiation: number;
  }[];
}

export default function HourlyForecast({ forecasts }: HourlyForecastProps) {
  if (!forecasts || forecasts.length === 0) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>Hourly Forecast</div>
        <div className={styles.empty}>No forecast data available</div>
      </div>
    );
  }

  const getWeatherIcon = (temp: number, precip: number): string => {
    if (precip > 0.5) return '🌧️';
    if (precip > 0.1) return '🌦️';
    if (temp > 30) return '☀️';
    if (temp > 25) return '⛅';
    if (temp > 20) return '🌤️';
    return '☁️';
  };

  const getTime = (isoString: string): string => {
    try {
      const date = new Date(isoString);
      return date.getHours().toString().padStart(2, '0') + ':00';
    } catch {
      return '--:--';
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>Hourly Forecast</div>
      <div className={styles.scrollContainer}>
        {forecasts.map((forecast, index) => (
          <div key={index} className={styles.hourCard}>
            <div className={styles.time}>{getTime(forecast.time)}</div>
            <div className={styles.icon}>{getWeatherIcon(forecast.temperature, forecast.precipitation)}</div>
            <div className={styles.temp}>{forecast.temperature.toFixed(0)}°</div>
            <div className={styles.details}>
              <span>💧 {forecast.humidity.toFixed(0)}%</span>
              <span>🌧️ {forecast.precipitation.toFixed(1)}mm</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
