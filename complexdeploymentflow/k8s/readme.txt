
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/mandatory.yaml


kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-0.32.0/deploy/static/provider/baremetal/deploy.yaml


# dashboard 

kubectl proxy

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login


# service account 

 kubectl create serviceaccount sudeep -n default

 kubectl create clusterrolebinding sudeep-admin -n default --clusterrole=cluster-admin --serviceaccount=default:sudeep
 
 kubectl get secret $(kubectl get serviceaccount sudeep -o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 --decode