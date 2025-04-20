from jiwer import wer

def compute_pronunciation_score(hypothesis, reference):
    """ this function compares spoken transcript with reference text using WER.
    it also returns accuracy as a percentage."""
    error_rate = wer(reference.lower(), hypothesis.lower())
    accuracy = max(0, 1 - error_rate)
    return round(accuracy * 100, 2)


def compute_timing_score(actual_duration, expected_duration, tolerance=0.5):
    """
    it compares spoken duration to expected duration.
    and also returns timing score as a percentage.
    """
    diff = abs(actual_duration - expected_duration)

    if diff <= tolerance:
        return 100.0

    excess = diff - tolerance
    penalty_ratio = excess / expected_duration
    score = max(0, (1 - penalty_ratio)) * 100

    return round(score, 2)
