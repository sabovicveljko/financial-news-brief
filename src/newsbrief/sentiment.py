from transformers import pipeline

_classifier = None


def classify_sentiment(text: str)->tuple[str, float]:
    global _classifier

    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model= "ProsusAI/finbert",
            device= -1,
        )

    prediction = _classifier(
        text,
        truncation = True,
        max_length = 512,
    )[0]

    return prediction["label"], prediction["score"]