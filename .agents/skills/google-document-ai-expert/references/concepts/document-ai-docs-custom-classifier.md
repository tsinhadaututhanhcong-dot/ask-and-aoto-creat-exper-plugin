# Create, use, and manage a custom document classifier  |  Document AI  |  Google Cloud Documentation
**Source:** [https://docs.cloud.google.com/document-ai/docs/custom-classifier](https://docs.cloud.google.com/document-ai/docs/custom-classifier)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [AI and ML](https://docs.cloud.google.com/docs/ai-ml)
* [Document AI](https://docs.cloud.google.com/document-ai/docs)
* [Guides](https://docs.cloud.google.com/document-ai/docs/overview)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.



# Create, use, and manage a custom document classifier

Use custom classifier to classify documents. Build it from the ground up with your
own documents and custom classes. Its generative AI aspect allows few-shot learning
and fine-tuning. These improve accuracy with fewer samples and corrections with
iterative auto-labeling.

Custom classifier covers these three general use cases.

* **Pretrained model:** Use the pretrained generative AI foundation model to
  quickly classify documents with your supplied labels.
* **Fine-tuning:** Improve accuracy by training the generative AI foundation model
  on your own data and labels.
* **Train a custom model:** Train a non-generative AI custom extractor using your
  own data and labels.

## Custom classifier model versions

Confidence scores are supported for custom classifier models in
[Preview](https://cloud.google.com/products#product-launch-stages). For
best performance, use them with fine-tuned models.

| Model version | Description | Release channel | ML processing in US/EU | Fine-tuning in US/EU | Release date |
| --- | --- | --- | --- | --- | --- |
| `pretrained-classifier-v1.5-2025-08-05` | Production-ready model powered by the Gemini 2.5 Flash LLM. Also includes advanced OCR features. This pre-trained model can be used without prior training. It supports zero-shot classification and provides better support for the catch-all class. | Stable | Yes | US, EU ([Preview](/products#product-launch-stages)) | August 5, 2025 |
| `pretrained-classifier-v1.6-2026-03-09` | Release candidate powered by the Gemini 3.1 Flash LLM. **Note:** This version does not support data residency. | Release Candidate | Yes | US, EU ([Preview](/products#product-launch-stages)) | March 9, 2026 |
| `pretrained-classifier-v1.6-pro-2026-03-09` | Release candidate powered by the Gemini 3.1 Pro LLM. **Note:** This version does not support data residency. | Release Candidate | Yes | US, EU ([Preview](/products#product-launch-stages)) | March 9, 2026 |

**Tip:** v1.5 uses Generative AI, you can use it out of the box without training.

## Create a custom classifier in the Google Cloud console

You can create custom classifiers that are specifically suited to your documents
and trained and evaluated with your data. This processor identifies classes of
documents from a user-defined set of classes. You can then use this trained processor
on additional documents. You typically would use a custom classifier on documents
that are different types, then use the identification to pass the documents to an
extraction processor to extract the entities.

For the general process to create and use a processor, see the [How to](/document-ai/docs/how-to)
section.

**Note:** If you have your documents in separate folders by class, then you can skip
step 4 by specifying the class at import time.

You can make your own configuration choices that suit your workflow.

---

To follow step-by-step guidance for this task directly in the
Google Cloud console, click **Guide me**:

[Guide me](https://console.cloud.google.com/ai/document-ai?tutorial=document-ai--documentai-workbench_custom_classifier_console)

---

## Before you begin

- Sign in to your Google Cloud account. If you're new to
  Google Cloud, [create an account](https://console.cloud.google.com/freetrial) to evaluate how our products perform in
  real-world scenarios. New customers also get $300 in free credits to
  run, test, and deploy workloads.
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI, Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com,storage.googleapis.com)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](/iam/docs/granting-changing-revoking-access).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard)
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](/billing/docs/how-to/verify-billing-enabled#confirm_billing_is_enabled_on_a_project).
- Enable the Document AI, Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](/iam/docs/granting-changing-revoking-access).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=documentai.googleapis.com,storage.googleapis.com)

### Required roles

To get the permissions that
you need to create a custom classifier,
ask your administrator to grant you the
following IAM roles on your project:

* [Document AI Administrator](/iam/docs/roles-permissions/clouddocumentai#documentai.admin)  (`roles/documentai.admin`)
* [Storage Admin](/iam/docs/roles-permissions/storage#storage.admin)  (`roles/storage.admin`)

For more information about granting roles, see [Manage access to projects, folders, and organizations](/iam/docs/granting-changing-revoking-access).

You might also be able to get
the required permissions through [custom
roles](/iam/docs/creating-custom-roles) or other [predefined
roles](/iam/docs/roles-overview#predefined).

**Note:** If you want to access input files stored in a different project, then you
need to grant additional roles to the Document AI service agent. For
more information, see [Cross project file access
setup](/document-ai/docs/setup#cross_project_file_access_setup).

## Create a processor

Complete the following steps.

1. Go to the [Workbench](https://console.cloud.google.com/ai/document-ai/workbench)
2. For custom document classifier, select
   **Create processor**.

   ![custom-classifier-1](/static/document-ai/docs/images/create/custom-classifier-1.png)
3. In the **Create processor** menu, enter a name for your processor, such as `my-custom-document-classifier`.

   ![custom-classifier-2](/static/document-ai/docs/images/create/custom-classifier-2.png)
4. Select the region closest to you.
5. Select **Create**. The **Processor Details** tab appears.

## Configure dataset

To train this new processor, you must create a dataset with training and
testing data to help the processor identify the documents that you want to split
and classify. This dataset requires a new location. This can be an empty [Cloud Storage bucket](/storage)
or folder, or you can allow an internally managed location.

After the **Processor Details** tab appears, then you can:

1. Select **Google-managed storage** in case you want to use Cloud Storage.
2. Select **I'll specify my own storage location** if you want to use your own
   storage to use Customer-Managed Encryption Keys (CMEK), and follow the
   procedure in [Create a dataset](/document-ai/docs/create-dataset).

![custom-classifier-3](/static/document-ai/docs/images/create/custom-classifier-3.png)

**Note:** Folders for datasets must be treated as read-only. Don't change or add anything.

## Import documents into a dataset

Next, you import your documents into your dataset.

1. On the **Build** tab, select
   **Import documents**.

   ![custom-classifier-6](/static/document-ai/docs/images/create/custom-classifier-6.png)
2. When choosing to use a storage bucket, you must enter the **Source Path** for
   the bucket. For this training example, enter this bucket name in
   **Source path**. This links directly to one document.

   ```
   cloud-samples-data/documentai/Custom/Patents/PDF/computer_vision_20.pdf
   ```
3. For **Data split**, select **Unassigned**. The document in this folder is not
   assigned to either the testing or training set. Leave **Import with auto-labeling**
   unchecked.
4. Select **Import**. Document AI reads the documents from the bucket into
   the dataset. It does not modify the import bucket or read from the bucket after
   the import is complete.
5. Optional: To delete imported documents, in the
   **Build** tab, go to **Manage dataset** > select the documents > click **Delete**.

When you import documents, you can optionally assign the documents to
the **Training** or **Test** set when imported, or wait to assign them later.

For more information about preparing your data for import, refer to the
[Data preparation guide](/document-ai/docs/workbench/create-dataset).

## Define processor schema

You can create the processor schema either before or after you import documents
into your dataset. The schema provides labels that you use to annotate documents.

1. On the **Build** tab, select **Manage Dataset** > **Edit Schema**.
   The **Edit schema** page opens.
2. Select
   **Create label**.
3. Enter the name for the label.
4. Select **Create**. Refer to [Define processor schema](/document-ai/docs/workbench/label-documents#define_processor_schema)
   for detailed instructions on creating and editing a schema.

   **Note:** When a processor is trained, labels cannot be deleted. Instead, you can
   disable any label you don't want to use.
5. Create each of the following labels for the processor schema.

   * `computer_vision`
   * `crypto`
   * `med_tech`
   * `other`**Tip:** Use the description field to enter a prompt which describes the label.
   This helps train the model and differentiate similarly written labels. Learn
   more at [label with property descriptions](/document-ai/docs/label-documents#add-a-description-prompt).
6. Select
   **Save** when the labels are complete.

   ![custom-classifier-7](/static/document-ai/docs/images/create/custom-classifier-7.png)

**Note:** Labels are flat and don't support child entities.

## Label a document

The process of selecting text in a document and applying labels is known as
annotation.

1. Return to the **Build** tab, and select
   a document
   to open the **Manage Dataset** console.
2. Among the options,
   select the appropriate label for the document.
   If you're using the sample document provided, select **`computer_vision`**.

   When labeled, the document should look like this: ![custom-classifier-8](/static/document-ai/docs/images/create/custom-classifier-8.png)
3. Select
   **Mark as Labeled**
   when you have finished annotating the document.

   On the **Manage Dataset** tab, the **Document** panel shows that one document
   has been labeled.

**Tip:** Remember to be meticulous when labeling manually or using batch labeling.
Tidy labeling improves techniques using [zero-and few-shot labeling](/document-ai/docs/label-documents#zero-shot_and_few-shot_learning).

## Assign annotated document to the training set

Now that you have labeled this example document, you can assign it to the
training set.

1. On the **Manage Dataset** tab, select the
   **Select All**
   checkbox.
2. From the
   **Assign to Set**
   list, select **Training**.

In the **Documents** panel, you can find that one document has been assigned to the
training set.

## (Optional) Import prelabeled data to the training and test sets

If you're using v1.4, you must upload training and test sets to train the custom
processor. You may skip this step when using v1.5.

In this guide, you are provided with prelabeled data. If working on your own
project, you have to determine how to label your data. Refer to [Labeling options](/document-ai/docs/workbench/label-documents#labeling_options).

Document AI custom processors require a minimum of one document in both the
training and test sets for each document type to be labeled. We recommend that
you have at least 10 documents for each label for best performance. For 5 labels,
you would need 50 documents to train and 50 to test. More training data
typically produces higher accuracy.

1. Select
   **Import documents**.
2. Enter the following path in
   **Source path**. This bucket contains pre-labeled documents in the [Document JSON](/document-ai/docs/reference/rest/v1/Document) format.

   ```
   cloud-samples-data/documentai/Custom/Patents/JSON/Classification-InventionType
   ```
3. From the **Data split** list, select **Auto-split**. This automatically
   splits the documents to have 80% in the training set and 20% in the test set.
   Ignore the **Apply labels** section.
4. Select **Import**. The import might take several minutes to complete.

When the import is finished, you'll find the documents in the **Manage Dataset**
tab.

## Batch label documents at import

Optionally, after the schema has been configured, you can label all documents that are in a
particular directory at import to save time with labeling.

![custom-classifier-9](/static/document-ai/docs/images/create/custom-classifier-9.png)

1. Select
   **Import documents**.
2. Enter the following path in
   **Source path**. This bucket contains unlabeled documents in PDF format.

   ```
   cloud-samples-data/documentai/Custom/Patents/PDF-CDC-BatchLabel
   ```
3. From the **Data split** list, select **Auto-split**. This automatically splits
   the documents to have 80% in the training set and 20% in the test set.
4. In the **Apply labels** section, select **Choose label**.
5. For these sample documents, select `other`.
6. Select **Import** and wait for the process to finish. You can leave this page
   and return later.
   When complete, you find the documents on the **Manage Dataset** tab with the label
   applied.

## (Optional) Train the processor

If you're using v1.4, you must train the custom processor on training and test
sets of data. You may skip this step when using v1.5.

Now that you have imported the training and test data, you can train the processor.
Because training might take several hours, make sure you have set up the processor
with the appropriate data and labels before you begin training.

You can train fine-tuned and custom models with your labeled data. Fine-tuned
models use generative AI. The custom models trains a unique large language Model
using your labeled data. You need a minimum of two labels in the schema, with a
recommended ten training documents and 10 test documents (minimum of 1).

1. Select
   **Train New Version**.

![custom-classifier-10](/static/document-ai/docs/images/create/custom-classifier-10.png)
**Note:** Fine-tuning will tune a foundation model, which is recommended.
**Train a custom model** will train a conventional model, one without generative AI.

1. In the
   **Version name** field, enter a name for this processor version, such as `my-cdc-version-1`.
2. Optional: Select **View Label Stats** to find information about the document
   labels that can help determine your coverage. Select **Close** to return to the
   training setup.
3. Select
   **Start training**.
   You can check the status on the side panel.

## Deploy the processor version

1. After training is complete, navigate to the
   **Manage Versions**
   tab. You can view details about the version you just trained.
2. Select the
   more\_vert
   beside the version you want to deploy, and select **Deploy version**.
3. Select
   **Deploy**
   from the dialog window.

   Deployment takes a few minutes to complete.

## Evaluate and test the processor

1. After deployment is complete, navigate to the
   **Evaluate & Test**
   tab.

   On this page, you can view evaluation metrics including the F1 score, precision
   and recall for the full document, and individual labels. For more information
   about evaluation and statistics, refer to [Evaluate processor](/document-ai/docs/workbench/evaluate).
2. Download a document that has not been involved in previous training or testing
   so that you can use it to evaluate the processor version. If using your own data,
   you would use a document set aside for this purpose.

   [file\_download
   Download PDF](https://storage.googleapis.com/cloud-samples-data/documentai/Custom/Patents/PDF/us_100.pdf)
3. Select
    **Upload Test Document**  and select the document you just downloaded.

   The **Custom Document Classifier analysis** page opens. The output demonstrates
   how well the document was classified.

   You can also rerun the evaluation against a different test set or processor
   version.

## Auto-label newly imported documents

After deploying a trained processor version, you can use [Auto-labeling](/document-ai/docs/workbench/label-documents#auto-label) to save time on labeling when importing new documents.

1. On the **Manage Dataset** page, **Import documents**.
2. Copy and paste the following Cloud Storage path. This directory contains
   five unlabeled patent PDFs. From the **Data split** drop-down list, select **Training**.

   ```
   cloud-samples-data/documentai/Custom/Patents/PDF-CDC-AutoLabel
   ```
3. In the **Apply labels** section, select **Auto-labeling**.
4. Select an existing processor version to label the documents.

   * For example: `2af620b2fd4d1fcf`
5. Select **Import** and wait for the process to finish. You can leave this page
   and return later. When complete, the documents appear in the **Auto-labeled**
   section of the **Manage Dataset** page.
6. You cannot use auto-labeled documents for training or testing without marking
   them as labeled. Go to the **Auto-labeled**
   section to view the auto-labeled documents.
7. Select the first document to enter the labeling console.
8. Verify the label to ensure it's correct. Adjust if it's incorrect.
9. Select **Mark as Labeled** when finished.
10. Repeat the label verification for each auto-labeled document, then return to
    the **Manage Dataset** page to assign the data for training.

## Use the processor

You can manage your custom-trained processor versions just like any other processor
version. For more information, refer to [Managing processor versions](/document-ai/docs/manage-processor-versions).

You can also [Send a processing request](/document-ai/docs/send-request) to your custom
processor, and the
[response can be handled the same as other classifier processors](/document-ai/docs/handle-response#splitting).

## Clean up

To avoid incurring charges to your Google Cloud account for
the resources used on this page, follow these steps.

1. In the Google Cloud console navigation menu, select **Document AI**, then
   **My Processors**.
2. Select **More actions** in the same row as the processor you want to delete.
3. Select **Delete processor**, enter the processor name, then select **Delete**
   again to confirm.

## What's next

* For more details, see [Guides](/document-ai/docs/how-to).
* Review the [processors list](/document-ai/docs/processors-list).
* Separate documents into readable chunks with [Layout Parser](/document-ai/docs/layout-parse-chunk).
* Use [Enterprise Document OCR](/document-ai/docs/enterprise-document-ocr) to
  detect and extract text.

[Next

Custom splitter

arrow\_forward](/document-ai/docs/custom-splitter)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-06-29 UTC."],[],[]]

## Related Files
- [https://docs.cloud.google.com/document-ai/docs](./document-ai-docs.md)
- [https://docs.cloud.google.com/document-ai/docs/custom-splitter](./document-ai-docs-custom-splitter.md)
- [https://docs.cloud.google.com/document-ai/docs/enterprise-document-ocr](./document-ai-docs-enterprise-document-ocr.md)
- [https://docs.cloud.google.com/document-ai/docs/handle-response](./document-ai-docs-handle-response.md)
- [https://docs.cloud.google.com/document-ai/docs/how-to](./document-ai-docs-how-to.md)
- [https://docs.cloud.google.com/document-ai/docs/label-documents](./document-ai-docs-label-documents.md)
- [https://docs.cloud.google.com/document-ai/docs/manage-processor-versions](./document-ai-docs-manage-processor-versions.md)
- [https://docs.cloud.google.com/document-ai/docs/overview](./document-ai-docs-overview.md)
- [https://docs.cloud.google.com/document-ai/docs/processors-list](./document-ai-docs-processors-list.md)
- [https://docs.cloud.google.com/document-ai/docs/send-request](./document-ai-docs-send-request.md)
- [https://docs.cloud.google.com/document-ai/docs/setup](./document-ai-docs-setup.md)
