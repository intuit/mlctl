import yaml
from pathlib import Path
import time
import pprint

from mlctl.interfaces.train import Train
from mlctl.plugins.utils import parse_config, run_subprocess

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException

class KubernetesTrain(Train):

    def __init__(self, profile=None):
        self.provider = 'kubernetes'
        config.load_kube_config()

        try:
            c = Configuration().get_default_copy()
        except AttributeError:
            c = Configuration()
            c.assert_hostname = False

        Configuration.set_default(c)
        self.api_instance = core_v1_api.CoreV1Api()

    def start_train(self, job):

        job_definition = job.serialize()

        # create the env variable payload
        env_vars = [{
            'name': 'sriracha_output',
            'value': job_definition['data_channels']['output']
        }]
        
        # add hyperparameters
        for k, v in job_definition['hyperparameters'].items():
            env_vars.append({
                'name': 'sriracha_hp_' + k,
                'value': f'{v}'
            })

        # add other env vars
        for k, v in job_definition['env_vars'].items():
            env_vars.append({
                'name': k,
                # convert to string
                'value': f'{v}'
            })

        # TODO: hardcoded keys, to remove
        env_vars.append({
            'name': 'AWS_ACCESS_KEY_ID',
            'value': os.getenv('AWS_ACCESS_KEY_ID')
        })
        env_vars.append({
            'name': 'AWS_SECRET_ACCESS_KEY',
            'value': os.getenv('AWS_SECRET_ACCESS_KEY')
        })

        # create the data payload
        for channel in ['training', 'validation', 'testing']:
            if channel in job_definition['data_channels']['input']:
                env_vars.append({
                    'name': f'sriracha_input_{channel}',
                    'value': job_definition['data_channels']['input'][channel]
                })

        manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': job_definition['name'],
                'labels': {
                    'purpose': 'mlctl-job'
                },
            },
            'spec': {
                'containers': [{
                    'name': 'mlctl-train',
                    'image': job_definition['infrastructure']['train']['container_repo'] + ':train-image',
                    'env': env_vars
                }],
                # TODO: make this based on the platform yaml
                'imagePullSecrets': [{
                    'name': 'regcred'
                }],
                'restartPolicy': 'OnFailure'
            }
        }

        # copy over the resource requirements
        if 'resources' in job_definition['infrastructure']['train']:
            manifest['spec']['containers'][0]['resources'] = job_definition['infrastructure']['train']['resources']

         # save yaml in cache
        Path("./.mlctl/k8s").mkdir(parents=True, exist_ok=True)
        with open('./.mlctl/k8s/train.yaml', 'w') as outfile:
            yaml.dump(manifest, outfile, default_flow_style=False)
        
        if 'namespace' in job_definition['infrastructure']['train']:
            namespace = job_definition['infrastructure']['train']['namespace']
        # 

        # run command in k8s
        # based off 
        # https://github.com/kubernetes-client/python/blob/master/examples/pod_exec.py
        
        resp = self.api_instance.create_namespaced_pod(
            body=manifest, namespace=namespace)
        print("Deployment created. status='%s'" % resp.metadata.name)
        return resp

    def get_train_info(self, job, loop=False):

        response = self.api_instance.read_namespaced_pod(name=job.serialize()['name'],
            namespace=job.serialize()['infrastructure']['train']['namespace'])
        # print(response)
        if response.status.phase == 'Pending':
            
            print('Job in progress')
            time.sleep(10)
            
            return self.get_train_info(job, loop)
        
        print('Job Spec:')
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response)
        print('Job Completed')

    def stop_train(self, train_job_name, hyperparameter_tuning=False):
        return
