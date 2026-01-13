# Hebbian Learning Implementation
class HebbianLearner:
    def __init__(self):
        self.weights = {}
    def learn(self, pre_activity, post_activity):
        return pre_activity * post_activity
