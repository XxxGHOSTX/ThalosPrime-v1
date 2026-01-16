"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Tests for Advanced AI Modules
"""

import pytest
import numpy as np
from ai.optimization.neural_optimizer import NeuralPathwayOptimizer, AdaptiveLearningOptimizer
from ai.optimization.predictive_analytics import PredictiveAnalyticsEngine
from ai.reasoning.advanced_reasoning import AdvancedReasoningEngine


class TestNeuralOptimizer:
    """Test neural pathway optimizer"""
    
    def test_optimizer_creation(self):
        """Test optimizer initialization"""
        optimizer = NeuralPathwayOptimizer()
        assert optimizer.learning_rate == 0.01
        assert optimizer.prune_threshold == 0.1
    
    def test_pathway_statistics(self):
        """Test pathway statistics"""
        optimizer = NeuralPathwayOptimizer()
        stats = optimizer.get_pathway_statistics()
        assert 'total_pathways' in stats
        assert stats['total_pathways'] == 0


class TestPredictiveAnalytics:
    """Test predictive analytics engine"""
    
    def test_analytics_creation(self):
        """Test analytics initialization"""
        analytics = PredictiveAnalyticsEngine(window_size=10)
        assert analytics.window_size == 10
    
    def test_add_data_point(self):
        """Test adding data points"""
        analytics = PredictiveAnalyticsEngine()
        analytics.add_data_point("temperature", 72.5)
        analytics.add_data_point("temperature", 73.0)
        assert "temperature" in analytics.time_series_data
        assert len(analytics.time_series_data["temperature"]) == 2
    
    def test_prediction(self):
        """Test time series prediction"""
        analytics = PredictiveAnalyticsEngine()
        
        # Add some data points
        for i in range(10):
            analytics.add_data_point("test", float(i))
        
        # Predict next values
        predictions = analytics.predict_next("test", steps=3)
        assert len(predictions) == 3
        assert all('value' in p for p in predictions)
        assert all('confidence' in p for p in predictions)
    
    def test_trend_detection(self):
        """Test trend detection"""
        analytics = PredictiveAnalyticsEngine()
        
        # Create increasing trend
        for i in range(10):
            analytics.add_data_point("increasing", float(i))
        
        trend = analytics.detect_trend("increasing")
        assert trend['trend'] == 'increasing'
        assert trend['slope'] > 0
    
    def test_anomaly_detection(self):
        """Test anomaly detection"""
        analytics = PredictiveAnalyticsEngine()
        
        # Normal data
        for i in range(20):
            analytics.add_data_point("test", 50.0 + np.random.normal(0, 1))
        
        # Add anomaly
        analytics.add_data_point("test", 100.0)
        
        anomalies = analytics.detect_anomalies("test", threshold=2.0)
        assert len(anomalies) > 0
    
    def test_forecast_probability(self):
        """Test probability forecasting"""
        analytics = PredictiveAnalyticsEngine()
        
        for i in range(10):
            analytics.add_data_point("test", float(i))
        
        prob = analytics.forecast_probability("test", target_value=15.0, horizon=10)
        assert 0.0 <= prob <= 1.0
    
    def test_analytics_summary(self):
        """Test analytics summary"""
        analytics = PredictiveAnalyticsEngine()
        
        for i in range(5):
            analytics.add_data_point("test", float(i))
        
        summary = analytics.get_analytics_summary()
        assert 'series_count' in summary
        assert 'series_summaries' in summary
        assert summary['series_count'] == 1


class TestReasoningEngine:
    """Test advanced reasoning engine"""
    
    def test_reasoning_creation(self):
        """Test reasoning engine initialization"""
        reasoning = AdvancedReasoningEngine()
        assert len(reasoning.facts) == 0
        assert len(reasoning.rules) == 0
    
    def test_add_facts(self):
        """Test adding facts"""
        reasoning = AdvancedReasoningEngine()
        reasoning.add_fact("sky is blue")
        reasoning.add_fact("grass is green")
        assert len(reasoning.facts) == 2
        assert "sky is blue" in reasoning.facts
    
    def test_add_rules(self):
        """Test adding inference rules"""
        reasoning = AdvancedReasoningEngine()
        reasoning.add_rule(
            conditions=["it is raining"],
            conclusion="ground is wet"
        )
        assert len(reasoning.rules) == 1
    
    def test_forward_chaining(self):
        """Test forward chaining inference"""
        reasoning = AdvancedReasoningEngine()
        
        # Add facts
        reasoning.add_fact("it is raining")
        
        # Add rule
        reasoning.add_rule(
            conditions=["it is raining"],
            conclusion="ground is wet"
        )
        
        # Perform inference
        new_facts = reasoning.forward_chain()
        assert "ground is wet" in reasoning.facts
        assert "ground is wet" in new_facts
    
    def test_backward_chaining(self):
        """Test backward chaining inference"""
        reasoning = AdvancedReasoningEngine()
        
        # Add facts
        reasoning.add_fact("it is raining")
        
        # Add rule
        reasoning.add_rule(
            conditions=["it is raining"],
            conclusion="use umbrella"
        )
        
        # Check if goal is provable
        provable = reasoning.backward_chain("use umbrella")
        assert provable == True
    
    def test_abductive_reasoning(self):
        """Test abductive reasoning"""
        reasoning = AdvancedReasoningEngine()
        
        # Add rule
        reasoning.add_rule(
            conditions=["it is raining", "clouds are dark"],
            conclusion="ground is wet",
            confidence=0.9
        )
        
        # Find explanations for observation
        explanations = reasoning.abductive_reasoning("ground is wet")
        assert len(explanations) > 0
        assert 'plausibility' in explanations[0]
    
    def test_causal_inference(self):
        """Test causal inference"""
        reasoning = AdvancedReasoningEngine()
        
        # Build causal chain
        reasoning.add_causal_relation("rain", "wet_ground")
        reasoning.add_causal_relation("wet_ground", "slippery")
        
        # Infer effects
        effects = reasoning.causal_inference("rain", max_depth=3)
        assert "wet_ground" in effects
        assert "slippery" in effects
    
    def test_reasoning_statistics(self):
        """Test reasoning statistics"""
        reasoning = AdvancedReasoningEngine()
        
        reasoning.add_fact("fact1")
        reasoning.add_fact("fact2")
        reasoning.add_rule(["fact1"], "fact3")
        
        stats = reasoning.get_reasoning_statistics()
        assert stats['total_facts'] == 2
        assert stats['total_rules'] == 1
    
    def test_query_system(self):
        """Test natural language query"""
        reasoning = AdvancedReasoningEngine()
        
        reasoning.add_fact("sky is blue")
        
        answer = reasoning.query("what is the sky?")
        assert 'answer' in answer
        assert answer['answer'] == "sky is blue"


class TestAdaptiveLearning:
    """Test adaptive learning optimizer"""
    
    def test_adaptive_creation(self):
        """Test adaptive optimizer creation"""
        optimizer = AdaptiveLearningOptimizer(initial_lr=0.01)
        assert optimizer.learning_rate == 0.01
    
    def test_learning_rate_adaptation(self):
        """Test learning rate adaptation"""
        optimizer = AdaptiveLearningOptimizer(initial_lr=0.01)
        
        # Simulate improving performance
        for i in range(10):
            performance = 0.5 + i * 0.05
            lr = optimizer.adapt_learning_rate(performance, target=0.9)
        
        # Learning rate should have been adjusted
        assert len(optimizer.lr_history) == 10
