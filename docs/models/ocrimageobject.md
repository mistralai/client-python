# OCRImageObject


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `id`                                                       | *str*                                                      | :heavy_check_mark:                                         | Image ID for extracted image in a page                     |
| `top_left_x`                                               | *Nullable[int]*                                            | :heavy_check_mark:                                         | X coordinate of top-left corner of the extracted image     |
| `top_left_y`                                               | *Nullable[int]*                                            | :heavy_check_mark:                                         | Y coordinate of top-left corner of the extracted image     |
| `bottom_right_x`                                           | *Nullable[int]*                                            | :heavy_check_mark:                                         | X coordinate of bottom-right corner of the extracted image |
| `bottom_right_y`                                           | *Nullable[int]*                                            | :heavy_check_mark:                                         | Y coordinate of bottom-right corner of the extracted image |
| `image_base64`                                             | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | Base64 string of the extracted image                       |