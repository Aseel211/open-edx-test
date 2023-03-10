#!/bin/bash
set -e

echo "Spinning up xdist workers with pytest_worker_manager.py"
python scripts/xdist/pytest_worker_manager.py -a up -n ${XDIST_NUM_WORKERS} \
-ami ${XDIST_WORKER_AMI} \
-type ${XDIST_INSTANCE_TYPE} \
-s ${XDIST_WORKER_SUBNET} \
-sg ${XDIST_WORKER_SECURITY_GROUP} \
-key ${XDIST_WORKER_KEY_NAME} \
-iam ${XDIST_WORKER_IAM_PROFILE_ARN}

ip_list=$(<pytest_worker_ips.txt)
for ip in $(echo $ip_list | sed "s/,/ /g")
do
    worker_reqs_cmd="ssh -o StrictHostKeyChecking=no jenkins@$ip
    'git clone --branch master --depth 1 -q https://github.com/openedx/edx-platform.git; cd edx-platform;
    git fetch -fq origin ${XDIST_GIT_REFSPEC}; git checkout -q ${XDIST_GIT_BRANCH};
    scripts/xdist/setup_worker.sh -p $PYTHON_VERSION & "

    cmd=$cmd$worker_reqs_cmd
done
cmd=$cmd"wait"

echo "Executing commmand: $cmd"
eval $cmd
