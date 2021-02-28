class Threshold:
    def __init__(self, threshold, color):
        self._threshold = threshold
        self._color = color

    def under_threshold(self, value):
        return value < self._threshold

    def threshold(self):
        return self._threshold

    def color(self):
        return self._color


class ThresholdConfiguration:
    def __init__(self, default_color, max):
        self._thresholds = []
        self._complete = False
        self._max = max
        self._default = Threshold(threshold=-1, color=default_color)

    def add(self, threshold, color):
        if not self._complete:
            self._thresholds.append(Threshold(threshold=threshold, color=color))
            return self

        else:
            raise Exception('The configuration is ready. You cannot add more thresholds')

    def complete(self):
        self._complete = True
        self._thresholds.sort(key=lambda threshold: threshold.threshold())
        return self

    def max(self):
        return self._max

    def match(self, value):
        for threshold in self._thresholds:
            if threshold.under_threshold(value):
                return threshold

        if len(self._thresholds) > 0:
            return self._thresholds[len(self._thresholds) - 1]
        else:
            return self._default
