kubectl autoscale deployment postgres-deployment --cpu-percent=80 --min=1 --max=2
kubectl autoscale deployment mainapp-deployment --cpu-percent=80 --min=1 --max=2
kubectl autoscale deployment userapp-deployment --cpu-percent=80 --min=1 --max=2
kubectl autoscale deployment timelineapp-deployment --cpu-percent=80 --min=1 --max=2
kubectl autoscale deployment addfriendapp-deployment --cpu-percent=80 --min=1 --max=2