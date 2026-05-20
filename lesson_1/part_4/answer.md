# Chicago Taxi Fares

Below we discuss the Chicago Taxi Trips public dataset and the transformations we
have applied to it for the purposes of predicting a high tip (>20% of fare).

##  Data Source and its limitations

The data source we use comes from a public data source of Taxi Trips in the city of
Chicago. It is at the trip grain, detailing the (anonymized) start and end state of the
trip and keeping track of key variables such as taxi company, speed, distance, fare,
and many other details. This dataset has a number of limitations, including a large
number of 0 fare, 0 distance, or 0 second duration trips. This is likely caused by
cancelled fares or malfunctions with the meter. It is also unlikely to include all tips
as it is fairly common to tip a taxi driver in cash, and taxi drivers may not always
report those tips. This is also reported data, and so this data may have lags in being
updated as various companies provide information on differing schedules.

## Bronze -> Silver Transformations

In creating our silver dataset, we filtered to 2023 credit card trips. This
significantly reduces both the reporting lag issue, as everything for 2023 should
already be reported, as well as minimizes the cash tip issue, as one is much less likely
to tip in cash if you have already paid with a credit card. We have also removed the
significant number of zero miles, zero second, zero fare, or negative tips. Finally,
we filtered to those rows where company and pickup_community_area are non-null, as these
are important qualitative variables to be used at least for analysis of outcomes if not
directly for prediction.

## Silver -> Gold Transformations

In transforming to our gold dataset, we first split into train/test in a roughly 80/20
ratio by time. This amounted to splitting from October and on into the test dataset. We
also engineered our target, as we are specifically focused on whether or not the tip was
above 20% of the fare. Therefore, we created an explicit indicator that is 1 when the
tip was >20%, and 0 otherwise.

We then engineered a few additional features, such as previous trip fare, potentially
picking up on signal correlated with fare price, such as peak demand times. We also
looked at average trip miles over the previous 5 trips for each company, the pickup hour,
the average speed, and whether or not the trip occured on a weekend. All of these
features correspond to various potential signals that could come from the mindset or
type of requests they are receiving. For example, a trip on the weekend, especially at
night, is much more likely to include folks going out for the night, and may involve
alcohol. This could, at a minimum, introduce a higher volatility to the likelihood of a
large tip.

## Quality Checks

We have included a number of quality checks, utilizing the `great_expectations` python
package. First, we verify that our target column and the company column are not null.
We also verify that pickup hour is within a reasonable range, 0-23, to ensure there are
not any data entry errors. We also verify that the unique keys are in fact unique,
that the train-test split was appropriately assigned by verifying all values are either
train or test, and that our is_weekend feature is truly binary. We then also
verify that the average of our high tip indicator is between .5 and .85, as the true
average is close to 78%, which indicates our 20% cutoff for "high tip" is too low. Finally, we
validate that the trip miles are always strictly greater than 0 to double check
our silver layer example.

Obviously, in a real example, we'd like to verify even more, but for the sake of brevity
within this exercise, we abbreviated the number of things to verify.

## Ownership

Traditionally, the bronze (if applicable) and silver level transformations would be
owned by an engineer, but in partnership and with heavy input from a data scientist.
This allows the engineer to ensure they are building a data asset that supports the work
the scientist needs to do, and ensures they are utilizing data sources appropriate to
the use case.

The gold level feature engineering transformations would generally be owned by a
scientist, at least in the sense of identifying and codifying the logic of what defines
the engineered features. However, the integration of those transformations into the
pipeline may be owned by an engineer (this would be true on our team at least).

The validation set is similar, in that the scientist would likely define what needs to
be validated, but the engineer may have ownership over the integration of that validation
in an automated fashion.

## Data Leakage Prevention

We prevented data leakage by first by splitting into train/test by time, as opposed to
randomly. This allows us to model our experiment as closely as possible to the challenge
faced in real life and include the temporal element of predicting into the future. We
also ensured that the split was included in our window functions, as they are intended
to be rolling inputs over time. We do not want our train dataset leaking into our test
information, so including the split into the partition prevents that.