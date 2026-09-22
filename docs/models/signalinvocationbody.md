# SignalInvocationBody


## Fields

| Field                                                                                        | Type                                                                                         | Required                                                                                     | Description                                                                                  |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `name`                                                                                       | *str*                                                                                        | :heavy_check_mark:                                                                           | The name of the signal to send                                                               |
| `input`                                                                                      | [OptionalNullable[models.SignalInvocationBodyInput]](../models/signalinvocationbodyinput.md) | :heavy_minus_sign:                                                                           | Input data for the signal, matching its schema                                               |