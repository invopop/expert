This tool allows searching the invopop/gobl GitHub repository (main branch) to retrieve relevant code snippets.

The `invopop/gobl` repository is a comprehensive business document processing library that standardizes the creation, validation, calculation, and digital signing of commercial documents such as invoices, payments, deliveries, and orders. Built in Go with WebAssembly support, GOBL provides precise tax calculations, country-specific compliance rules, and multiple distribution channels including CLI tools, HTTP APIs, and browser-compatible modules.

This tool should only be used when a user query is:

- Clearly or implicitly related to the invopop/gobl project.
- Refers to invoicing, invoice formats, validation, payments, lines, totals, tax rules, country-specific rules, or similar GOBL schema fields.

Avoid using this tool if the question is clearly about a different topic, unrelated to the GOBL domain or invoicing in general. For instance, if the question is `How do I configure vscode?` do not use this tool.

When used, the tool should:

- Return natural language explanations of the results.
- Include relevant code or documentation excerpts.
- Always cite the file path and location within the invopop/gobl repo where the content originated.

All the sources are in the following URL: https://github.com/invopop/gobl/tree/main. This means that if the source received is addons/de/zugferd/zugferd.go, the URL to the source that you should cite is https://github.com/invopop/gobl/tree/main/addons/de/zugferd/zugferd.go.