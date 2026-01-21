---
navigation_title: Contribute to Asciidoc docs
---

# Contribute to `elastic.co/guide` (Asciidoc)

To contribute to pages that live at [elastic.co/guide](https://www.elastic.co/guide/index.html), you must work with our [Asciidoc documentation build system](https://github.com/elastic/docs). These docs are written in the [ASCIIDoc](https://asciidoc.org/) markup language.

Refer to [elastic.co/guide](https://www.elastic.co/guide) for the full list of products and versions that use this system.

## Contribute on the web

These changes should be made in the original source folders in their respective repositories. Here's how you can do it:

1. Navigate to the page that is impacted.
2. Click the **Edit** button.
3. Ensure the targeted branch is \<insert proper branch\>.
4. Make the necessary updates.
5. Commit your changes and create a pull request.
6. Add the appropriate labels as required by the repo. To learn which labels to add, refer to the contribution documentation for that repo or reach out to the file codeowners.

:::{note}
Backports can be complicated. You can use the [backport tool](https://github.com/sorenlouv/backport) to manage backporting your changes to other version branches.
:::

## Contribute locally

For complex or multi-page updates to `elastic.co/guide` (Asciidoc) documentation, refer to the [Asciidoc documentation build guide](https://github.com/elastic/docs?tab=readme-ov-file#building-documentation).

## Updating docs in both systems

If you need to merge changes that are published in both systems (usually because a change is valid in multiple product versions, such as stack 9.x and 8.x), it is recommended to update the documentation in elastic.co/docs first. Then you can convert the updates to ASCIIDoc and make the changes to the elastic.co/guide documentation. To do this, follow these steps:

1. Install [pandoc](https://pandoc.org/installing.html) to convert your markdown file to ASCIIDoc
2. Update the /docs content first in Markdown as described in [Contribute on the web](on-the-web.md) in the relevant repository.
3. Run your changes through pandoc:
   1. If you need to bring over the entire file, you can run the following command and it will create an ASCIIDoc file for you: `pandoc -f gfm -t asciidoc ./<file-name>.md -o <file-name>.asciidoc`
   2. If you just need to port a specific section you can use: `pandoc -f gfm -t asciidoc ./<file-name>.md` and the output of the file will be in your command window from which you can copy.
4. Follow the steps in [Contribute on the web](#contribute-on-the-web) to publish your changes.
5. If the change is too large or complicated, create a new issue in the [`docs-content`](https://github.com/elastic/docs-content) or [`docs-content-internal`](https://github.com/elastic/docs-content-internal) repository detailing the changes made for the team to triage.
6. Merge the changes and close the issue (if applicable) once the updates are reflected in the documentation.
