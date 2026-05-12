# Short Answer Questions

## Question 1: Random splitting and Data Leakage

- Explain why randomly splitting data between train and test causes data leakage in this
assignment.
    - Because this is time series data, splitting randomly could mean including a random
    selection of data from across the entire year in your sampling dataset. It makes
    your train/test split not mimic the reality that the model would actually be applied
    (where your model would be applied to a full series of time on which it was never
    trained). This allows your trained model to potentially pick up on patterns and
    trends from the random sampling of rows from December that it would not be able to
    do in reality. This would overstate the effectiveness of your model in your test
    evaluation, because it has more information further into the future.
- Explain why using a time-based split fixes this issue
    - Ultimately, a time-based split mimics the reality of how you use the model. You
    are evaluating it on a set of observations *and times* it has not seen before. So
    it does not have the opportunity to learn patterns from "the future", and so your
    test dataset evaluation is significantly more sound and predictive of future
    performance.

## Question 2: Feature engineering and data leakage

- Explain why computing a rolling window aggregation over the full dataset before
splitting causes data leakage.
    - It explicitly causes your test dataset along the edge of the cutoff to include
    information from your training dataset
    - *Fix*: When you utilize the window functions, includ ethe train/test split in the
    partition by clause. This way, the window resets at the boundary and test and train
    never see eachother.
- Explain why computing a company-level average tip rate over the full dataset before
splitting introduces leakage.
    - This puts information from your test set into the average calculation that will be
    used to train your model, in this case including future information into your
    training dataset.
    - *Fix* - Calculate the average tip rate using only the training data, then use
    those values for the test set. If a company is included in the test set but not the
    training set, use a global training mean as a fallback. This most closely aligns
    what you would have to do in production.
