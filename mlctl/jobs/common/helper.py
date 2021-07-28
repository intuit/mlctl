def parse_infrastructure(params):
    '''
    Parse the infrastructure section of the provider YAML
    and assess the actual provider that this type of job should use.

    If there is only one provider in the infrastructure section, 
    it will be used for all jobs. Else, it will feed jobs the specific provider (SageMaker, AzureML, etc).
    '''

       # TODO: add validation on allowed infrastructure
    options = ['processing', 'training', 'hosting', 'batch']
    infra_options = {}
    # loop through the infra options
    # if no job_type, mark it as the default
    for infra in params:

        # parse through the current infra_option
        iter = {'name': infra['name']}
        iter['container_repo'] = infra['container_repo']

        # currently used for AWS
        if 'arn' in infra:
            iter['arn'] = infra['arn']

        # currently used for Azure
        if 'resource_group' in infra:
            iter['resource_group'] = infra['resource_group']
        
        if 'workspace_name' in infra:
            iter['workspace_name'] = infra['workspace_name']
        
        if type(infra) == str:
            iter['instance_type'] = infra
            iter['instance_count'] = 1
        elif 'instance' in infra:
            iter['instance_type'] = infra.instance 
            iter['instance_count'] = infra.count
        elif 'cpu' in infra:
            iter['cpu'] = infra.cpu
            iter['memory'] = infra.memory
        
        
        if 'job_type' in infra:
            # if selected, save the infra for a specific type
            
            for job in infra['job_type']:
                # save the infra choice for a job type
                if job in options:
                    infra_options[job] = iter
                else:
                    print(f'{job} in an invalid job type in provider yaml.')
        
        else: 
            # else save as the default option
            infra_options['default'] = iter
    
    options = ['processing', 'training', 'hosting', 'batch']
    for job in options:
        # save the infra choice for a job type
        if job not in infra_options:
            print(f'Copying default infra config to {job}')
            infra_options[job] = infra_options['default']

    # print(infra_options)

    # if hosting add in autoscaling params
    if ('resources' in infra_options['hosting'] and
        'instance_type' in infra_options['hosting']['resources'] and 
        'instance_count_max' not in infra_options['hosting']['resources']):
        infra_options['hosting']['resources']['instance_count_max'] = 1
        
    return infra_options