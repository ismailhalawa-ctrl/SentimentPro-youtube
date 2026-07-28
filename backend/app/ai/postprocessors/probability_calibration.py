import math


def apply_temperature(probs: dict[str, float], temperature: float) -> dict[str, float]:
    if not probs or temperature == 1.0:
        return probs

    logits = {label: math.log(max(p, 1e-9)) for label, p in probs.items()}
    scaled = {label: logit / temperature for label, logit in logits.items()}
    max_scaled = max(scaled.values())
    exps = {label: math.exp(value - max_scaled) for label, value in scaled.items()}
    denominator = sum(exps.values())
    return {label: value / denominator for label, value in exps.items()}
