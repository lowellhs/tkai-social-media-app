kubectl apply  -f kube-env-secret.yml
kubectl create -f kube-postgres.yml
kubectl create -f kube-main-interface.yml
kubectl create -f kube-userapp.yml
kubectl create -f kube-timelineapp.yml
kubectl create -f kube-addfriendapp.yml
