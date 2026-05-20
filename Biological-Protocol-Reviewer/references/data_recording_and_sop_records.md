# Data recording and SOP records

A publication-grade protocol must be auditable. Every experimental run should be reconstructable from records without relying on memory.

Apply an operator burden budget: every added record must support a failure-mode, QC, governance, reproducibility, traceability, or data-reanalysis need. If the value is mainly publication/audit context, move it to an appendix rather than the bench-facing main body.

## Mandatory record types

1. SOP control record
2. Study design record
3. Animal/cell/sample provenance record
4. Reagent and consumable lot record
5. Equipment, software, and instrument settings record
6. QC release record
7. Deviation and exclusion log
8. Raw-data inventory
9. Downstream analysis manifest
10. Operator and reviewer sign-off

## Minimum table fields

### SOP control
- SOP title
- SOP ID
- Version
- Author
- Reviewer
- Approver
- Effective date
- Revision history
- Change rationale

### Experiment run sheet
- Run ID
- Date
- Operator
- Protocol version
- Experimental group
- Biological replicate
- Technical replicate
- Start/end time
- Deviations
- Pass/fail

### Sample provenance
- Sample ID
- Source organism/cell line/tissue
- Genotype/strain/sex/age/weight when applicable
- Treatment group
- Collection method
- Collection time
- Processing start time
- Storage condition
- Freeze-thaw count

### Reagent lot table
- Reagent name
- Vendor
- Catalog number
- Lot number
- Clone when applicable
- Concentration
- Preparation date
- Expiration date
- Storage condition
- Operator

### Instrument settings
- Instrument name
- Model
- Serial/core facility ID
- Configuration
- Calibration status
- Software version
- Acquisition/sort settings
- File output path

### QC release
- QC checkpoint
- Acceptance criterion
- Observed value
- Pass/fail
- Corrective action
- Disposition

### Deviation/exclusion log
- Item ID
- Deviation or exclusion
- Root cause
- Impact on interpretation
- Corrective action
- Approved by

### Raw-data inventory
- File ID
- File name
- File type
- Instrument/software source
- Acquisition date
- Sample IDs represented
- Storage path
- Backup status
- Checksum if available

For omics, flow, imaging, and computational outputs, add FAIR/data-quality fields where feasible:

- software and version;
- instrument settings or settings file path;
- reference genome/database/library version;
- processing command, workflow, or pipeline version;
- QC metric and pass/fail status;
- analysis rerun status for publication-grade outputs.


# Governance and Qualification Records

Every revised SOP must include records proving that the procedure is executed under appropriate oversight. If the uploaded draft does not provide these values, insert the fields and mark them `TO BE COMPLETED BEFORE EXECUTION`. Do not use missing values as a reason to withhold a complete SOP.

Minimum governance fields:

- Responsible PI / supervisor
- Approval category: IACUC, IRB, IBC, biosafety, chemical safety, radiation safety, core facility, or equivalent
- Approval identifier and expiration date
- Approved procedure title
- Approved biological material, species, strain, cell type, vector, or sample source
- Approved facility, room, instrument, or core facility
- Required personnel training and competency verification
- PPE and containment requirements
- Waste stream and decontamination route
- Emergency contact and incident/deviation reporting procedure
