# AliasList

Presence wrapper for a set of alias labels on update RPCs. As a message field it carries presence, so callers can distinguish "leave aliases unchanged" (field omitted) from "clear all aliases" (field set, empty ``values``).


## Fields

| Field              | Type               | Required           | Description        |
| ------------------ | ------------------ | ------------------ | ------------------ |
| `values`           | List[*str*]        | :heavy_minus_sign: | N/A                |