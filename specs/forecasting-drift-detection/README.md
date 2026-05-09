# Forecasting Drift Detection — placeholder module

> **Status: placeholder.** This module is reserved for evaluation methodology covering time-series forecasting systems under data-shift conditions. No spec has been authored yet. RFC welcome.

## Class of system in scope

Production-deployed forecasting systems — whether classical (ARIMA / ETS / Prophet) or modern (TimeGPT / TabPFN-TS / TimesFM / patch-TST family) — face a class of operational failures that don't show up in evaluation against held-out historical test sets:

- **Distribution-shift blindness** — model performs well in backtest but degrades silently when the underlying data-generating process shifts (regime change, intervention, post-pandemic reset).
- **Calibration collapse** — point forecasts stay reasonable but prediction intervals stop covering at the claimed level, breaking downstream decision-making that relied on the uncertainty quantification.
- **Stale-feature debt** — exogenous-feature pipelines drift (data sources change schemas, upstream signals get deprecated) and the model keeps producing forecasts on partially-stale features without flagging it.
- **Cross-series leakage** — multi-series forecasters silently leak information from a held-out series into a "training" series via shared embedding layers, masking the true generalization gap.

## Why this needs its own module

These failure modes are not addressed by standard MAE / MAPE / sMAPE / MASE evaluation. They require operational telemetry layered on top: data-quality assertions on the feature pipeline, calibration tracking over deployment windows, drift-detection on the residual distribution, and leakage audits on the embedding layer.

A spec under this module would codify what it means for a forecasting system to be *operationally ready* — including the runtime telemetry it must emit for an operator to detect drift before it shows up as a business-decision regression.

## When this module will graduate from placeholder

When a partner engagement covering this domain produces enough specific failure-mode evidence to anchor a draft spec. Likely vendors: time-series forecasting platforms, demand-planning vendors, energy-load-forecasting operators, financial-volatility forecasters.

## RFC

Practitioners working on production forecasting telemetry — file a GitHub issue on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[forecasting-drift-detection]` in the title.
