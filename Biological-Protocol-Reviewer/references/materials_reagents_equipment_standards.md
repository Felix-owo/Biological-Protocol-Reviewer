# Materials, Reagents, Consumables, Equipment, and Reagent-Setup Standards

## Purpose

This reference defines the minimum acceptable detail for all Materials, Equipment, Reagent setup, and Appendix recording tables in a revised protocol. The goal is that a trained user can purchase the correct resources, reproduce the method, audit deviations, and replace missing information with justified best-in-class recommendations.

Key resource identity is a release gate. Antibodies, cell lines, animal strains, kits, enzymes, instruments, software, sequencing chemistries, reference databases, primers/oligos/barcodes/gRNAs, and analytical resources must be identified as completely as the source protocol and authoritative sources allow. If a field is unknown, mark it `△TO BE CONFIRMED` and state whether execution can proceed before confirmation.

## Mandatory rule

A revised protocol must not contain generic material entries such as `antibody`, `PCR mix`, `centrifuge`, `flow cytometer`, `lysis buffer`, `cell strainer`, or `kit` without sufficient identifiers. Every entry must be converted into a traceable record.

If the original protocol does not specify a required item, the skill must:

1. Recommend an appropriate gold-standard or commonly accepted option when it can be selected from official vendor documentation, peer-reviewed protocol papers, top-journal methods, or core-facility practice.
2. Mark the item as `RECOMMENDED — TO BE VERIFIED LOCALLY`.
3. Provide the rationale for the recommendation in the review report.
4. Avoid falsely claiming the recommended item was in the original protocol.
5. Leave truly non-identifiable parameters as `TO BE CONFIRMED` with a validation plan.

## Key resources table requirement

Every `Revised_Protocol.md` must contain a Key Resources Table in the Materials section. The table must include, as applicable:

| Category | Required fields |
|---|---|
| Biological samples | Species/source, strain/background, sex/age if relevant, genotype, vendor/source, stock/strain ID, RRID if available, storage/handling, approval record |
| Cell lines | Cell line name, source/vendor, catalog/identifier, RRID if available, authentication method/date, mycoplasma test date, passage range, culture condition |
| Antibodies | Target, fluorophore/conjugate, clone, host/isotype, vendor, catalog number, RRID if available, lot number, working dilution or amount per cells/test, storage, expiration, validation status |
| Oligos/primers/probes | Name, sequence, modification, vendor, scale/purification, stock concentration, working concentration, storage, expiration, target amplicon or assay role |
| Enzymes/kits | Name, vendor, catalog number, lot number, unit concentration, storage, freeze-thaw limit, expiration, critical handling notes |
| Chemicals/reagents | Name, grade, vendor, catalog number, lot number, stock concentration, working concentration, storage, expiration, hazard notes when relevant |
| Buffers/media | Name, formulation, supplier or preparation recipe, pH/osmolality if relevant, sterile filtration, storage, expiration |
| Consumables | Item, material/format, sterile/low-bind/DNase-RNase-free status, vendor, catalog number, lot number, use step |
| Equipment | Instrument name, vendor, model, serial/core ID, configuration, calibration requirement, software version, settings to record |
| Software/databases | Name, version, vendor/source, RRID or DOI if available, parameters, repository link if applicable |

## Antibody-specific standard

For every antibody, require:

- Target antigen
- Fluorophore or conjugate
- Clone
- Host species and isotype when relevant
- Vendor
- Catalog number
- Lot number record field
- RRID if available
- Recommended amount per test or per 10^6 cells
- Titration status
- Storage condition
- Expiration date or validated use-by date
- Protected-from-light requirement for fluorophore-conjugated antibodies
- Relevant FMO and compensation control requirements for flow cytometry

If the original protocol gives only target and fluorophore, recommend a clone/catalog only when a defensible standard exists. Otherwise write `clone/catalog TO BE CONFIRMED` and add `perform antibody titration and validation before production run`.

## Reagent setup requirement

Every prepared reagent must have a dedicated reagent setup table with:

- Reagent name
- Purpose/use step
- Components with vendor/catalog if critical
- Stock concentrations
- Final concentrations
- Exact volumes for a defined final volume
- Preparation order
- Mixing method
- Filtration/sterilization requirement
- Aliquot size
- Storage condition
- Expiration/shelf life
- Freeze-thaw limit
- Light sensitivity
- Pre-use QC acceptance criteria, such as clarity, pH, sterility, color, precipitate, activity, or concentration
- Disposal notes when relevant

If shelf life is unavailable, set a conservative default such as `prepare fresh`, `same day`, or `validate locally`, and mark `RECOMMENDED — TO BE VERIFIED LOCALLY`.

## Equipment settings requirement

Every equipment-dependent procedure must include a settings table. Examples:

- Centrifuge: rotor type, RCF in ×g, temperature, time, acceleration/deceleration if critical.
- Flow sorter: model, nozzle, pressure, laser/filter configuration, sort mode, drop delay calibration, threshold, event rate, abort rate, temperature, index sort setting.
- Thermocycler: model, lid temperature, ramp mode if relevant, program name, cycle settings.
- Sequencer: model, kit, read structure, index structure, loading concentration, run mode.
- Microscope: objective, numerical aperture, exposure, gain, illumination power, binning, pixel size, z-step, software version.

Do not report centrifugation in rpm unless rotor radius is provided; use ×g as the primary standard.

## Missing-resource recommendation policy

When the original protocol lacks a brand/catalog/clone:

1. Search authoritative sources if web/literature access is available.
2. Prefer resources used in peer-reviewed protocols or top-journal methods.
3. Prefer official vendor products matching the stated method when a kit/manual is referenced.
4. For antibodies, prefer clones validated for the relevant species, sample type, and application.
5. For instruments, specify a functional class and record fields if a single model cannot be assumed.
6. Mark every recommendation clearly as `RECOMMENDED — TO BE VERIFIED LOCALLY`.
7. Add a local validation requirement: titration, pilot run, positive/negative control, side-by-side comparison, or acceptance criterion.

## Review report requirements

`Review_Report.md` must include a `Resource completeness audit` section with:

- Number of material/resource entries in original protocol.
- Number missing vendor.
- Number missing catalog number.
- Number missing clone/RRID when applicable.
- Number missing lot/expiration/storage record fields.
- Number requiring recommended replacements.
- Critical resources that cannot be safely inferred.

## Markdown appendix requirements

`Revised_Protocol.md` must include appendices for:

- Appendix C: Reagent, antibody, kit, consumable, and lot record table.
- Appendix D: Equipment, software, calibration, and settings record table.
- Appendix I: Prepared reagent batch record and expiration log.


## Chinese/Nature Protocols-style resource notation

In Chinese output, all prepared reagents must use the `◉EXPDATE` marker to state storage and shelf life. All critical reagent source constraints must use `▲CRITICAL`. All recommended substitutions must use `★RECOMMENDED — TO BE VERIFIED LOCALLY`, and all unknown source details must use `△TO BE CONFIRMED`.
