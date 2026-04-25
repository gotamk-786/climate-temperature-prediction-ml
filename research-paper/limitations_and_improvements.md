# Limitations and Improvements

## Current Limitations

1. The original dataset is historical and city-level, so it does not directly include other explanatory variables such as rainfall, humidity, land cover, or urbanization.
2. Some exploratory plots use large random samples instead of every row because full plotting on millions of records is computationally expensive and visually cluttered.
3. Temperature uncertainty exists in the source dataset, which means the observations themselves contain estimation limits.
4. The project focuses on tabular machine learning models and does not include deep learning or advanced time-series forecasting models.

## Practical Improvements

1. Add more environmental features such as rainfall, elevation, humidity, and vegetation indicators.
2. Integrate remote-sensing or Google Earth Engine variables for richer climate context.
3. Test stronger forecasting approaches such as LSTM, Temporal Fusion Transformer, or Prophet-style time-series baselines.
4. Build separate regional models and compare their performance against the single global model.
5. Extend the analysis with a simple dashboard for interactive climate exploration.
