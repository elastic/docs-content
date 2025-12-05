---
navigation_title: Vale style checker
---

# Elastic style guide for Vale

[Vale](https://github.com/errata-ai/vale) is a prose linter that checks documentation in Markdown format against the [Elastic style guide](/contribute-docs/style-guide/index.md). The documentation is checked when you commit changes to a pull request.

Follow the instructions on this page to:

- [Use the Vale action for GitHub](/contribute-docs/vale-linter.md#vale-checks-in-pull-requests) to check for style issues when you commit changes to a pull request.
- [Use the Vale linter in your IDE](/contribute-docs/vale-linter.md#use-the-vale-linter-locally) to check for style issues while writing documentation.

## Vale checks in pull requests [vale-checks-in-pull-requests]

The Vale action for GitHub runs Vale checks on pull requests that include documentation changes. The action reports any style issues found in modified lines in the form of a sticky comment.

:::{image} ./images/vale-sticky-comment.png
:alt: Vale comment in pull request
:screenshot:
:width: 85%
:::

Issues are reported in the form of errors, warnings, and suggestions. You can expand each category to browse the specific issues. The report updates every time you commit changes.

:::{important}
Make an effort to fix all warnings and suggestions reported by the Vale linter. This helps ensure your docs read well and are easier to understand.
:::

## Use the Vale linter locally [use-the-vale-linter-locally]

You can use the Vale linter locally to check for style issues while writing documentation.

::::::{stepper}

:::::{step} Install Vale and the Elastic style
Run these commands to install the Elastic style guide locally. If Vale isn't installed, the commands install it for you or suggest how to do it.

::::{tab-set}

:::{tab-item} macOS

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/vale-rules/main/install-macos.sh | bash
```

:::

:::{tab-item} Linux

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/vale-rules/main/install-linux.sh | bash
```

:::

:::{tab-item} Windows

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/elastic/vale-rules/main/install-windows.ps1 -OutFile install-windows.ps1
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

:::
::::

:::{tip}
To update the Elastic style guide to the latest rules, rerun the installation script.
:::
:::::

:::::{step} Install the IDE extension
Install the [Vale VSCode](https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode) extension. The extension is also available for other editors that support the Open VSX Registry, like Cursor.
:::::

:::::{step} Open any Markdown file
The extension automatically runs Vale checks when you save a document. Issues are reported both in the Problems tab and in the editor itself.

:::{image} ./images/vale-ide.png
:alt: Vale comment in pull request
:screenshot:
:width: 100%
:::
:::::

::::::

## Style rules reference [elastic-style-rules-reference]

The following table lists all the rules included in the [Elastic Vale style package](https://github.com/elastic/vale-rules/tree/main/styles/Elastic):

| Rule        | Description |
|-------------|-------------|
| [Accessibility](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Accessibility.yml) | Flags ableist language that defines people by their disability. Refer to [Avoid violent, offensive, ableist terminology](./style-guide/accessibility.md#avoid-violent-offensive-ableist-terminology). |
| [Acronyms](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Acronyms.yml) | Checks that acronyms are defined before being used (unless they're common exceptions). Refer to [Abbreviations and acronyms](./style-guide/grammar-spelling.md#abbreviations-and-acronyms). |
| [Articles](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Articles.yml) | Ensures correct article usage ("a" vs "an") based on pronunciation, not spelling. Refer to [Using the right article](./style-guide/grammar-spelling.md#using-the-right-article). |
| [BritishSpellings](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/BritishSpellings.yml) | Suggests American English spellings instead of British English variants. Refer to [American English](./style-guide/grammar-spelling.md#american-english). |
| [Capitalization](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Capitalization.yml) | Checks that headings use sentence-style capitalization. Refer to [Capitalization](./style-guide/grammar-spelling.md#capitalization). |
| [ConflictMarkers](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/ConflictMarkers.yml) | Detects Git merge conflict markers in source code. |
| [DeviceAgnosticism](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/DeviceAgnosticism.yml) | Suggests device-agnostic language (for example, "select" instead of "tap"). Refer to [Use device-agnostic language](./style-guide/accessibility.md#accessibility-guidelines). |
| [Dimensions](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Dimensions.yml) | Suggests using "MxN" format instead of "M X N" for dimensions. Refer to [Dimensions](./style-guide/formatting.md#dimensions). |
| [DontUse](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/DontUse.yml) | Flags words and phrases that shouldn't be used (for example, "please", "just", "aka"). Refer to [Word choice](./style-guide/word-choice.md). |
| [Ellipses](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Ellipses.yml) | Discourages the use of ellipses. Refer to [Write like a minimalist](./style-guide/voice-tone.md#write-like-a-minimalist). |
| [EmDashes](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/EmDashes.yml) | Checks that em dashes don't have spaces before or after. Refer to [Em dashes](./style-guide/grammar-spelling.md#em-dashes). |
| [EndPuntuaction](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/EndPuntuaction.yml) | Flags headings that end with punctuation. Refer to [Capitalization](./style-guide/grammar-spelling.md#capitalization). |
| [Exclamation](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Exclamation.yml) | Encourages sparing use of exclamation points. Refer to [Tone](./style-guide/voice-tone.md#tone). |
| [FirstPerson](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/FirstPerson.yml) | Discourages first-person pronouns (I, me, my, mine). Refer to [Use singular first-person pronouns sparingly](./style-guide/grammar-spelling.md#use-singular-first-person-pronouns-sparingly-i-me-my-mine). |
| [FutureTense](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/FutureTense.yml) | Encourages writing in present tense instead of future tense. Refer to [Verb tense](./style-guide/grammar-spelling.md#verb-tense). |
| [Gender](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Gender.yml) | Flags gender-specific compound pronouns like "he/she" or "s/he". Refer to [Use gender-neutral language](./style-guide/accessibility.md#use-gender-neutral-language). |
| [GenderBias](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/GenderBias.yml) | Suggests gender-neutral alternatives for gendered terms. Refer to [Use gender-neutral language](./style-guide/accessibility.md#use-gender-neutral-language). |
| [HeadingColons](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/HeadingColons.yml) | Checks that text after colons in headings is capitalized. Refer to [Colons](./style-guide/grammar-spelling.md#colons). |
| [Latinisms](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Latinisms.yml) | Suggests plain English alternatives to Latin terms (for example, "for example" instead of "e.g."). Refer to [Latin abbreviations](./style-guide/grammar-spelling.md#latin-abbreviations). |
| [MeaningfulCTAs](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/MeaningfulCTAs.yml) | Flags non-descriptive link text like "click here". Refer to [Use meaningful link text](./style-guide/accessibility.md#accessibility-guidelines). |
| [Negations](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Negations.yml) | Suggests rephrasing negative constructions to positive ones. Refer to [Write for an international audience](./style-guide/accessibility.md#write-for-an-international-audience). |
| [OxfordComma](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/OxfordComma.yml) | Enforces the use of the Oxford comma in lists. Refer to [Commas](./style-guide/grammar-spelling.md#commas). |
| [PluralAbbreviations](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/PluralAbbreviations.yml) | Flags apostrophes in plural abbreviations (use "APIs" instead of "API's"). Refer to [Making abbreviations plural](./style-guide/grammar-spelling.md#making-abbreviations-plural). |
| [QuotesPunctuation](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/QuotesPunctuation.yml) | Ensures punctuation is placed outside quotation marks. Refer to [Punctuation](./style-guide/grammar-spelling.md#punctuation). |
| [Repetition](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Repetition.yml) | Detects repeated words. Refer to [Write like a minimalist](./style-guide/voice-tone.md#write-like-a-minimalist). |
| [Semicolons](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Semicolons.yml) | Encourages judicious use of semicolons. Refer to [Semicolons](./style-guide/grammar-spelling.md#semicolons). |
| [Versions](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Versions.yml) | Suggests "later" or "earlier" instead of "newer", "older", "higher", or "lower" for versions. |
| [WordChoice](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/WordChoice.yml) | Suggests preferred word choices (for example, "stop" instead of "abort", "allowlist" instead of "whitelist"). Refer to [Word choice](./style-guide/word-choice.md). |
| [Wordiness](https://github.com/elastic/vale-rules/blob/main/styles/Elastic/Wordiness.yml) | Suggests concise alternatives to wordy phrases. Refer to [Write like a minimalist](./style-guide/voice-tone.md#write-like-a-minimalist). |

## Vocabularies [elastic-vocabularies]

The Elastic Vale style uses [Vale vocabularies](https://vale.sh/docs/keys/vocab) to recognize product and feature names. Vocabularies help Vale avoid false positives when checking capitalization and spelling rules.

The Elastic style includes these vocabularies:

- [**ElasticTerms**](https://github.com/elastic/vale-rules/blob/main/styles/config/vocabularies/ElasticTerms/accept.txt): Contains Elastic product and feature names (for example, Elasticsearch, Kibana, Elastic Agent).
- [**ThirdPartyProducts**](https://github.com/elastic/vale-rules/blob/main/styles/config/vocabularies/ThirdPartyProducts/accept.txt): Contains non-Elastic product names (for example, Kubernetes, AWS, Docker).

:::{tip}
If Vale incorrectly flags a product or feature name, suggest adding it to the appropriate vocabulary by creating a pull request or issue in the [Elastic Vale rules repository](https://github.com/elastic/vale-rules).
:::

## Report issues or suggest improvements [report-issues-or-suggest-improvements]

You can report issues or suggest improvements to the Elastic style guide by creating an issue in the [Elastic Vale rules repository](https://github.com/elastic/vale-rules/issues).

## Additional resources [additional-resources]

- [Vale's official documentation](https://vale.sh/docs/vale-cli/overview/)
- [Elastic Vale rules repository](https://github.com/elastic/vale-rules)
