# EmbeddingRequest


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          | Example                                                              |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `model`                                                              | *str*                                                                | :heavy_check_mark:                                                   | ID of the model to use.                                              | mistral-embed                                                        |
| `inputs`                                                             | [models.EmbeddingRequestInputs](../models/embeddingrequestinputs.md) | :heavy_check_mark:                                                   | Text to embed.                                                       | [<br/>"Embed this sentence.",<br/>"As well as this one."<br/>]       |