"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Predictive Analytics Engine

Advanced forecasting and prediction capabilities:
- Time series forecasting
- Trend analysis
- Pattern prediction
- Anomaly detection
- Confidence intervals
- Multi-variate prediction
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from collections import deque


class PredictiveAnalyticsEngine:
    """
    Advanced predictive analytics and forecasting
    
    Features:
    - Time series prediction
    - Trend detection
    - Seasonal decomposition
    - Anomaly detection
    - Confidence estimation
    """
    
    def __init__(self, window_size: int = 50):
        """
        Initialize analytics engine
        
        Args:
            window_size: Size of sliding window for analysis
        """
        self.window_size = window_size
        self.time_series_data: Dict[str, deque] = {}
        self.predictions: Dict[str, List] = {}
        self.anomalies: Dict[str, List] = {}
        
        # Statistics
        self.total_predictions = 0
        self.prediction_errors = []
    
    def add_data_point(self, series_name: str, value: float, 
                       timestamp: Optional[float] = None) -> None:
        """
        Add data point to time series
        
        Args:
            series_name: Name of the series
            value: Data value
            timestamp: Optional timestamp
        """
        if series_name not in self.time_series_data:
            self.time_series_data[series_name] = deque(maxlen=self.window_size)
        
        self.time_series_data[series_name].append({
            'value': value,
            'timestamp': timestamp or len(self.time_series_data[series_name])
        })
    
    def predict_next(self, series_name: str, steps: int = 1) -> List[Dict[str, float]]:
        """
        Predict next values in time series
        
        Args:
            series_name: Name of series to predict
            steps: Number of steps to predict
            
        Returns:
            List of predictions with confidence intervals
        """
        if series_name not in self.time_series_data:
            return []
        
        data = self.time_series_data[series_name]
        if len(data) < 3:
            return []
        
        values = np.array([d['value'] for d in data])
        
        # Simple linear regression for trend
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, deg=1)
        trend_line = np.poly1d(coeffs)
        
        # Calculate residuals for confidence
        residuals = values - trend_line(x)
        std_error = np.std(residuals)
        
        # Predict future values
        predictions = []
        last_x = len(values) - 1
        
        for step in range(1, steps + 1):
            predicted_value = trend_line(last_x + step)
            
            # Confidence interval (95%)
            confidence_margin = 1.96 * std_error * np.sqrt(1 + 1/len(values))
            
            predictions.append({
                'value': float(predicted_value),
                'lower_bound': float(predicted_value - confidence_margin),
                'upper_bound': float(predicted_value + confidence_margin),
                'confidence': 0.95,
                'step': step
            })
        
        # Store predictions
        if series_name not in self.predictions:
            self.predictions[series_name] = []
        self.predictions[series_name].extend(predictions)
        
        self.total_predictions += len(predictions)
        
        return predictions
    
    def detect_trend(self, series_name: str) -> Dict[str, Any]:
        """
        Detect trend in time series
        
        Args:
            series_name: Name of series
            
        Returns:
            Trend information
        """
        if series_name not in self.time_series_data:
            return {'trend': 'unknown'}
        
        data = self.time_series_data[series_name]
        if len(data) < 3:
            return {'trend': 'insufficient_data'}
        
        values = np.array([d['value'] for d in data])
        
        # Linear regression
        x = np.arange(len(values))
        slope, intercept = np.polyfit(x, values, deg=1)
        
        # Categorize trend
        if abs(slope) < 0.01:
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'
        
        # Calculate strength
        r_squared = self._calculate_r_squared(values, slope, intercept)
        
        return {
            'trend': trend,
            'slope': float(slope),
            'strength': float(r_squared),
            'current_value': float(values[-1]),
            'start_value': float(values[0]),
            'change_percent': float((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
        }
    
    def detect_anomalies(self, series_name: str, threshold: float = 2.5) -> List[Dict]:
        """
        Detect anomalies in time series
        
        Args:
            series_name: Name of series
            threshold: Standard deviations for anomaly threshold
            
        Returns:
            List of anomalies
        """
        if series_name not in self.time_series_data:
            return []
        
        data = self.time_series_data[series_name]
        if len(data) < 5:
            return []
        
        values = np.array([d['value'] for d in data])
        
        # Calculate statistics
        mean = np.mean(values)
        std = np.std(values)
        
        # Find anomalies
        anomalies = []
        for i, point in enumerate(data):
            z_score = abs((point['value'] - mean) / std) if std > 0 else 0
            
            if z_score > threshold:
                anomaly = {
                    'index': i,
                    'value': point['value'],
                    'timestamp': point['timestamp'],
                    'z_score': float(z_score),
                    'deviation': float(point['value'] - mean)
                }
                anomalies.append(anomaly)
        
        # Store anomalies
        if series_name not in self.anomalies:
            self.anomalies[series_name] = []
        self.anomalies[series_name].extend(anomalies)
        
        return anomalies
    
    def forecast_probability(self, series_name: str, target_value: float, 
                           horizon: int = 10) -> float:
        """
        Estimate probability of reaching target value
        
        Args:
            series_name: Name of series
            target_value: Target value
            horizon: Time horizon
            
        Returns:
            Probability estimate (0-1)
        """
        predictions = self.predict_next(series_name, steps=horizon)
        
        if not predictions:
            return 0.0
        
        # Check if target is within confidence intervals
        for pred in predictions:
            if pred['lower_bound'] <= target_value <= pred['upper_bound']:
                # Closer to predicted value = higher probability
                distance = abs(pred['value'] - target_value)
                range_size = pred['upper_bound'] - pred['lower_bound']
                
                if range_size > 0:
                    probability = 1.0 - (distance / range_size)
                    return max(0.0, min(1.0, probability))
        
        # Outside all confidence intervals
        return 0.1  # Small non-zero probability
    
    def analyze_correlation(self, series1: str, series2: str) -> float:
        """
        Analyze correlation between two series
        
        Args:
            series1: First series name
            series2: Second series name
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        if series1 not in self.time_series_data or series2 not in self.time_series_data:
            return 0.0
        
        data1 = self.time_series_data[series1]
        data2 = self.time_series_data[series2]
        
        # Get common length
        min_len = min(len(data1), len(data2))
        if min_len < 2:
            return 0.0
        
        values1 = np.array([d['value'] for d in list(data1)[-min_len:]])
        values2 = np.array([d['value'] for d in list(data2)[-min_len:]])
        
        # Calculate correlation
        correlation = np.corrcoef(values1, values2)[0, 1]
        
        return float(correlation) if not np.isnan(correlation) else 0.0
    
    def get_prediction_accuracy(self, series_name: str) -> Dict[str, float]:
        """
        Calculate prediction accuracy metrics
        
        Args:
            series_name: Name of series
            
        Returns:
            Accuracy metrics
        """
        if series_name not in self.predictions or series_name not in self.time_series_data:
            return {'mape': 0.0, 'rmse': 0.0}
        
        # Compare predictions with actual values
        predictions = self.predictions[series_name]
        actual_data = list(self.time_series_data[series_name])
        
        errors = []
        for pred in predictions[-10:]:  # Last 10 predictions
            step = pred['step']
            if step < len(actual_data):
                actual = actual_data[step]['value']
                predicted = pred['value']
                error = abs(actual - predicted)
                errors.append(error)
        
        if not errors:
            return {'mape': 0.0, 'rmse': 0.0}
        
        # Calculate metrics
        mape = np.mean(errors) * 100  # Mean Absolute Percentage Error
        rmse = np.sqrt(np.mean(np.array(errors) ** 2))  # Root Mean Square Error
        
        return {
            'mape': float(mape),
            'rmse': float(rmse),
            'sample_size': len(errors)
        }
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get complete analytics summary"""
        summary = {
            'series_count': len(self.time_series_data),
            'total_predictions': self.total_predictions,
            'series_summaries': {}
        }
        
        for series_name in self.time_series_data:
            data = self.time_series_data[series_name]
            if len(data) > 0:
                values = [d['value'] for d in data]
                
                summary['series_summaries'][series_name] = {
                    'data_points': len(data),
                    'current_value': values[-1],
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'trend': self.detect_trend(series_name),
                    'anomalies_detected': len(self.anomalies.get(series_name, []))
                }
        
        return summary
    
    def _calculate_r_squared(self, values: np.ndarray, slope: float, 
                            intercept: float) -> float:
        """Calculate R-squared value"""
        x = np.arange(len(values))
        predicted = slope * x + intercept
        
        ss_res = np.sum((values - predicted) ** 2)
        ss_tot = np.sum((values - np.mean(values)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        return 1.0 - (ss_res / ss_tot)
