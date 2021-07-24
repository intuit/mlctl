
def sriracha_bootstrapping(metadata, job):
    """
    Parse a metadata field and return entries that needs to go to Sriracha
    """
    job_spec = job.serialize()
    job_spec['env_vars']['sriracha_provider'] += ',mlflow'
    env_vars = {
        'sriracha_provider': job_spec['env_vars']['sriracha_provider'] + ',mlflow',
        'sriracha_mlflow_tracking_uri': metadata['tracking_uri']
    }
    job.add_env_vars(env_vars)
    return job