# IPAPhoneme

The IPA phone inventory usable in pronunciation hints.

``StrEnum`` members' values are their (lowercase) names via ``auto()``, so each member IS
the IPA string it represents. Using an enum makes ``phoneme_hints`` values self-validating
at the API boundary (pydantic rejects any phone outside this set). **Append-only**: never
reorder or remove entries, only add new phones (e.g. for future languages) at the end.

## Example Usage

```python
from mistralai.client.models import IPAPhoneme
value: IPAPhoneme = "a"
```


## Values

- `"a"`
- `"aɪ"`
- `"aʊ"`
- `"b"`
- `"d"`
- `"dʒ"`
- `"e"`
- `"eɪ"`
- `"f"`
- `"g"`
- `"h"`
- `"i"`
- `"j"`
- `"k"`
- `"l"`
- `"m"`
- `"n"`
- `"o"`
- `"oʊ"`
- `"p"`
- `"s"`
- `"t"`
- `"tʃ"`
- `"u"`
- `"v"`
- `"w"`
- `"z"`
- `"æ"`
- `"ð"`
- `"ŋ"`
- `"ɑ"`
- `"ɔ"`
- `"ɔɪ"`
- `"ɖ"`
- `"ə"`
- `"ɚ"`
- `"ɛ"`
- `"ɜ"`
- `"ɪ"`
- `"ɱ"`
- `"ɹ"`
- `"ɾ"`
- `"ʃ"`
- `"ʈ"`
- `"ʊ"`
- `"ʋ"`
- `"ʌ"`
- `"ʒ"`
- `"ʔ"`
- `"θ"`
