def fuse_probability_distributions(distributions: list[dict[str, float]]) -> dict[str, float]:
    labels: set[str] = set()
    for distribution in distributions:
        labels.update(distribution.keys())

    return {
        label: sum(distribution.get(label, 0.0) for distribution in distributions) / len(distributions)
        for label in labels
    }
