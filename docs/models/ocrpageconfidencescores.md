# OCRPageConfidenceScores

Confidence scores for an OCR page at various granularities.

Note on page-level stats:
- For 'page' and 'block' granularity: average/minimum are computed from per-token
  exp(logprob). Neither ``word_confidence_scores`` nor ``token_scores`` is populated.
  Per-block scores are attached to response blocks separately for 'block' granularity.
- For 'word' granularity: average/minimum are computed from per-word confidence, where
  each word's confidence is exp(mean(token_logprobs)) — a geometric mean over the
  word's subword tokens. ``word_confidence_scores`` is populated.
- For 'token' granularity (internal): average/minimum are computed from
  ``token_scores``; ``token_scores`` is populated.


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `word_confidence_scores`                                             | List[[models.OCRConfidenceScore](../models/ocrconfidencescore.md)]   | :heavy_minus_sign:                                                   | Word-level confidence scores (populated only for 'word' granularity) |
| `average_page_confidence_score`                                      | *float*                                                              | :heavy_check_mark:                                                   | Average confidence score for the page                                |
| `minimum_page_confidence_score`                                      | *float*                                                              | :heavy_check_mark:                                                   | Minimum confidence score for the page                                |