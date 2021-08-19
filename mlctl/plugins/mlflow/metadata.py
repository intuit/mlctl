
def sriracha_bootstrapping(metadata, job):
    """
    Parse a metadata field and return entries that needs to go to Sriracha
    """
    job_spec = job.serialize()
    
    env_vars = {
        'provider': job_spec['env_vars']['sriracha_provider'] + ',mlflow',
        'mlflow_tracking_uri': metadata['tracking_uri']
    }
    job.add_env_vars(env_vars)
    return job