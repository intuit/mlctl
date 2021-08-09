

# @mlctl.job.processing(name='user_filter')
def main(pa):
    """
    Load inputs and parameters 

    Note: This is the processing entrypoint used by baklava!
    """
    # Read in the training data
    data = pa.input_as_dataframe()
    print(data)
    orig_length = len(data.index)
    # remove everyone under the age of 18
    x = data[data['age'] >= 18]

    pa.log_metric({'remaining_data_after_filter_percent': len(x.index) / orig_length})
    pa.log_metric({'remaining_data_after_filter_number': len(x.index)})
    # Save model object using the training adapter
    pa.log_artifact(x, 'data')

    print('Success!')