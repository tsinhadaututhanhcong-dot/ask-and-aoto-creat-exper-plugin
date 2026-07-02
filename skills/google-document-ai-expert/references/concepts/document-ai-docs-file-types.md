# Supported Files  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/file-types](https://docs.cloud.google.com/document-ai/docs/file-types)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback

# Supported Files Stay organized with collections Save and categorize content based on your preferences.



## File Types

Document AI supports the following image types.

For information about file size and page limits, refer to the [Quotas and
Limits](/document-ai/quotas#content_limits) page.

**Note:** Document AI includes some supported file types in [Preview](https://cloud.google.com/products/#product-launch-stages).
These will be charged when they are released to General Availability (GA).

| Name | File Extension(s) | [MIME Type](https://www.iana.org/assignments/media-types/media-types.xhtml) |
| --- | --- | --- |
| Portable Document Format (PDF) | `.pdf` | `application/pdf` |
| Graphics Interchange Format (GIF) | `.gif` | `image/gif` |
| Tag Image File Format (TIFF) | `.tiff`, `.tif` | `image/tiff` |
| Joint Photographic Experts Group (JPEG) | `.jpg`, `.jpeg` | `image/jpeg` |
| Portable Network Graphics (PNG) | `.png` | `image/png` |
| Bitmap (BMP) | `.bmp` | `image/bmp` |
| WebP | `.webp` | `image/webp` |
| HyperText Markup Language (HTML) | `.html` | `text/html` |
| Microsoft Word Office Open XML (OOXML) | `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Microsoft PowerPoint OOXML | `.pptx` | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| Microsoft Excel OOXML | `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

Note that some of these image formats are "lossy" (for example, JPEG). Reducing
file sizes for lossy formats may result in a degradation of image quality and
accuracy of results from Document AI.

**Note:** Prior JPEG compressions for TIFF are unsupported. Type of JPEG encapsulation
defined by the TIFF [version 6.0
specification](https://gitlab.com/libtiff/libtiff/-/commit/f0a54a4fa0cfa377f493d57ee2af393005d5bbe5).**Note:** HTML and OOXML support are only available with [layout
parser](/document-ai/docs/layout-parse-chunk). [Custom
splitter](/document-ai/docs/custom-splitter) only supports PDF, TIFF, TIF, and
GIF file types.

### Document scan resolution

For most accurate OCR results from Document AI, document scans should be
a minimum of 200 dpi [(dots per inch)](https://en.wikipedia.org/wiki/Dots_per_inch).
300 dpi and higher generally produce the best results. OCR accuracy is dependent
on both the resolution and the minimum font size, along with other factors like
document (and if handwritten, handwriting) quality, so testing is recommended.
The [image quality analysis](/document-ai/docs/process-documents-ocr#image-quality_analysis)
feature can help evaluate resolution concerns.

NOTE: 2k x 3k pixels are required for the US driver's license back side image in
order to read the barcode.

[Previous

arrow\_back

Processor list](/document-ai/docs/processors-list)

[Next

Regional and multi-regional support

arrow\_forward](/document-ai/docs/regions)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/custom-splitter](./document-ai-docs-custom-splitter.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/process-documents-ocr](./document-ai-docs-process-documents-ocr.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
