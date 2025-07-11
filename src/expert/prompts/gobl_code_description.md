This tool enables searching across the following GitHub repositories on their main branches:  
- `invopop/gobl`  
- `invopop/gobl.verifactu`  
- `invopop/gobl.fatturapa`
- `invopop/gobl.cfdi`
- `invopop/gobl.ubl`
- `invopop/gobl.cii` 

When used, the tool should:

- Return natural language explanations of the results.
- Include relevant code or documentation excerpts.
- Always cite the file path and location within the invopop/gobl repo where the content originated.

All the sources must be in this format: `https://github.com/{repository_name}/tree/main/{file_path}`. This means that if the source received is `addons/de/zugferd/zugferd.go` from searching in `invopop/gobl`, the URL to the source that you should cite is `https://github.com/invopop/gobl/tree/main/addons/de/zugferd/zugferd.go`.

---

## Repository Overview & Selection Criteria

### `invopop/gobl`
This is the **core repository** of the GOBL system and the foundation of the Invopop project.

**Use this repository when a query:**
- Asks about the format, schema, and fields of any GOBL document like lines, parties, taxes, totals, extensions and more. 
- Asks about the specific gobl fields that need to be included for specific regime (country) or addon (invoice format)
- Asks about addons. An addon represents the validations, normalizations and extensions included for a specific invoice format. For instance, when the `mx-cfdi-v4` addon is applied to an invoice it will ensure that the validations and extensions are performed to be ready to processed by the conversor from GOBL to CFDI. The supported addons are `peppol`, `es-verifactu`, `it-sdi`, `it-ticket`, `de-zugferd`, `de-xrechnung`, `en16931`, `fr-choruspro`, `fr-facturx`, `mx-cfdi-v4`, `pt-saft`, `br-nfse`, `co-dian`

### `invopop/gobl.verifactu`
A **conversion library** focused on transforming GOBL invoices into the Spanish **VeriFactu** format and submitting them to the AEAT. It handles specific Spanish legal requirements, such as invoice chaining and digital signatures.

**Use this repository when a query:**
- Is about how a specific GOBL field maps to the **VeriFactu** format.
- Involves an error or issue during conversion to VeriFactu.

### `invopop/gobl.fatturapa`
A **conversion library** for converting between GOBL and **Italian FatturaPA electronic invoicing XML** formats and submitting to SDI. 

**Use this repository when a query:**
- Asks how specific GOBL fields are mapped to or from Fatturapa.
- Involves conversion errors between GOBL and Fatturapa format.

### `invopop/gobl.cfdi`
A **conversion library** focused on transforming GOBL invoices into the Mexican **CFDI** (Comprobante Fiscal Digital por Internet) XML format.

**Use this repository when a query:**
- Is about how a specific GOBL field maps to the **CFDI** format.
- Involves an error or issue during conversion to CFDI.

### `invopop/gobl.ubl`
A **conversion library** focused on converting between GOBL and **UBL (Universal Business Language)** formats, including variants like **EN16931**, **PEPPOL**, **FacturX**, and **X-Rechnung**.

**Use this repository when a query:**
- Asks how specific GOBL fields are mapped to or from UBL or one of its variants.
- Involves conversion errors between GOBL and UBL formats.

### `invopop/gobl.cii`
A **conversion library** focused on converting between GOBL and **CII (Cross Industry Invoice XML format)** format. It is a bridge between GOBL and various European e-invoicing formats including  **EN16931**, **XRechnung**, **FacturX**, and **ChorusPro**.

**Use this repository when a query:**
- Asks how specific GOBL fields are mapped to or from CII.
- Involves conversion errors between GOBL and CII formats.

---

## ⚠️ General Guidance

- **Do not use this tool** for unrelated questions, such as general programming topics (e.g. “How do I configure VSCode?”).
- Query the tool in English
