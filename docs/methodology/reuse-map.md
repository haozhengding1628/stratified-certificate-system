# Reuse Map: From Representation Theory To Linear Algebra

This document describes the reusable methodology behind a
certificate-driven classification project. It is intentionally source-agnostic:
it does not include private parameters, research data, paper-specific
certificates, local paths, or unpublished classification artifacts.

## Core Thesis

Many finite-dimensional representation-theoretic classification problems can be
made tractable by reducing them to parameterized linear algebra:

```text
family of finite-dimensional modules over an algebraic parameter space
  -> structural question
     (simplicity, maximal submodule, head dimension, Hom, reducible locus)
  -> rank/kernel/cokernel question for polynomial matrices
  -> rank-drop locus cut out by determinantal ideals
  -> stratification plus certificate checks on each stratum
```

The key prerequisite is a **linearizing structure**: a reason that the
representation-theoretic question can be tested by kernels, ranks, radicals, or
orbits of explicitly computable matrices.

## Linearization Routes

Two common routes produce the same kind of certificate ledger.

| Route | Mechanism | Typical certificate |
| --- | --- | --- |
| Degree-lowering or singular-vector reduction | Every nonzero submodule contains a vector killed by a chosen positive part, so submodule detection becomes a singular-kernel problem. | Kernel basis, rank certificate, orbit/fullspan certificate |
| Contravariant, Gram, or cellular form | The radical of a bilinear form controls the maximal submodule or simple head. | Gram rank, determinant factorization, radical dimension |

The first route is useful when an Engel-type or triangular structure forces
singular vectors to appear. The second route is broader: once a Gram or
contravariant form is available, the same stratification and certification
machinery applies.

## Reusable Pipeline

1. **Choose the finite model.**
   Fix a finite-dimensional quotient, truncation, standard module, cell module,
   or finite weight space where all operators are finite matrices.

2. **Build parameterized matrices.**
   Express action matrices, Gram matrices, Hom equations, quotient action
   matrices, or orbit matrices over a polynomial coordinate ring.

3. **Identify structural invariants.**
   Record the invariants to classify, such as kernel dimension, radical
   dimension, quotient dimension, simple-head dimension, or Hom dimension.

4. **Compute the generic behavior.**
   Find rank witnesses, determinant witnesses, pivot charts, or fullspan minors
   on dense opens.

5. **Control rank-drop loci.**
   Use determinantal ideals, primary decomposition when feasible, localization,
   and saturation to turn generic evidence into pointwise evidence on each
   stratum.

6. **Bridge machine evidence to mathematics.**
   For each row, state how the certificate implies the theorem-level claim:
   rank controls a kernel, a kernel controls singular vectors, orbit fullspan
   proves cyclicity, and cyclicity or radical control proves simplicity or
   maximality.

7. **Separate proof from validation.**
   Finite-field replay, random checks, and independent CAS runs are valuable
   guardrails, but they should be marked as validation unless the theorem itself
   is finite-field.

## Domains Where The Pattern Reuses Well

### Highest-Weight And Standard-Module Theory

Shapovalov or contravariant forms reduce reducibility and head dimensions to
determinants and Gram ranks. In Kac-Moody, affine, Lie-super, quantum-group, and
Virasoro/VOA settings, determinant factors describe rank-drop loci in parameter
space. Jantzen-style filtrations can often be read from valuations of these
forms after specialization.

### Modular Representation Theory

Weyl modules, Specht modules, Hecke modules, and related standard modules often
carry explicit integral or modular Gram matrices. Simple-head dimensions become
rank computations after specialization. Decomposition-number problems can then
be organized as certificate ledgers around Gram ranks and radical dimensions.

### Cellular Algebras

Cellular algebras are a particularly clean target. Each cell module has a Gram
form, and the simple quotient is controlled by the rank of that form. Examples
include Temperley-Lieb, Brauer, BMW, partition, cyclotomic Hecke, and KLR-type
settings. In these problems, the singular-vector module can be replaced by a
cell-module Gram-matrix module while keeping the same stratification workflow.

### Rational Cherednik And Parameterized Category O Problems

Standard modules in parameterized category O settings often have reducibility
or asphericity loci described by hyperplane arrangements or determinantal
conditions. The certificate structure maps naturally to parameter strata,
rank-drop loci, and specialization checks.

### Quiver, Hom, Ext, Branching, Tensor, And Fusion Problems

Many structural questions can be written as linear systems. A Hom space is the
kernel of intertwining equations; Ext computations can be reduced to kernels
and cokernels of explicit maps; branching, tensor-product, and fusion rules
often become rank computations once a finite basis and parameterized action are
fixed.

## Reusable Certificate Types

The following certificate families are largely independent of the source
representation problem:

- `rank`: a named matrix has a fixed rank on a stratum.
- `kernel`: a kernel basis or kernel dimension is certified.
- `determinant`: a minor or Gram determinant factors as expected.
- `saturation`: a generic-rank witness remains valid across the intended open
  set.
- `orbit_fullspan`: a vector, singular direction, or quotient class generates
  the whole target module.
- `quotient_kernel`: the singular or radical space of a quotient has the stated
  dimension.
- `cover`: multiple affine charts cover a projective or residual parameter
  space, with no common uncovered rank-drop locus.
- `validation`: independent finite-field, random, or second-tool replay checks.

## Practical Boundaries

The method works best when all of the following are true:

- the module or quotient is finite-dimensional;
- a linearizing structure is available;
- the parameter dependence is polynomial or rational after localization;
- rank-drop loci are cut out by ideals that can be decomposed, saturated, or
  covered by manageable charts;
- cyclicity or radical control can be checked by finite matrix operations.

It becomes risky when:

- no contravariant, cellular, self-dual, or degree-lowering structure is known;
- the problem is wild and submodules cannot be represented by a small set of
  kernels or forms;
- the model is infinite-dimensional without a theorem-supported finite
  truncation;
- Groebner or saturation computations explode because the parameter space or
  module dimension is too large.

In difficult cases, the same ledger can still be useful if the objective is
weakened from complete closure to a named residual set with explicit open gaps.

## Recommended Pilot Problems

Low-risk reuse targets are parameterized cellular-algebra examples, such as
Temperley-Lieb or cyclotomic Hecke cell modules. They already provide explicit
Gram matrices, the simple-head question is a rank question, and the
stratification-plus-saturation workflow can be exercised without inventing a
new representation-theoretic bridge.

## How To Encode This In A Ledger

For a new project, keep the public ledger at the level of reusable structure:

```json
{
  "id": "generic-gram-rank",
  "kind": "rank",
  "claim": "the cell-module Gram matrix has full rank on the generic open stratum",
  "support": "theorem",
  "artifact": "certificates/generic-gram-rank.json",
  "software": {
    "name": "Singular",
    "version": "record-exact-version",
    "role": "determinantal ideal and saturation check"
  }
}
```

The row using that certificate should also include the bridge:

```json
{
  "id": "generic-open",
  "condition": "D(delta)",
  "status": "theorem",
  "quotient": {
    "dimension": 8,
    "kernel": "radical of the Gram form is zero"
  },
  "certificates": ["generic-gram-rank"],
  "bridge": "full Gram rank implies zero radical, hence the standard module has simple head of the stated dimension"
}
```

The exact algebra, source data, private computation logs, and unpublished
specialization tables should stay outside the public repository unless they are
already meant for release.
