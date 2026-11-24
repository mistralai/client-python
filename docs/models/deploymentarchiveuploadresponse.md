# DeploymentArchiveUploadResponse

An empty archive, and where to upload the tarball a managed deployment then builds from.


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `archive_id`                                                                   | *str*                                                                          | :heavy_check_mark:                                                             | Pass it as the spec's `archive_id` once the upload has finished.               |
| `upload_url`                                                                   | *str*                                                                          | :heavy_check_mark:                                                             | A signed URL to PUT the tarball to. It grants write access, so keep it secret. |
| `upload_headers`                                                               | Dict[str, *str*]                                                               | :heavy_check_mark:                                                             | Headers the PUT must send for the signed URL to accept it.                     |