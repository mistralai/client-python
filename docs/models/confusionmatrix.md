# ConfusionMatrix

A confusion matrix over ``(expected, predicted)`` label pairs.

``matrix[i][j]`` is the number of samples whose expected label is ``labels[i]`` and predicted
label is ``labels[j]``. It is the complete, aggregatable representation: precision/recall/f1 for
any class derive from it, and matrices from several runs merge by element-wise sum.


## Fields

| Field              | Type               | Required           | Description        |
| ------------------ | ------------------ | ------------------ | ------------------ |
| `labels`           | List[*str*]        | :heavy_check_mark: | N/A                |
| `matrix`           | List[List[*int*]]  | :heavy_check_mark: | N/A                |