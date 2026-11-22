# Haro Release B Governance: Founding Proposal v2

Status: PROPOSAL, submitted for independent review. Not adopted. Nothing in this document is in effect.

This file is never edited to record a review outcome. Outcomes exist only as signed review records that cite this version's SHA-256 (section 8). Any edit creates a new version.

## 1. Version

- Version: v2. Replaces v1 (commit `596cab230401074b2232c68455a4d603259ec48f`, SHA-256 `09bf7c85acb5c09ac9126d90f2d1978c3e052f709fb87a4e9445ee13ace3e389`), which was not adopted.
- Canonical bytes: this file as stored in Git, UTF-8 without BOM, LF line endings, ending with one newline. `.gitattributes` keeps these bytes identical on every platform.
- Identifier: the SHA-256 of the canonical bytes. It is published in the pull request that adds this version and repeated in every signed record that refers to it.

## 2. Remit

- In scope: deciding who may issue governance policy for Haro Factory Release B, and who may receive authority inquiries about it.
- Out of scope: the technical content of Release B, and any decision about a specific release.
- The working name "Haro Release B Governance" identifies this proposal only and confers no status.

## 3. Non-authorization

This proposal issues no grant or registration, appoints no one, opens no case, and authorizes no release, root change, or dispatch.

A GitHub review or approval of a pull request that adds this file is a repository merge control. It is not a signature, grant, registration, or receipt under this proposal.

## 4. Roles

| Role | Account (numeric ID) | Function | Status |
|---|---|---|---|
| Owner | `mmibu1939-debug` (264738043) | Owner of the Haro Factory project repository. Submits this proposal. | Candidate |
| Reviewer | `mashimashiman-max` (359733728) | Independent reviewer. Owner of `haro-trust-governance` (repository ID 1467202772). | Candidate; review requested |
| Custodian | none | Maintains the trust anchor. | Vacant; no one has accepted an appointment |
| Witness | none | Receives cases and returns signed case receipts. | Not designated |

- Accounts are identified by numeric ID. Logins are informational because they can change.
- Owning `haro-trust-governance` does not make the Reviewer an Owner under this proposal.
- Haro Factory project repository: a private GitHub repository owned by account 264738043, identified by its root commit `fbf43fd7930086a145aae10e9f5cb77a0ab1f4ca`. Its name is disclosed to the Reviewer on request.

## 5. Definitions

- Founding mandate: the Owner's signed act that establishes the governance body, fixes its remit (section 2), and delegates authority to it.
- Trust anchor: the protected list of principals and public keys against which governance signatures are verified.
- Verifier: the published procedure, and any tool, that checks a signature against the trust anchor and section 7.
- Activation: the point from which the governance body may issue policy and open cases (section 9).
- Authority inquiry: a question about who may authorize a specific action for Release B.
- Case: an authority inquiry formally opened under an adopted intake policy. No case can be opened before activation.
- Case receipt: the Witness's signed acknowledgment of a case, covering the case content, its case number, and an independently verifiable time.
- Grant: a signed assignment of authority, a role, or a key scope to a principal.
- Registration: a principal's signed enrollment of their own public key in the trust anchor.
- Root change: adding, removing, or replacing a principal or key in the trust anchor.
- Dispatch: starting any automated action that acts on Haro Factory, including workflow runs, deployments, and release publication.
- Independent: meeting every requirement in section 6.

## 6. Independence

- I-1. The Owner and the Reviewer are different natural persons. Two accounts controlled by one person do not meet this requirement.
- I-2. Neither party holds, shares, or can use the other's account credentials, authenticators, signing keys, devices, or recovery channels.
- I-3. Each party's decisions and signatures are their own. An AI agent, bot, or automation may assist with drafting or analysis but MUST NOT decide, approve, or sign for anyone.
- I-4. Before signing for any other purpose in S-4, each party signs a declaration that I-1 to I-3 hold (purpose `haro-independence`).
- I-5. The Owner SHOULD NOT have write access to this repository, and proposals SHOULD come from a fork. v1 was submitted from a branch in this repository, so the Owner account currently has write access. That access also lets it run workflows on other branches that produce attestations under this repository's identity. If the access is kept, the reason is recorded before activation. Either way, verifiers MUST pin the workflow path and `refs/heads/main` (S-6).

## 7. Signing and verification

- S-1. Governance signatures are made only by natural persons, each using their own hardware-bound FIDO2 authenticator that requires user presence for every signature. Software-only, shared, or automation-accessible keys are not acceptable.
- S-2. No AI agent, bot, or automation may hold a governance key or use one on a principal's behalf.
- S-3. A signature covers the exact canonical bytes it signs, identified by their SHA-256, and is made for exactly one purpose in S-4. A signature made for one purpose is not valid for another.
- S-4. Stated purposes:

| Stage | Signer | Purpose | Namespace (S-5) |
|---|---|---|---|
| Proposal | Owner | Submit this exact version and confirm the facts it states about the Owner | `haro-founding-submit` |
| Proposal | Reviewer | Sign the review record for this exact version (section 8) | `haro-founding-review` |
| Activation | Owner | Issue the founding mandate and policy | `haro-founding-issue` |
| Activation | Reviewer | Countersign the same mandate and policy as the independent party | `haro-founding-countersign` |
| Any | Owner, Reviewer | Independence declaration (I-4) | `haro-independence` |

- S-5. Proposed profile, open for review: OpenSSH signatures (`ssh-keygen -Y sign`) made with FIDO2 `sk` keys, with the purpose carried as the signature namespace. The trust anchor is an `allowed_signers` file in this repository, changed only as a root change, in which each key is limited to its role's namespaces (`namespaces=`) and validity period (`valid-after`, `valid-before`).
- S-6. Workflow attestations, such as those from `attest-approval.yml`, record what a workflow observed. They are evidence, never a principal's signature. Verifiers MUST pin the repository, the workflow path, and `refs/heads/main` (with `gh attestation verify`: `--repo`, `--signer-workflow`, `--source-ref`).
- S-7. Every signed record and case receipt carries independently verifiable time and ordering, such as an RFC 3161 timestamp from a named timestamp authority or an inclusion proof in a public transparency log. Git commit dates are set by the committer and GitHub timestamps are asserted by the platform, so neither is sufficient alone.
- S-8. Signed records are self-verifying. Their validity does not depend on where they are stored or on any merge.

## 8. Decision requested

The Reviewer is asked to sign a review record (purpose `haro-founding-review`) that states:

- the SHA-256 of the reviewed version;
- one outcome: ACCEPT-AS-BASIS (the remit is an acceptable basis for drafting a founding mandate and policy; this activates nothing), CHANGES-REQUESTED (with the changes required), or REJECT (with reasons);
- answers to Q-1 to Q-3;
- the Reviewer's numeric account ID.

Questions:

- Q-1. Is the remit in section 2 appropriately bounded?
- Q-2. Does a valid founding mandate exist, and does an independent custodian exist? If not, what would establish them?
- Q-3. What evidence is required before a purpose-limited signing and intake policy can be adopted?

Merging the pull request that adds a version archives that version. It does not record or imply any outcome.

## 9. Activation conditions

Activation requires all of the following, each recorded under section 7. None is met by this version.

- A-1. The text of the founding mandate is final, and it fixes the remit (section 2) and the authority delegated to the governance body.
- A-2. A custodian has accepted appointment in a signed statement, and the trust anchor is designated.
- A-3. A verifier procedure that implements section 7 against that trust anchor is published.
- A-4. The adopted policy identifies, for each delegated principal: numeric account ID, key fingerprint, scope, validity period, revocation authority, and recovery boundary. It also sets signing thresholds for root changes, forbids any principal from approving their own submission, and states how the policy is amended.
- A-5. A Witness is designated, and the intake policy requires a signed case receipt with independently verifiable ordering and time (S-7) for every case.
- A-6. The Owner and the Reviewer have each signed the same version of the founding mandate and policy for their activation purposes (S-4), and each has signed the independence declaration (I-4).

Activation takes effect at the time established under S-7 for the later of the two A-6 signatures.

## 10. Inquiry references

| Reference | SHA-256 | Preimage location | Hashed bytes |
|---|---|---|---|
| Original inquiry | `ee0d9613dcd0a0fdd325e64b8c0315f2191033a39b705126400d5d14e5b92901` | Not public; provided to the Reviewer on request | Exact bytes of `PUBLIC_AUTHORITY_REQUEST.json` (3043 bytes), no normalization |
| Follow-up inquiry 00 | `50022a2c53410941c697ada3e3835d6118e343c25c1a9e54b2ac127344a0e87b` | Not public; provided to the Reviewer on request | Exact bytes of `00-inquiry.json` (2182 bytes), no normalization |

The preimages are not published. The Owner provides them privately at the Reviewer's request, and the Reviewer recomputes each SHA-256 before accepting a preimage as evidence.

## 11. Open items

- O-1. Resolved: the project repository is identified by its root commit (section 4).
- O-2. Resolved: the hashed bytes are stated, and the preimages are provided on request (section 10).
- O-3. The Owner's write access to this repository (I-5).
- O-4. The Custodian and Witness roles are vacant (section 4).

O-3 and O-4 are resolved before activation.

## 12. Changes from v1

- Moved the decision, outcomes, and review questions from the pull request description into this document, so the signed bytes cover them.
- Added roles keyed by numeric ID, definitions, and stated signing purposes.
- Added numbered independence, signing, verification, and activation requirements.
- Stated the hashed bytes and disclosure route of the inquiry references, and identified the project repository by its root commit.
- Defined the version identifier, canonical bytes, and the meaning of a merge.
