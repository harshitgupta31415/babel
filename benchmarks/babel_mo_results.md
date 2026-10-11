# MO-file writing benchmark

Python 3.15.0; base e2a17919f0eb988bfea2883b00793ca4d5d37c4f; changed-source SHA256 d00b731b862c072ab0c4a4869ebdece57fb3999697a98c9abf1c5a8ee5043ac4.
Median of 8 timing and 8 separate peak-memory runs per version.
The complete write_mo() call is timed, including sorting and writing to a fresh BytesIO.
Catalog construction, PO parsing, fixture downloads and output comparisons are excluded.
Memory is peak newly traced Python allocations during one write, not total RAM.
Paired versions use the same two physical cores; pairs rotate between repeats. Version order alternates.
There are 100 generated examples (not collected production workloads), plus two empty-catalog controls and six cases using unchanged public project catalogs.
Small differences may be measurement noise. Slower cases and extra memory are retained.
Completed: 108/108 cases. Output/error comparisons: 414.

<details>
<summary>Show all 108 measured cases</summary>

| Messages | Catalog | Include fuzzy | Base time | PR time | Speed | Base peak | PR peak | Memory |
|---:|---|:---:|---:|---:|---|---:|---:|---|
| 0 | empty-catalog control | no | 0.0794 ms | 0.0735 ms | 1.080× faster | 4.95 KiB | 5.11 KiB | 1.032× more |
| 0 | empty-catalog control | yes | 0.0727 ms | 0.0730 ms | 1.004× slower | 4.95 KiB | 5.11 KiB | 1.032× more |
| 1 | generated: UI labels | no | 0.0862 ms | 0.0910 ms | 1.056× slower | 4.92 KiB | 5.10 KiB | 1.037× more |
| 1 | generated: UI labels | yes | 0.1086 ms | 0.0784 ms | 1.385× faster | 4.92 KiB | 5.10 KiB | 1.037× more |
| 1 | generated: context labels | no | 0.0906 ms | 0.0979 ms | 1.081× slower | 4.85 KiB | 5.03 KiB | 1.037× more |
| 1 | generated: context labels | yes | 0.0974 ms | 0.0908 ms | 1.073× faster | 4.85 KiB | 5.03 KiB | 1.037× more |
| 1 | generated: help paragraphs | no | 0.0818 ms | 0.0843 ms | 1.031× slower | 7.64 KiB | 7.76 KiB | 1.016× more |
| 1 | generated: help paragraphs | yes | 0.0947 ms | 0.0888 ms | 1.067× faster | 7.64 KiB | 7.76 KiB | 1.016× more |
| 1 | generated: mixed catalog | no | 0.0922 ms | 0.0984 ms | 1.067× slower | 4.93 KiB | 5.09 KiB | 1.032× more |
| 1 | generated: mixed catalog | yes | 0.0840 ms | 0.0807 ms | 1.040× faster | 4.93 KiB | 5.09 KiB | 1.032× more |
| 1 | generated: plural status | no | 0.0829 ms | 0.0880 ms | 1.062× slower | 5.06 KiB | 5.25 KiB | 1.036× more |
| 1 | generated: plural status | yes | 0.0924 ms | 0.0884 ms | 1.045× faster | 5.06 KiB | 5.25 KiB | 1.036× more |
| 2 | generated: UI labels | no | 0.0867 ms | 0.0988 ms | 1.140× slower | 5.22 KiB | 5.38 KiB | 1.031× more |
| 2 | generated: UI labels | yes | 0.0939 ms | 0.0900 ms | 1.044× faster | 5.22 KiB | 5.38 KiB | 1.031× more |
| 2 | generated: context labels | no | 0.0847 ms | 0.0917 ms | 1.082× slower | 5.10 KiB | 5.27 KiB | 1.034× more |
| 2 | generated: context labels | yes | 0.0960 ms | 0.0870 ms | 1.103× faster | 5.10 KiB | 5.27 KiB | 1.034× more |
| 2 | generated: help paragraphs | no | 0.0939 ms | 0.1026 ms | 1.093× slower | 10.04 KiB | 10.17 KiB | 1.012× more |
| 2 | generated: help paragraphs | yes | 0.1086 ms | 0.0969 ms | 1.122× faster | 10.04 KiB | 10.17 KiB | 1.012× more |
| 2 | generated: mixed catalog | no | 0.0824 ms | 0.0897 ms | 1.088× slower | 7.68 KiB | 7.81 KiB | 1.016× more |
| 2 | generated: mixed catalog | yes | 0.0878 ms | 0.0863 ms | 1.017× faster | 7.68 KiB | 7.81 KiB | 1.016× more |
| 2 | generated: plural status | no | 0.1088 ms | 0.1095 ms | 1.007× slower | 5.41 KiB | 5.56 KiB | 1.028× more |
| 2 | generated: plural status | yes | 0.1118 ms | 0.1050 ms | 1.064× faster | 5.41 KiB | 5.56 KiB | 1.028× more |
| 10 | generated: UI labels | no | 0.1098 ms | 0.1296 ms | 1.180× slower | 7.31 KiB | 7.49 KiB | 1.024× more |
| 10 | generated: UI labels | yes | 0.1174 ms | 0.1182 ms | 1.007× slower | 7.57 KiB | 7.71 KiB | 1.018× more |
| 10 | generated: context labels | no | 0.1253 ms | 0.1140 ms | 1.099× faster | 6.85 KiB | 7.06 KiB | 1.031× more |
| 10 | generated: context labels | yes | 0.1240 ms | 0.1220 ms | 1.016× faster | 7.05 KiB | 7.24 KiB | 1.027× more |
| 10 | generated: help paragraphs | no | 0.1259 ms | 0.1378 ms | 1.095× slower | 27.25 KiB | 28.24 KiB | 1.036× more |
| 10 | generated: help paragraphs | yes | 0.1341 ms | 0.1311 ms | 1.023× faster | 29.67 KiB | 29.94 KiB | 1.009× more |
| 10 | generated: mixed catalog | no | 0.1767 ms | 0.1646 ms | 1.073× faster | 11.63 KiB | 11.83 KiB | 1.017× more |
| 10 | generated: mixed catalog | yes | 0.1505 ms | 0.1684 ms | 1.119× slower | 14.24 KiB | 14.53 KiB | 1.020× more |
| 10 | generated: plural status | no | 0.1391 ms | 0.1364 ms | 1.020× faster | 7.87 KiB | 8.11 KiB | 1.031× more |
| 10 | generated: plural status | yes | 0.1540 ms | 0.1428 ms | 1.079× faster | 8.26 KiB | 8.46 KiB | 1.023× more |
| 50 | generated: UI labels | no | 0.3981 ms | 0.3506 ms | 1.135× faster | 21.14 KiB | 21.29 KiB | 1.007× more |
| 50 | generated: UI labels | yes | 0.4514 ms | 0.3917 ms | 1.153× faster | 23.37 KiB | 23.62 KiB | 1.011× more |
| 50 | generated: context labels | no | 0.3862 ms | 0.3979 ms | 1.030× slower | 18.18 KiB | 18.38 KiB | 1.011× more |
| 50 | generated: context labels | yes | 0.4008 ms | 0.3964 ms | 1.011× faster | 20.00 KiB | 20.18 KiB | 1.009× more |
| 50 | generated: help paragraphs | no | 0.5686 ms | 0.4991 ms | 1.139× faster | 116.24 KiB | 118.39 KiB | 1.018× more |
| 50 | generated: help paragraphs | yes | 0.6699 ms | 0.5115 ms | 1.310× faster | 128.68 KiB | 132.09 KiB | 1.026× more |
| 50 | generated: mixed catalog | no | 0.4229 ms | 0.4041 ms | 1.047× faster | 40.24 KiB | 41.00 KiB | 1.019× more |
| 50 | generated: mixed catalog | yes | 0.4575 ms | 0.4229 ms | 1.082× faster | 48.67 KiB | 49.51 KiB | 1.017× more |
| 50 | generated: plural status | no | 0.4987 ms | 0.4645 ms | 1.074× faster | 24.09 KiB | 24.50 KiB | 1.017× more |
| 50 | generated: plural status | yes | 0.6297 ms | 0.5483 ms | 1.148× faster | 26.68 KiB | 26.84 KiB | 1.006× more |
| 100 | generated: UI labels | no | 0.5550 ms | 0.5139 ms | 1.080× faster | 40.34 KiB | 40.76 KiB | 1.010× more |
| 100 | generated: UI labels | yes | 0.7697 ms | 0.5991 ms | 1.285× faster | 44.47 KiB | 44.93 KiB | 1.010× more |
| 100 | generated: context labels | no | 0.6396 ms | 0.5805 ms | 1.102× faster | 33.82 KiB | 34.03 KiB | 1.006× more |
| 100 | generated: context labels | yes | 0.6035 ms | 0.5970 ms | 1.011× faster | 37.65 KiB | 37.97 KiB | 1.009× more |
| 100 | generated: help paragraphs | no | 1.0481 ms | 0.6878 ms | 1.524× faster | 225.21 KiB | 227.35 KiB | 1.010× more |
| 100 | generated: help paragraphs | yes | 1.1132 ms | 0.7800 ms | 1.427× faster | 249.35 KiB | 253.21 KiB | 1.015× more |
| 100 | generated: mixed catalog | no | 1.0351 ms | 0.9084 ms | 1.139× faster | 75.13 KiB | 76.76 KiB | 1.022× more |
| 100 | generated: mixed catalog | yes | 1.3102 ms | 0.9102 ms | 1.440× faster | 88.81 KiB | 89.64 KiB | 1.009× more |
| 100 | generated: plural status | no | 0.8139 ms | 0.7807 ms | 1.043× faster | 45.54 KiB | 45.88 KiB | 1.007× more |
| 100 | generated: plural status | yes | 0.9719 ms | 0.8374 ms | 1.161× faster | 49.79 KiB | 50.33 KiB | 1.011× more |
| 250 | generated: UI labels | no | 1.3360 ms | 1.1707 ms | 1.141× faster | 91.52 KiB | 92.79 KiB | 1.014× more |
| 250 | generated: UI labels | yes | 1.6381 ms | 1.2588 ms | 1.301× faster | 99.68 KiB | 99.91 KiB | 1.002× more |
| 250 | generated: context labels | no | 1.3728 ms | 1.1463 ms | 1.198× faster | 79.27 KiB | 79.81 KiB | 1.007× more |
| 250 | generated: context labels | yes | 1.4930 ms | 1.4138 ms | 1.056× faster | 86.07 KiB | 86.32 KiB | 1.003× more |
| 250 | generated: help paragraphs | no | 3.2016 ms | 1.8306 ms | 1.749× faster | 551.65 KiB | 568.42 KiB | 1.030× more |
| 250 | generated: help paragraphs | yes | 4.2914 ms | 2.1651 ms | 1.982× faster | 610.86 KiB | 632.32 KiB | 1.035× more |
| 250 | generated: mixed catalog | no | 2.9324 ms | 2.0096 ms | 1.459× faster | 178.97 KiB | 183.16 KiB | 1.023× more |
| 250 | generated: mixed catalog | yes | 3.3237 ms | 2.3687 ms | 1.403× faster | 212.96 KiB | 215.10 KiB | 1.010× more |
| 250 | generated: plural status | no | 2.5251 ms | 2.0214 ms | 1.249× faster | 104.23 KiB | 105.05 KiB | 1.008× more |
| 250 | generated: plural status | yes | 2.3970 ms | 2.0610 ms | 1.163× faster | 113.79 KiB | 114.88 KiB | 1.010× more |
| 348 | Django German | no | 4.7925 ms | 4.3883 ms | 1.092× faster | 155.46 KiB | 155.99 KiB | 1.003× more |
| 348 | Django German | yes | 4.4586 ms | 3.9581 ms | 1.126× faster | 155.46 KiB | 155.99 KiB | 1.003× more |
| 500 | generated: UI labels | no | 3.1018 ms | 2.6990 ms | 1.149× faster | 174.82 KiB | 175.48 KiB | 1.004× more |
| 500 | generated: UI labels | yes | 3.5530 ms | 2.3261 ms | 1.527× faster | 193.21 KiB | 194.26 KiB | 1.005× more |
| 500 | generated: context labels | no | 3.9200 ms | 2.8876 ms | 1.358× faster | 150.04 KiB | 150.26 KiB | 1.001× more |
| 500 | generated: context labels | yes | 3.3068 ms | 2.4294 ms | 1.361× faster | 165.68 KiB | 166.12 KiB | 1.003× more |
| 500 | generated: help paragraphs | no | 8.7462 ms | 3.0473 ms | 2.870× faster | 1094.40 KiB | 1095.82 KiB | 1.001× more |
| 500 | generated: help paragraphs | yes | 10.9009 ms | 4.9355 ms | 2.209× faster | 1214.89 KiB | 1221.64 KiB | 1.006× more |
| 500 | generated: mixed catalog | no | 6.5656 ms | 4.3322 ms | 1.516× faster | 347.74 KiB | 353.81 KiB | 1.017× more |
| 500 | generated: mixed catalog | yes | 7.9519 ms | 4.8575 ms | 1.637× faster | 413.59 KiB | 418.58 KiB | 1.012× more |
| 500 | generated: plural status | no | 4.4429 ms | 3.5859 ms | 1.239× faster | 200.71 KiB | 202.78 KiB | 1.010× more |
| 500 | generated: plural status | yes | 4.6811 ms | 3.6184 ms | 1.294× faster | 221.96 KiB | 222.51 KiB | 1.002× more |
| 902 | Wagtail French | no | 14.6092 ms | 12.0440 ms | 1.213× faster | 459.64 KiB | 462.06 KiB | 1.005× more |
| 902 | Wagtail French | yes | 15.4097 ms | 10.8802 ms | 1.416× faster | 459.64 KiB | 462.06 KiB | 1.005× more |
| 902 | Wagtail German | no | 13.9527 ms | 10.9376 ms | 1.276× faster | 450.92 KiB | 455.24 KiB | 1.010× more |
| 902 | Wagtail German | yes | 16.5029 ms | 11.1853 ms | 1.475× faster | 450.92 KiB | 455.24 KiB | 1.010× more |
| 1000 | generated: UI labels | no | 5.7973 ms | 3.9999 ms | 1.449× faster | 343.63 KiB | 345.79 KiB | 1.006× more |
| 1000 | generated: UI labels | yes | 6.1017 ms | 3.9066 ms | 1.562× faster | 376.48 KiB | 379.50 KiB | 1.008× more |
| 1000 | generated: context labels | no | 9.0295 ms | 5.5931 ms | 1.614× faster | 293.81 KiB | 294.86 KiB | 1.004× more |
| 1000 | generated: context labels | yes | 7.1513 ms | 5.0712 ms | 1.410× faster | 321.12 KiB | 322.66 KiB | 1.005× more |
| 1000 | generated: help paragraphs | no | 26.4305 ms | 7.2473 ms | 3.647× faster | 2182.11 KiB | 2196.45 KiB | 1.007× more |
| 1000 | generated: help paragraphs | yes | 44.0453 ms | 8.6429 ms | 5.096× faster | 2419.15 KiB | 2444.96 KiB | 1.011× more |
| 1000 | generated: mixed catalog | no | 19.5093 ms | 9.5673 ms | 2.039× faster | 689.44 KiB | 698.28 KiB | 1.013× more |
| 1000 | generated: mixed catalog | yes | 24.3490 ms | 10.2310 ms | 2.380× faster | 821.26 KiB | 828.86 KiB | 1.009× more |
| 1000 | generated: plural status | no | 12.3560 ms | 8.4057 ms | 1.470× faster | 395.89 KiB | 397.25 KiB | 1.003× more |
| 1000 | generated: plural status | yes | 12.0427 ms | 7.8518 ms | 1.534× faster | 434.54 KiB | 436.84 KiB | 1.005× more |
| 2500 | generated: UI labels | no | 21.1395 ms | 10.9906 ms | 1.923× faster | 830.44 KiB | 835.67 KiB | 1.006× more |
| 2500 | generated: UI labels | yes | 26.5648 ms | 11.5095 ms | 2.308× faster | 903.12 KiB | 911.85 KiB | 1.010× more |
| 2500 | generated: context labels | no | 18.6855 ms | 11.4761 ms | 1.628× faster | 701.51 KiB | 704.84 KiB | 1.005× more |
| 2500 | generated: context labels | yes | 24.1964 ms | 11.4877 ms | 2.106× faster | 768.65 KiB | 773.18 KiB | 1.006× more |
| 2500 | generated: help paragraphs | no | 328.6664 ms | 20.8280 ms | 15.780× faster | 5425.60 KiB | 5513.45 KiB | 1.016× more |
| 2500 | generated: help paragraphs | yes | 563.0075 ms | 24.2740 ms | 23.194× faster | 6008.79 KiB | 6130.16 KiB | 1.020× more |
| 2500 | generated: mixed catalog | no | 80.3307 ms | 25.4874 ms | 3.152× faster | 1714.36 KiB | 1730.85 KiB | 1.010× more |
| 2500 | generated: mixed catalog | yes | 103.8611 ms | 28.2105 ms | 3.682× faster | 2024.54 KiB | 2061.41 KiB | 1.018× more |
| 2500 | generated: plural status | no | 37.7302 ms | 19.2432 ms | 1.961× faster | 969.71 KiB | 980.55 KiB | 1.011× more |
| 2500 | generated: plural status | yes | 42.8890 ms | 20.4280 ms | 2.100× faster | 1057.86 KiB | 1071.85 KiB | 1.013× more |
| 5000 | generated: UI labels | no | 66.9249 ms | 22.2688 ms | 3.005× faster | 1505.45 KiB | 1517.30 KiB | 1.008× more |
| 5000 | generated: UI labels | yes | 67.0938 ms | 24.8941 ms | 2.695× faster | 1651.78 KiB | 1670.93 KiB | 1.012× more |
| 5000 | generated: context labels | no | 47.4505 ms | 22.4813 ms | 2.111× faster | 1390.62 KiB | 1398.35 KiB | 1.006× more |
| 5000 | generated: context labels | yes | 58.6467 ms | 22.8965 ms | 2.561× faster | 1543.03 KiB | 1553.26 KiB | 1.007× more |
| 5000 | generated: help paragraphs | no | 2799.6683 ms | 42.0053 ms | 66.650× faster | 10695.09 KiB | 10918.81 KiB | 1.021× more |
| 5000 | generated: help paragraphs | yes | 3994.5715 ms | 44.5307 ms | 89.704× faster | 11862.42 KiB | 12160.32 KiB | 1.025× more |
| 5000 | generated: mixed catalog | no | 321.7073 ms | 48.1212 ms | 6.685× faster | 3259.16 KiB | 3303.50 KiB | 1.014× more |
| 5000 | generated: mixed catalog | yes | 429.5797 ms | 57.2891 ms | 7.498× faster | 3878.69 KiB | 3967.72 KiB | 1.023× more |
| 5000 | generated: plural status | no | 97.1637 ms | 35.9960 ms | 2.699× faster | 1789.74 KiB | 1812.31 KiB | 1.013× more |
| 5000 | generated: plural status | yes | 121.2796 ms | 36.1377 ms | 3.356× faster | 1967.64 KiB | 1996.67 KiB | 1.015× more |

</details>

Public fixture sources:

- [Django German](https://raw.githubusercontent.com/django/django/dab0a5c47f159eb58472110dcbc10bd4a9b01adb/django/conf/locale/de/LC_MESSAGES/django.po) (unchanged contents; source SHA256 in JSON).
- [Wagtail German](https://raw.githubusercontent.com/wagtail/wagtail/e18fa1162b2fd352cefef345d9f558cc7fbdbcf3/wagtail/admin/locale/de/LC_MESSAGES/django.po) (unchanged contents; source SHA256 in JSON).
- [Wagtail French](https://raw.githubusercontent.com/wagtail/wagtail/e18fa1162b2fd352cefef345d9f558cc7fbdbcf3/wagtail/admin/locale/fr/LC_MESSAGES/django.po) (unchanged contents; source SHA256 in JSON).
