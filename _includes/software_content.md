<!-- markdownlint-disable -->

<div class="pkg-header">
<img src="https://raw.githubusercontent.com/kskbhat/Silhouette/main/man/figures/logo.png" alt="Silhouette logo" class="pkg-logo" onerror="this.style.display='none'">
<div class="pkg-header-text">
<h2>Silhouette</h2>

**Proximity Measure Based Diagnostics for Standard, Soft, and Multi-Way Clustering**

</div>
</div>

<div class="pkg-downloads">
<strong>Downloads</strong><br>
<a href="https://cran.r-project.org/package=Silhouette"><img src="https://cranlogs.r-pkg.org/badges/Silhouette" alt="monthly downloads"></a> <a href="https://cran.r-project.org/package=Silhouette"><img src="https://cranlogs.r-pkg.org/badges/grand-total/Silhouette" alt="total downloads"></a>
</div>

::: {.card-grid-2}

::: {.card}

### [📦 CRAN](https://cran.r-project.org/package=Silhouette)

R package version 0.9.6

:::

::: {.card}

### [📖 Documentation](https://kskbhat.github.io/Silhouette)

Package website & vignettes

:::

:::

**Authors:** **Shrikrishna Bhat Kapu** and Kiruthika C\
**DOI:** [10.32614/CRAN.package.Silhouette](https://doi.org/10.32614/CRAN.package.Silhouette)

### Description

An R package for silhouette-based diagnostics in standard, soft, and multi-way clustering. Quantifies clustering quality by measuring both cohesion within clusters and separation between clusters. Implements advanced silhouette width computations for diverse clustering structures, including: simplified silhouette by Van der Laan et al. (2003), Probability of Alternative Cluster normalization methods by Raymaekers and Rousseeuw (2022), fuzzy clustering and silhouette diagnostics using membership probabilities by Campello and Hruschka (2006), Menardi (2011) and Bhat and Kiruthika (2024), and multi-way clustering extensions such as block and tensor clustering by Schepers et al. (2008) and Bhat and Kiruthika (2025). Provides tools for computation and visualization based on Rousseeuw (1987) to support robust and reproducible cluster diagnostics across standard, soft, and multi-way clustering settings. Note: This package does not use the classical Rousseeuw (1987) calculation directly.

### Installation

```r
install.packages("Silhouette")
```

---

## blockclusterPDQ

**An R Package for Block Probabilistic Distance Clustering**

::: {.card-grid-2}

::: {.card}

### [🐙 GitHub](https://github.com/kskbhat/blockclusterPDQ)

Source code repository

:::

:::

**Authors:** **Shrikrishna Bhat Kapu** and Kiruthika C

### Description

The blockclusterPDQ R package implements block (co-)clustering using probabilistic distance methods. It provides a unified framework for simultaneously clustering rows and columns of a data matrix, with support for various data types including continuous, binary, and ordinal data. The package includes functions for model fitting, cluster evaluation, and visualization of co-cluster structures.

### Installation

```r
# Install from GitHub
# install.packages("devtools")
devtools::install_github("kskbhat/blockclusterPDQ")
```

---
