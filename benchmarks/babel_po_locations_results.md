# PO-location benchmark

Python 3.15.0; base e2a17919f0eb988bfea2883b00793ca4d5d37c4f; changed source SHA256 6d6ff31cbf0eec982b1cf3146ac80fa4b11607abbb92c42b22173198591cbc7f.
Median of 8 timing and 8 separate memory runs per version.
The complete write_po call is timed, including sorting, formatting, encoding and writes to a fresh BytesIO.
The two writer functions have identical code; only their generate_po global differs (base or changed).
Catalog construction, PO parsing and output/error checks are outside the timer.
Memory is peak newly traced Python allocations during a write, not total process RAM.
One process is restricted to two physical cores at a time. Pairs rotate, paired versions use the same cores, and order alternates.
100 cases are generated project-like examples; two are empty controls, eight use unchanged public catalogs, and two disable location output.
Generated examples are not collected production workloads. Small timing differences may be noise; slower results and extra memory are retained.
Completed: 112/112; output/error comparisons: 692.

<details>
<summary>Show all 112 benchmark cases</summary>

| Messages | Source references | Catalog | Line numbers | Locations enabled | Base time | PR time | Speed | Base peak | PR peak | Memory |
|---:|---:|---|:---:|:---:|---:|---:|---|---:|---:|---|
| 0 | 0 | empty catalog | no | yes | 0.3879 ms | 0.3476 ms | 1.116× faster | 9.07 KiB | 9.00 KiB | 1.008× less |
| 0 | 0 | empty catalog | yes | yes | 0.3238 ms | 0.3340 ms | 1.032× slower | 9.05 KiB | 9.01 KiB | 1.004× less |
| 1 | 1 | generated: filenames with spaces and Unicode | no | yes | 0.3355 ms | 0.3666 ms | 1.093× slower | 9.00 KiB | 8.92 KiB | 1.009× less |
| 1 | 1 | generated: filenames with spaces and Unicode | yes | yes | 0.4006 ms | 0.4649 ms | 1.161× slower | 9.03 KiB | 9.00 KiB | 1.003× less |
| 1 | 1 | generated: shared label across files | no | yes | 0.4496 ms | 0.5152 ms | 1.146× slower | 9.04 KiB | 8.98 KiB | 1.006× less |
| 1 | 1 | generated: shared label across files | yes | yes | 0.4802 ms | 0.5099 ms | 1.062× slower | 9.06 KiB | 8.98 KiB | 1.008× less |
| 1 | 1 | generated: shared label within one file | no | yes | 0.5430 ms | 0.6177 ms | 1.138× slower | 9.03 KiB | 8.97 KiB | 1.006× less |
| 1 | 1 | generated: shared label within one file | yes | yes | 0.3353 ms | 0.3881 ms | 1.157× slower | 9.04 KiB | 8.98 KiB | 1.007× less |
| 1 | 2 | generated: filenames with spaces and Unicode | no | yes | 0.3969 ms | 0.6115 ms | 1.541× slower | 9.15 KiB | 9.15 KiB | 1.000× less |
| 1 | 2 | generated: filenames with spaces and Unicode | yes | yes | 0.5547 ms | 0.4236 ms | 1.309× faster | 9.23 KiB | 9.16 KiB | 1.007× less |
| 1 | 2 | generated: shared label across files | no | yes | 0.3046 ms | 0.3849 ms | 1.263× slower | 9.04 KiB | 8.98 KiB | 1.007× less |
| 1 | 2 | generated: shared label across files | yes | yes | 0.4399 ms | 0.3526 ms | 1.248× faster | 9.04 KiB | 8.95 KiB | 1.009× less |
| 1 | 2 | generated: shared label within one file | no | yes | 0.3860 ms | 0.4086 ms | 1.059× slower | 9.04 KiB | 9.00 KiB | 1.004× less |
| 1 | 2 | generated: shared label within one file | yes | yes | 0.3600 ms | 0.3685 ms | 1.024× slower | 9.03 KiB | 8.97 KiB | 1.006× less |
| 1 | 5 | generated: filenames with spaces and Unicode | no | yes | 0.4473 ms | 0.3986 ms | 1.122× faster | 10.53 KiB | 10.47 KiB | 1.005× less |
| 1 | 5 | generated: filenames with spaces and Unicode | yes | yes | 0.5288 ms | 0.4149 ms | 1.275× faster | 10.61 KiB | 10.57 KiB | 1.004× less |
| 1 | 5 | generated: shared label across files | no | yes | 0.4750 ms | 0.3894 ms | 1.220× faster | 8.98 KiB | 8.93 KiB | 1.006× less |
| 1 | 5 | generated: shared label across files | yes | yes | 0.5047 ms | 0.3561 ms | 1.417× faster | 9.04 KiB | 8.96 KiB | 1.009× less |
| 1 | 5 | generated: shared label within one file | no | yes | 0.4345 ms | 0.4032 ms | 1.078× faster | 8.98 KiB | 8.93 KiB | 1.007× less |
| 1 | 5 | generated: shared label within one file | yes | yes | 0.3852 ms | 0.4255 ms | 1.105× slower | 9.10 KiB | 9.07 KiB | 1.003× less |
| 1 | 10 | generated: filenames with spaces and Unicode | no | yes | 0.3327 ms | 0.3243 ms | 1.026× faster | 12.83 KiB | 12.92 KiB | 1.007× more |
| 1 | 10 | generated: filenames with spaces and Unicode | yes | yes | 0.3435 ms | 0.3569 ms | 1.039× slower | 13.04 KiB | 13.13 KiB | 1.007× more |
| 1 | 10 | generated: shared label across files | no | yes | 0.3389 ms | 0.3071 ms | 1.104× faster | 9.42 KiB | 9.50 KiB | 1.009× more |
| 1 | 10 | generated: shared label across files | yes | yes | 0.3213 ms | 0.2909 ms | 1.105× faster | 10.08 KiB | 10.17 KiB | 1.009× more |
| 1 | 10 | generated: shared label within one file | no | yes | 0.2772 ms | 0.2726 ms | 1.017× faster | 9.00 KiB | 8.95 KiB | 1.006× less |
| 1 | 10 | generated: shared label within one file | yes | yes | 0.3825 ms | 0.3332 ms | 1.148× faster | 10.11 KiB | 10.20 KiB | 1.009× more |
| 1 | 20 | generated: filenames with spaces and Unicode | no | yes | 0.4416 ms | 0.4812 ms | 1.090× slower | 18.09 KiB | 18.34 KiB | 1.014× more |
| 1 | 20 | generated: filenames with spaces and Unicode | yes | yes | 0.4686 ms | 0.4625 ms | 1.013× faster | 18.48 KiB | 18.77 KiB | 1.015× more |
| 1 | 20 | generated: shared label across files | no | yes | 0.3846 ms | 0.3715 ms | 1.035× faster | 11.28 KiB | 11.47 KiB | 1.017× more |
| 1 | 20 | generated: shared label across files | yes | yes | 0.4659 ms | 0.4040 ms | 1.153× faster | 12.64 KiB | 12.90 KiB | 1.021× more |
| 1 | 20 | generated: shared label within one file | no | yes | 0.2899 ms | 0.2909 ms | 1.003× slower | 9.06 KiB | 8.97 KiB | 1.009× less |
| 1 | 20 | generated: shared label within one file | yes | yes | 0.3661 ms | 0.3780 ms | 1.032× slower | 12.78 KiB | 13.02 KiB | 1.018× more |
| 1 | 50 | generated: filenames with spaces and Unicode | no | yes | 0.6490 ms | 0.6300 ms | 1.030× faster | 33.85 KiB | 34.94 KiB | 1.032× more |
| 1 | 50 | generated: filenames with spaces and Unicode | yes | yes | 0.6621 ms | 0.6589 ms | 1.005× faster | 35.11 KiB | 36.18 KiB | 1.030× more |
| 1 | 50 | generated: shared label across files | no | yes | 0.4888 ms | 0.5422 ms | 1.109× slower | 17.21 KiB | 18.30 KiB | 1.063× more |
| 1 | 50 | generated: shared label across files | yes | yes | 0.6829 ms | 0.5314 ms | 1.285× faster | 20.77 KiB | 21.88 KiB | 1.054× more |
| 1 | 50 | generated: shared label within one file | no | yes | 0.2827 ms | 0.3200 ms | 1.132× slower | 10.96 KiB | 10.93 KiB | 1.002× less |
| 1 | 50 | generated: shared label within one file | yes | yes | 0.8052 ms | 0.6396 ms | 1.259× faster | 21.03 KiB | 22.12 KiB | 1.051× more |
| 1 | 100 | generated: filenames with spaces and Unicode | no | yes | 1.4086 ms | 1.2300 ms | 1.145× faster | 60.20 KiB | 62.50 KiB | 1.038× more |
| 1 | 100 | generated: filenames with spaces and Unicode | yes | yes | 1.5486 ms | 1.7181 ms | 1.109× slower | 63.02 KiB | 65.37 KiB | 1.037× more |
| 1 | 100 | generated: shared label across files | no | yes | 0.9824 ms | 0.7209 ms | 1.363× faster | 27.34 KiB | 29.74 KiB | 1.088× more |
| 1 | 100 | generated: shared label across files | yes | yes | 1.1002 ms | 0.9925 ms | 1.109× faster | 34.74 KiB | 37.06 KiB | 1.067× more |
| 1 | 100 | generated: shared label within one file | no | yes | 0.5462 ms | 0.4364 ms | 1.252× faster | 14.52 KiB | 14.45 KiB | 1.005× less |
| 1 | 100 | generated: shared label within one file | yes | yes | 1.2783 ms | 1.1726 ms | 1.090× faster | 35.17 KiB | 37.54 KiB | 1.067× more |
| 1 | 250 | generated: filenames with spaces and Unicode | no | yes | 3.1341 ms | 2.5496 ms | 1.229× faster | 139.98 KiB | 144.27 KiB | 1.031× more |
| 1 | 250 | generated: filenames with spaces and Unicode | yes | yes | 3.5715 ms | 2.7552 ms | 1.296× faster | 147.50 KiB | 151.78 KiB | 1.029× more |
| 1 | 250 | generated: shared label across files | no | yes | 2.2920 ms | 1.5757 ms | 1.455× faster | 59.71 KiB | 63.99 KiB | 1.072× more |
| 1 | 250 | generated: shared label across files | yes | yes | 2.8604 ms | 1.9285 ms | 1.483× faster | 78.51 KiB | 82.73 KiB | 1.054× more |
| 1 | 250 | generated: shared label within one file | no | yes | 0.6425 ms | 0.7053 ms | 1.098× slower | 25.73 KiB | 25.74 KiB | 1.000× more |
| 1 | 250 | generated: shared label within one file | yes | yes | 3.5869 ms | 2.3370 ms | 1.535× faster | 78.94 KiB | 83.21 KiB | 1.054× more |
| 1 | 500 | generated: filenames with spaces and Unicode | no | yes | 9.3451 ms | 4.5844 ms | 2.038× faster | 274.10 KiB | 282.71 KiB | 1.031× more |
| 1 | 500 | generated: filenames with spaces and Unicode | yes | yes | 8.3529 ms | 4.8285 ms | 1.730× faster | 290.72 KiB | 299.38 KiB | 1.030× more |
| 1 | 500 | generated: shared label across files | no | yes | 6.9262 ms | 3.6841 ms | 1.880× faster | 114.20 KiB | 122.84 KiB | 1.076× more |
| 1 | 500 | generated: shared label across files | yes | yes | 7.5947 ms | 3.7021 ms | 2.051× faster | 152.69 KiB | 161.30 KiB | 1.056× more |
| 1 | 500 | generated: shared label within one file | no | yes | 0.6268 ms | 0.6487 ms | 1.035× slower | 45.26 KiB | 45.27 KiB | 1.000× more |
| 1 | 500 | generated: shared label within one file | yes | yes | 6.8567 ms | 3.2698 ms | 2.097× faster | 153.10 KiB | 161.76 KiB | 1.057× more |
| 1 | 1000 | generated: filenames with spaces and Unicode | no | yes | 24.0237 ms | 8.2101 ms | 2.926× faster | 539.04 KiB | 555.81 KiB | 1.031× more |
| 1 | 1000 | generated: filenames with spaces and Unicode | yes | yes | 24.1219 ms | 8.8915 ms | 2.713× faster | 575.22 KiB | 591.99 KiB | 1.029× more |
| 1 | 1000 | generated: shared label across files | no | yes | 20.4920 ms | 5.8335 ms | 3.513× faster | 219.96 KiB | 236.73 KiB | 1.076× more |
| 1 | 1000 | generated: shared label across files | yes | yes | 23.4584 ms | 7.9836 ms | 2.938× faster | 298.49 KiB | 315.26 KiB | 1.056× more |
| 1 | 1000 | generated: shared label within one file | no | yes | 0.9209 ms | 0.9861 ms | 1.071× slower | 84.32 KiB | 84.33 KiB | 1.000× more |
| 1 | 1000 | generated: shared label within one file | yes | yes | 20.6049 ms | 7.5160 ms | 2.741× faster | 298.92 KiB | 315.69 KiB | 1.056× more |
| 1 | 1000 | locations disabled control | no | no | 0.3424 ms | 0.3825 ms | 1.117× slower | 9.00 KiB | 8.97 KiB | 1.003× less |
| 1 | 1000 | locations disabled control | yes | no | 0.4982 ms | 0.4482 ms | 1.111× faster | 8.92 KiB | 8.92 KiB | same |
| 5 | 5000 | generated: app labels across files | no | yes | 103.1697 ms | 24.1225 ms | 4.277× faster | 319.03 KiB | 335.80 KiB | 1.053× more |
| 5 | 5000 | generated: app labels across files | yes | yes | 101.1042 ms | 32.0523 ms | 3.154× faster | 411.34 KiB | 428.12 KiB | 1.041× more |
| 5 | 5000 | generated: app labels within modules | no | yes | 5.8773 ms | 6.3909 ms | 1.087× slower | 99.04 KiB | 99.05 KiB | 1.000× more |
| 5 | 5000 | generated: app labels within modules | yes | yes | 96.2439 ms | 29.9406 ms | 3.214× faster | 409.77 KiB | 426.51 KiB | 1.041× more |
| 10 | 5000 | generated: app labels across files | no | yes | 70.4790 ms | 24.1830 ms | 2.914× faster | 226.39 KiB | 235.02 KiB | 1.038× more |
| 10 | 5000 | generated: app labels across files | yes | yes | 61.1414 ms | 29.2460 ms | 2.091× faster | 280.40 KiB | 289.00 KiB | 1.031× more |
| 10 | 5000 | generated: app labels within modules | no | yes | 5.8122 ms | 5.9958 ms | 1.032× slower | 54.11 KiB | 54.12 KiB | 1.000× more |
| 10 | 5000 | generated: app labels within modules | yes | yes | 70.1133 ms | 34.1129 ms | 2.055× faster | 279.74 KiB | 288.40 KiB | 1.031× more |
| 20 | 5000 | generated: app labels across files | no | yes | 48.1683 ms | 27.0498 ms | 1.781× faster | 171.23 KiB | 175.50 KiB | 1.025× more |
| 20 | 5000 | generated: app labels across files | yes | yes | 45.7667 ms | 29.2633 ms | 1.564× faster | 207.06 KiB | 211.34 KiB | 1.021× more |
| 20 | 5000 | generated: app labels within modules | no | yes | 6.3804 ms | 6.6139 ms | 1.037× slower | 31.21 KiB | 31.25 KiB | 1.001× more |
| 20 | 5000 | generated: app labels within modules | yes | yes | 50.9239 ms | 30.8730 ms | 1.649× faster | 209.87 KiB | 214.11 KiB | 1.020× more |
| 25 | 25 | generated: app labels across files | no | yes | 1.1040 ms | 1.2118 ms | 1.098× slower | 10.68 KiB | 10.65 KiB | 1.002× less |
| 25 | 25 | generated: app labels across files | yes | yes | 1.2873 ms | 1.0867 ms | 1.185× faster | 10.82 KiB | 10.80 KiB | 1.002× less |
| 25 | 25 | generated: app labels within modules | no | yes | 0.8693 ms | 1.0674 ms | 1.228× slower | 10.81 KiB | 10.76 KiB | 1.005× less |
| 25 | 25 | generated: app labels within modules | yes | yes | 1.0117 ms | 1.0425 ms | 1.030× slower | 10.79 KiB | 10.79 KiB | 1.000× more |
| 25 | 50 | generated: app labels across files | no | yes | 1.2293 ms | 1.0666 ms | 1.153× faster | 11.38 KiB | 11.36 KiB | 1.002× less |
| 25 | 50 | generated: app labels across files | yes | yes | 1.0927 ms | 1.2461 ms | 1.140× slower | 11.66 KiB | 11.64 KiB | 1.002× less |
| 25 | 50 | generated: app labels within modules | no | yes | 1.0074 ms | 1.1400 ms | 1.132× slower | 11.45 KiB | 11.45 KiB | 1.001× more |
| 25 | 50 | generated: app labels within modules | yes | yes | 1.3353 ms | 1.2015 ms | 1.111× faster | 11.64 KiB | 11.64 KiB | 1.000× less |
| 25 | 125 | generated: app labels across files | no | yes | 1.3482 ms | 1.9255 ms | 1.428× slower | 13.67 KiB | 13.57 KiB | 1.007× less |
| 25 | 125 | generated: app labels across files | yes | yes | 1.4118 ms | 1.6582 ms | 1.174× slower | 13.99 KiB | 13.90 KiB | 1.007× less |
| 25 | 125 | generated: app labels within modules | no | yes | 1.3276 ms | 1.2245 ms | 1.084× faster | 13.21 KiB | 13.21 KiB | 1.000× less |
| 25 | 125 | generated: app labels within modules | yes | yes | 1.3267 ms | 1.3006 ms | 1.020× faster | 14.28 KiB | 14.23 KiB | 1.004× less |
| 25 | 250 | generated: app labels across files | no | yes | 1.8263 ms | 1.6455 ms | 1.110× faster | 16.83 KiB | 16.87 KiB | 1.002× more |
| 25 | 250 | generated: app labels across files | yes | yes | 1.8258 ms | 1.8559 ms | 1.016× slower | 18.04 KiB | 18.10 KiB | 1.004× more |
| 25 | 250 | generated: app labels within modules | no | yes | 1.4622 ms | 1.5002 ms | 1.026× slower | 13.21 KiB | 13.16 KiB | 1.004× less |
| 25 | 250 | generated: app labels within modules | yes | yes | 2.3531 ms | 2.0599 ms | 1.142× faster | 19.10 KiB | 19.19 KiB | 1.004× more |
| 25 | 500 | generated: app labels across files | no | yes | 4.2437 ms | 3.9466 ms | 1.075× faster | 24.46 KiB | 24.73 KiB | 1.011× more |
| 25 | 500 | generated: app labels across files | yes | yes | 4.5649 ms | 3.9921 ms | 1.143× faster | 26.33 KiB | 26.52 KiB | 1.007× more |
| 25 | 500 | generated: app labels within modules | no | yes | 2.0906 ms | 1.6111 ms | 1.298× faster | 13.91 KiB | 13.92 KiB | 1.000× more |
| 25 | 500 | generated: app labels within modules | yes | yes | 3.2044 ms | 3.2587 ms | 1.017× slower | 27.13 KiB | 27.34 KiB | 1.008× more |
| 25 | 1250 | generated: app labels across files | no | yes | 7.6463 ms | 6.5834 ms | 1.161× faster | 46.24 KiB | 47.32 KiB | 1.023× more |
| 25 | 1250 | generated: app labels across files | yes | yes | 7.2787 ms | 6.9598 ms | 1.046× faster | 53.39 KiB | 54.52 KiB | 1.021× more |
| 25 | 1250 | generated: app labels within modules | no | yes | 2.2934 ms | 2.4949 ms | 1.088× slower | 16.05 KiB | 16.00 KiB | 1.003× less |
| 25 | 1250 | generated: app labels within modules | yes | yes | 8.4109 ms | 8.6813 ms | 1.032× slower | 55.96 KiB | 57.07 KiB | 1.020× more |
| 25 | 2500 | generated: app labels across files | no | yes | 16.4236 ms | 13.6815 ms | 1.200× faster | 80.70 KiB | 83.08 KiB | 1.029× more |
| 25 | 2500 | generated: app labels across files | yes | yes | 20.0682 ms | 16.1213 ms | 1.245× faster | 100.74 KiB | 103.09 KiB | 1.023× more |
| 25 | 2500 | generated: app labels within modules | no | yes | 3.5257 ms | 3.9350 ms | 1.116× slower | 19.54 KiB | 19.47 KiB | 1.004× less |
| 25 | 2500 | generated: app labels within modules | yes | yes | 19.8136 ms | 16.7752 ms | 1.181× faster | 108.02 KiB | 110.37 KiB | 1.022× more |
| 348 | 0 | Django German | no | yes | 12.1650 ms | 12.9314 ms | 1.063× slower | 46.38 KiB | 46.41 KiB | 1.001× more |
| 348 | 0 | Django German | yes | yes | 12.6133 ms | 12.8305 ms | 1.017× slower | 46.35 KiB | 46.36 KiB | 1.000× more |
| 902 | 0 | Wagtail French | no | yes | 35.2144 ms | 35.7598 ms | 1.015× slower | 131.90 KiB | 131.87 KiB | 1.000× less |
| 902 | 0 | Wagtail French | yes | yes | 35.0926 ms | 34.9100 ms | 1.005× faster | 131.87 KiB | 131.87 KiB | 1.000× more |
| 902 | 0 | Wagtail German | no | yes | 37.7520 ms | 38.1230 ms | 1.010× slower | 128.59 KiB | 128.54 KiB | 1.000× less |
| 902 | 0 | Wagtail German | yes | yes | 38.6008 ms | 37.8689 ms | 1.019× faster | 128.54 KiB | 128.57 KiB | 1.000× more |
| 3171 | 784 | Odoo account template | no | yes | 127.0572 ms | 131.6106 ms | 1.036× slower | 369.68 KiB | 369.65 KiB | 1.000× less |
| 3171 | 784 | Odoo account template | yes | yes | 122.0702 ms | 131.2746 ms | 1.075× slower | 369.68 KiB | 369.65 KiB | 1.000× less |

</details>

Public catalog sources:

- [Django German](https://raw.githubusercontent.com/django/django/dab0a5c47f159eb58472110dcbc10bd4a9b01adb/django/conf/locale/de/LC_MESSAGES/django.po) (unchanged contents; SHA256 in JSON).
- [Wagtail German](https://raw.githubusercontent.com/wagtail/wagtail/e18fa1162b2fd352cefef345d9f558cc7fbdbcf3/wagtail/admin/locale/de/LC_MESSAGES/django.po) (unchanged contents; SHA256 in JSON).
- [Wagtail French](https://raw.githubusercontent.com/wagtail/wagtail/e18fa1162b2fd352cefef345d9f558cc7fbdbcf3/wagtail/admin/locale/fr/LC_MESSAGES/django.po) (unchanged contents; SHA256 in JSON).
- [Odoo account template](https://raw.githubusercontent.com/odoo/odoo/e1ed4fe077ba98ce7ac6802a43bb68242081dee9/addons/account/i18n/account.pot) (unchanged contents; SHA256 in JSON).
