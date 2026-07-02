# Add or discover new sources for your notebook - Computer - NotebookLM Help
**Source:** [https://support.google.com/notebooklm/answer/16215270?hl=en&amp;ref_topic=16164070](https://support.google.com/notebooklm/answer/16215270?hl=en&amp;ref_topic=16164070)

# Add or discover new sources for your notebook

**Important:** At this time, the NotebookLM mobile app may have limitations to this feature. [Learn more about the supported features in NotebookLM mobile app](/notebooklm/answer/16296687).

A source is a copy or auto-synced version of the source document you import or upload to the app. When you use NotebookLM, the model uses the sources you upload to answer your questions or complete your requests.

## Understand source types & limitations

NotebookLM supports these source types:

* Audio files: MP3 and WAV, among others.
* Copy and pasted text
* Google Drive files, including:
  + Google Docs
  + Google Slides: Up to 100 slides
  + Google Sheets: At this time, files are limited to 100k tokens
* Google Docs
* Google Slides: up to 100 slides
* Google Sheets: at this time, files are limited to 100k tokens
* Images:
  + Supported file types: avif, bmp, gif, heic, heif, ico, jp2, jpe, jpeg, jpg, png, tif, tiff, webp
  + At this time, certain types of images may not work as well.
* Microsoft Word (docx), Text (txt), Markdown (md), PDF files (pdf), CSV (csv), and PowerPoint (pptx) files
* Web URLs
* ePub files
* YouTube URLs of public videos
* Gemini Chats: Chat with your notebooks in Gemini to add them as context to your NotebookLM notebooks. [Learn more about NotebookLM notebooks in Gemini Apps.](/gemini/answer/16972047)

Each source can contain up to 500,000 words or up to 200MB for uploaded files. You can include up to 50 sources (for Free users). [Learn about source limits and premium features in Google’s AI Plans.](/notebooklm/answer/16213268)

**Tips:**

* Avoid uploading documents you don’t have rights to.
* You can copy and paste text to create a new source and add or edit the title upon creation.
* To chat with a specific set of sources in your Notebook, select them individually in the “Source” panel.
* When uploading multiple web URLs, separate links by a space or a new line.

## Summarize a source

NotebookLM offers 2 modes for summarizing sources. You can:

* Ask for a summary of specific topics from your source directly in chat.
* Find an auto-generated summary of the entire source in the Source Guide. In the left hand side source viewer, select "To open a source.”

To get more focused summaries in the chat, ask specific questions about the information you're looking for. When multiple sources are selected, mentioning source names in your query helps NotebookLM narrow its search. For example, instead of "Summarize this source," try "What are the key findings about dog training in the 'Dog Training 101' document?"

## Add source

1. On your computer, open [NotebookLM](https://notebooklm.google.com/) or Notebooks in Gemini.
2. Select Add ![](//storage.googleapis.com/support-kms-prod/tKbhvylWdt3SXsLkNu9x93PCC8oxy8yqG5tc).
   * Type a research question in the search box to find sources from the web or files from Workspace.Select all the sources you want to include in your notebook.

### Import Google Drive files

When adding sources, you can import supported files from your Google Drive. You can choose one or multiple files to import at a time.

* Sources imported from Google Drive are auto-updated and will sync every few minutes. Changes to your original document will automatically update in your Notebook. If needed, you can manually update a source by opening the source in Notebook and clicking ”Click to sync with Google Drive.”
* You can only import files if you have **view access or more**. If you lose access to a file in Google Drive or if the file is deleted, the source will be inaccessible, and you will no longer be able to view or interact with the source in your notebook. This applies to both owned and shared notebooks.
* Inactive sources will count towards source limits but will not be referenced throughout your notebook. For example:
  + Chats will not reference the inaccessible file
  + The studio will not reference the inaccessible file when generating images or slides.
* If needed, you can use the links provided to request access to files or remove them from your source list.
* NotebookLM can’t delete or edit your original files in Drive. The source content may appear differently in the NotebookLM viewer than the original file to enable analysis and understanding of the source information. This does not change the formatting of the original source file.
* **Limitations**
  + NotebookLM does not import footnotes or comments from Google files.
  + While NotebookLM will pull in data from multiple tabs in Google Docs and Google Sheets as one source.
  + Importing audio files from Drive is not supported.

### Import through Web URL

* Only the text content of the given HTML webpage is scraped for use as a source. Images, embedded videos, or nested webpages are not imported. Paywalled webpages aren't supported.
* PDFs uploaded through URLs are treated as PDF sources.

### Import through YouTube URL

* Only public YouTube videos with captions, either user-uploaded or auto-generated, are supported.
* Only the text transcript of the video is imported as a source.
* Videos uploaded less than 72 hours prior may not be available to import.
* Videos without speech aren't supported.
* If a video is deleted or made private, sources are auto-deleted from your notebook within 30 days.
* There is no limit for the length of the video unless the caption file contains over 500,000 words.
* Your import can fail for a number of reasons; the most common are:
  + The YouTube link is invalid.
  + The video is potentially unsafe.
  + The content doesn't have a captions file.
  + The video language is not currently supported.

### Import a local audio file

* The audio file is transcribed at the time of import and its text is saved to use as a new source.
* Supported audio file types include: 3g2, 3gp, aac, aif, aifc, aiff, amr, au, avi, cda, m4a, mid, mp3, mp4, mpeg, ogg, opus, ra, ram, snd, wav, wma
* Audios with no speech aren't supported.

Languages supported for audio import

**Tip:** Imports may fail if the audio is low quality.

Languages listed below are supported for audio import:

* Afrikaans
* Amharic
* Albanian
* Arabic
* Armenian
* Azerbaijani
* Bangla
* Basque
* Belarusian
* Bulgarian
* Burmese
* Catalan
* Czech
* Danish
* Dutch
* English
* Estonian
* Filipino
* Finnish
* French
* Galician
* Georgian
* German
* Greek
* Gujarati
* Hebrew
* Hindi
* Hungarian
* Icelandic
* Indonesian
* Italian
* Javanese
* Japanese
* Khmer
* Kannada
* Korean
* Lao
* Latvian
* Lithuanian
* Macedonian
* Malay
* Malayalam
* Marathi
* Mongolian
* Norwegian
* Nepali
* Punjabi
* Persian
* Polish
* Portuguese
* Romanian
* Russian
* Serbian
* Sinhalese
* Slovak
* Slovene
* Spanish
* Sundanese
* Swedish
* Swahili
* Tamil
* Telugu
* Thai
* Traditional Cantonese
* Traditional Chinese
* Turkish
* Ukrainian
* Urdu
* Uzbek
* Vietnamese
* Zulu

**Tip:** If the source content is too short, NotebookLM references the entire document without citing individual text from your source.

## How to Search for Sources

**Important**: At this time, the NotebookLM mobile app may have limitations to this feature. [Learn more about the supported features in NotebookLM mobile app](/notebooklm/answer/16296687).

Pull in sources based on a query to conveniently begin new notebooks and build comprehensive collections of relevant materials. You can search for sources from the web or Google Drive with Fast Research, or you can use [Gemini Deep Research](https://gemini.google/overview/deep-research/) directly within NotebookLM.

### Fast Research

1. In the sources panel, enter a query in the search box. You can try: “Butterfly Anatomy”, “Most Important Fossil Finds”, "Docs about Q4 planning," or "Slides from Claire."
2. Choose Web or Drive
   * NotebookLM will pull in supported sources from the web or from Google Drive that you have access to
3. Search and review results. Expand the view and select/deselect results by clicking on “View”.
   * The most relevant search results are presented in a list and include:
     + The title
     + A brief description on how the source relates to your original query
     + A link to open the full webpage in a new window
4. Select sources and import: Select one or multiple sources from the search results to import into your notebook.

### Deep Research

Deep Research is an agentic feature that can automatically browse up to hundreds of websites on your behalf, think through its findings, and create insightful multi-page reports in minutes. NotebookLM lets you search, compile, and import the results and sources. Learn more about Gemini’s [Deep Research](https://gemini.google/overview/deep-research/) capabilities.

1. In the Sources panel, enter a research question in the search box.
2. Toggle on “Web” and “Deep Research”
3. Search to start. Results may take a couple minutes to load, and you can continue to use NotebookLM while you wait.
4. Import all results, or review by clicking on “View” to expand.
   * You will see the Deep Research report as well as a list of all relevant sources (cited and not cited).
   * Select and deselect to choose which results you would like to import as sources into your Notebook.
5. “Cancel” or minimize to exit Deep Research mode. All results that are not imported will be discarded.

**Important**:  At this time, this feature is also only available to over 18 users. Source limits apply. Results may be partially imported if usage limits are exceeded. [Learn more about limits.](https://support.google.com/notebooklm/answer/16213268?hl=en&ref_topic=16175214&sjid=12844604175234447838-NA)

### Label & Categorize Sources

When you have 5+ sources, NotebookLM can auto-label & categorize sources, allowing you to quickly and easily organize your sources by topic. By default, your sources will be automatically organized. You can also manually modify source organization by:

* Adding a new label
* Re-naming labels
* Deleting labels
* Moving sources to different labels

## Related resources

* [Create a notebook in NotebookLM](/notebooklm/answer/16206563)
* [Use chat in NotebookLM](/notebooklm/answer/16179559)
* [Use Mind Maps in NotebookLM](/notebooklm/answer/16212283)

[Computer](https://support.google.com/notebooklm/answer/16215270?hl=en&amp;ref_topic=16164070&co=GENIE.Platform%3DDesktop) [Android](https://support.google.com/notebooklm/answer/16215270?hl=en&amp;ref_topic=16164070&co=GENIE.Platform%3DAndroid)[iPhone & iPad](https://support.google.com/notebooklm/answer/16215270?hl=en&amp;ref_topic=16164070&co=GENIE.Platform%3DiOS)

More

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://support.google.com/notebooklm/answer/16206563](./notebooklm-answer-16206563.md)
- [https://support.google.com/notebooklm/answer/16212283](./notebooklm-answer-16212283.md)
- [https://support.google.com/notebooklm/answer/16296687](./notebooklm-answer-16296687.md)
